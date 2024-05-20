import functools
import sys
from loguru import logger as log
from asyncio import sleep
from time import time
from os import times
from orbit_component_base.schema.OrbitGroupPermissions import GroupPermissionsCollection
from orbit_component_base.schema.OrbitUsers import UsersTable


permissions = []


async def watch(func, args, kwargs):
    try:
        tstart = time()
        cstart = times()
        try:
            output = await func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}
        tend = time()
        cend = times()
        real_time = (tend - tstart) * 1000
        sys_time = (cend[0] - cstart[0]) * 1000
        usr_time = (cend[1] - cstart[1]) * 1000
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                if len(arg) > 20:
                    arg = arg[:20] + '...'
            elif isinstance(arg, bytes):
                if len(arg) > 20:
                    arg = arg[:20] + b'...'
            new_args += [arg]
        if len(new_args) > 2:
            params = new_args[2]
            if isinstance(params, dict):
                log.log('RPC', f'{func.__name__} => {params.get("method")} :: real={real_time:.0f}ms, sys={sys_time:.0f}ms usr={usr_time:.0f}ms repeat@{1000/real_time:.0f}/sec')
                return output
        log.log('RPC', f'{func.__name__} :: real={real_time:.0f}ms, sys={sys_time:.0f}ms usr={usr_time:.0f}ms repeat@{1000/real_time:.0f}/sec') ## :: {new_args}')
        return output
    except Exception as e:
        log.exception(e)

def check_permission (session, nsp, name, args):
    host_id = session.get('host_id')
    user = UsersTable().from_key(host_id)
    if not user.isValid:
        return False
    if 'admin' in user._groups:
        return True
    exec = args[3] if len(args) > 3 else 'default'
    if nsp in (user._groups or []):
        return True
    for group_id in (user._groups or []):
        if GroupPermissionsCollection(args[1]).check(group_id, nsp, name, exec):
            return True
    log.debug(f'Permission denied, user={user.doc} namespace={nsp} name={name} exec={exec}')
    return False

def check_own_hostid (session, nsp, name, args):
    # log.debug(f'[check host id] nsp={nsp} name={name} args={str(args)}')
    if len(args) > 2 and 'host_id' in args[2]:
        # log.success(f'Compare: {args[2].get("host_id")} || {session.get("host_id")}')
        return args[2].get('host_id') == session.get('host_id')
    return True

def Sentry(fn=None, nsp=None, desc=None):
    def navGuard(func):
        if fn and nsp:
            f = list(sys._current_frames().values())[0]
            permissions.append((f.f_back.f_globals["__package__"], nsp, func.__name__, desc))
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                retrying = False
                while True:
                    try:
                        session = await args[0].get_session(args[1])
                    except KeyError:
                        log.warning('<< disconnected dead session >>')
                        return {'ok': False, 'error': 'Server was restarted'}
                    except Exception as e:
                        log.exception(e)
                        raise
                    if not session.get('activated', False):
                        if not retrying:
                            # log.debug(f'<< waiting for authentication >> {args[1]}')
                            retrying = True
                        await sleep(0.1)
                        continue
                    try:
                        if fn and not fn(session, nsp, func.__name__, args):
                            log.error(error := f'you do not have permission to access this endpoint: {func.__name__}')
                            return { 'ok': False, 'error': error }
                        return await watch(func, args, kwargs)
                    except Exception as e:
                        log.exception(e)
                        log.error(f'Args: {str(args)}')
                        return { 'ok': False, 'error': str(e) }
            except Exception as e:
                log.exception(e)
        return wrapper
    return navGuard
