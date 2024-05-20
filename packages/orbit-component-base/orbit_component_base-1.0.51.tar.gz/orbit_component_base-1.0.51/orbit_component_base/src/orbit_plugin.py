from socketio import AsyncNamespace
from orbit_component_base.src.orbit_nql import NQL
from orbit_component_base.src.orbit_auth import OrbitAuth
from orbit_component_base.src.orbit_decorators import Sentry, check_own_hostid
from orbit_component_base.schema.OrbitSessions import SessionsCollection
from orbit_component_base.schema.OrbitSessions import SessionsTable
from loguru import logger as log
from orbit_component_base.src.orbit_shared import world

VALIDATORS = []

class ValidatorBase (AsyncNamespace):
    
    def __init__ (self):
        print("Missing Something!")

def install_validator (models, func):
    VALIDATORS.append((models, func))    

def validate (session, nsp, name, args):
    model = args[2].get('model')
    if not model:
        log.error(f'No Model: {args[2]}')
        return False
    # log.warning(f'Checking model: {model}')
    for models,func in VALIDATORS:
        if model in models:
            # log.debug(f"Test> {model} {models} {func}")
            if not func (session, nsp, name, args):
                log.error(f'Fail: {func}')
                return False
            # log.error(f'Pass: {func}')
    # log.success(f'Succeeded: {model}')
    return True
       
install_validator (['users', 'group_permissions'], check_own_hostid)


class PluginBase (AsyncNamespace):

    NAMESPACE = ''
    COLLECTIONS = []

    @property
    def ns (self):
        return f'/{self.NAMESPACE}'

    def __init__(self, *args, **kwargs):
        # log.debug(f'Initialise namespace: {self.ns}')
        kwargs['namespace'] = self.ns
        self._odb = kwargs.pop('odb')
        self._nql = None
        self._collections = []
        super().__init__(*args, **kwargs)

    def open (self, nql=True):
        # if world.conf.debug:
        #     log.success(f'Open namespace: {self.ns}')
        if nql:
            self._nql = NQL(self.emit, self.ns).open()
        for cls in self.COLLECTIONS:
            cls().open(self._odb, self._nql)
        if nql:
            SessionsCollection().flush(self.ns)
        return self
    
    def register (self, sio):
        sio.register_namespace(self)
        return self
    
    async def on_connect(self, sid, environ):
        await self.save_session(sid, {
            'sid': sid,
            'address': environ['aiohttp.request'].transport.get_extra_info('peername')[0]
        })
        self._nql.connect(sid, await self.get_session(sid))

    async def on_disconnect(self, sid):
        self._nql.disconnect(sid)
        SessionsTable().from_sid(sid).delete()

    async def on_auth_hello(self, sid, auth):
        return await OrbitAuth(sid, self.ns).hello(auth, self.get_session, self.save_session)

    async def on_auth_validate(self, sid, auth):
        # log.info(f'Validated access for session={sid} to namespace={self.NAMESPACE}')
        return await OrbitAuth(sid, self.ns).validate(auth, self.get_session, self.save_session)

    async def on_auth_confirm(self, sid, auth):
        return await OrbitAuth(sid, self.ns).confirm(auth, self.get_session, self.save_session)

    @Sentry(validate)
    async def on_call_nql(self, sid, params):
        return self._nql.call(sid, params)

    @Sentry()
    async def on_drop_nql(self, sid, params):
        return self._nql.drop(sid, params)

    @Sentry()
    async def on_dump_nql(self, sid):
        return self._nql.dump ()
    

class ArgsBase:

    def __init__ (self, parser=None, args=None):
        self._parser = parser

    def setup (self):
        return self

    def open (self, odb=None, args=None):
        self._odb = odb
        self._args = args
        return self

    def process (self):
        return self
