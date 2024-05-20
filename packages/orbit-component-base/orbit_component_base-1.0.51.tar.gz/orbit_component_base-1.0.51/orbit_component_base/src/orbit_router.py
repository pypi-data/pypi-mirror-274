from aiohttp import web
from orbit_component_base.src.orbit_shared import world
from aiohttp import web, ClientSession, TCPConnector, client_exceptions
from aiohttp.web_exceptions import HTTPNotFound
from loguru import logger as log

routes = web.RouteTableDef()


class OrbitRouter:

    def __init__(self, context=None, args=None):
        self._context = context
        self._args = args
        self._namespaces = set([])

    async def redirect(self, request):
        try:
            if str(request.rel_url).startswith('/assets/'):
                path = str(request.rel_url)[1:]
                headers = {
                    'Cache-Control': 'max-age=0, s-maxage=0',
                    'Access-Control-Allow-Origin': '*'
                }
                origin = f"https://{world.conf.name}:{world.conf.vite_port}"
                headers['Origin'] = origin
                fullpath = world.conf.web / path
                try:
                    response =  web.FileResponse(fullpath.as_posix(), headers=headers)
                    return response
                except FileNotFoundError:
                    log.error(f'File not found: {fullpath.as_posix()}')
                    return ''
                except Exception as e:
                    log.error(e)
                    return ''
            if not world.conf.web or world.args.dev:
                async with ClientSession(connector=TCPConnector(verify_ssl=False), skip_auto_headers=['accept-encoding']) as session:
                    origin = f"https://{world.conf.name}:{world.conf.vite_port}"
                    try:
                        async with session.get(f'{origin}{request.rel_url}') as resp:
                            headers = dict(resp.headers)
                            headers['Origin'] = origin
                            headers['Cache-Control'] = 'max-age=0, s-maxage=0'
                            return web.Response(body=await resp.content.read(), status=resp.status, headers=headers)
                    except FileNotFoundError:
                        log.error(f'File not found2: {fullpath.as_posix()}')
                        return ''
                    except client_exceptions.ClientConnectorError as e:
                        log.error(f'VITE server is down on: {origin}')
                        return ''
            else:
                path = (request.path if request.path != '/' else 'index.html').strip('/')
                headers = {'Cache-Control': 'max-age=0, s-maxage=0'}
                fullpath = world.conf.web / path
                return web.FileResponse(fullpath.as_posix(), headers=headers)
        except FileNotFoundError:
            log.error(f'File not found3: {fullpath.as_posix()}')
            return ''
        except Exception as e:
            log.exception(e)
        return ''

    @web.middleware
    async def default_route(self, request, handler, *args):
        try:
            ns = request.path.strip('/').split('/')[0]
            return await (handler(request) if ns in self._namespaces else self.redirect(request))
        except HTTPNotFound:
            if world.conf.debug:
                log.debug (f'debug: 404 Not Found: {request.path}')
            return web.Response(body='404 Not Found', status=404)
        except Exception as e:
            log.exception(e)

    def application(self):
        app = web.Application(client_max_size=1024*1024*1024, middlewares=[self.default_route])
        if world.conf.debug:
            log.debug(f'debug: Installing routes: {routes}')
            for route in routes:
                log.debug(f'debug: -> {route}')
        app.add_routes(routes)
        return app
    
    def add_namespace (self, nsp):
        self._namespaces.add(nsp)
