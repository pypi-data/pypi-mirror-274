from loguru import logger as log
from asyncio import sleep as async_sleep
from asyncio import get_event_loop
from time import time


class OutputBuffer:

    default_interval = 1.0

    def __init__(self, emitter):
        self._emitter = emitter
        self._flashpoints = {}

    async def run (self, model, flashpoint, delay=0):
        # log.success(f"RUN> {delay}")
        await async_sleep(delay)
        #
        output = []
        #
        #   Isolate meta and insert into output
        #
        for label in flashpoint.get('meta', {}):
            response = {
                'sid': flashpoint['sid'],
                'meta': flashpoint['meta'][label]
            }
            output.append((f'{model}_{label}', response))
        #
        #   Add data items
        #
        for label in flashpoint.get('data'):
            response = {}
            if isinstance(flashpoint['data'][label], list):
                response['data'] = flashpoint['data'][label]
            else:
                response['data'] = [v for v in flashpoint['data'][label].values()]
            if response['data']:
                response['sid'] = flashpoint['sid']
                flashpoint['data'].update({label: {}})
                output.append(((f'{model}_{label}', response)))
        #
        #   Reset trigger and flush output
        #
        flashpoint['trigger'] = False
        for entry in output:
            await self._emitter.emit(entry)
                
    async def enqueue (self, sid, model, label, response):
        # log.warning(f'ENQ> sid={sid} model={model} label={label} response={response}')
        try:
            if 'ids' in response:
                # log.warning(f'ENQ> emit={model}_{label}')
                await self._emitter.emit((f'{model}_{label}', response))
                return
            key = f'{sid}_{model}'
            if key not in self._flashpoints:
                self._flashpoints[key] = {'time': 0, 'trigger': None, 'sid': sid, 'data': {}}
            flashpoint = self._flashpoints[key]
            if label not in flashpoint['data']:
                flashpoint['data'][label] = {}
            
            if isinstance(response, dict):
                # log.warning("#1")
                for item in response.get('data', []):
                    flashpoint['data'][label][item['_id']] = item
                if 'meta' in response:
                    # log.warning("#2")
                    flashpoint['meta'] = {label: response['meta']}
            else:
                flashpoint['data'][label] = response

            # log.warning(f'Flashpoint: {flashpoint}')
                
            if flashpoint['trigger']:
                return
            flush = flashpoint['time']
            delay = 0 if time() > flush else flush - time()
            if not delay:
                flashpoint['time'] = time() + self.default_interval
            flashpoint['trigger'] = True
            # log.debug(f"# RUN {key} :: {delay} :: {list(flashpoint['data'].keys())}")
            await get_event_loop().create_task(self.run(model, flashpoint, delay))
        except Exception as e:
            log.exception(e)
        

class InputBuffer:
    
    default_interval = 1.0
    
    def __init__(self, next):
        self._flashpoints = {}
        self._next = next
        
    async def run (self, model, flashpoint, delay):
        await async_sleep(delay)
        docs = flashpoint.get('docs', [])
        # log.success(f'FLUSH: {model} => {len(docs)}')
        flashpoint.update({'docs': [], 'trigger': False})
        await self._next(model, docs)

    async def enqueue (self, model, docs):
        # log.debug(f'incoming: {model} => {len(docs)}')
        # log.info(f'ENQ> model={model}')
        if model not in self._flashpoints:
            self._flashpoints[model] = {'time': 0, 'trigger': False, 'docs': []}
        flashpoint = self._flashpoints[model]
        # if isinstance(docs, list):
            # for doc in docs:
                # log.info(f"Flash: {doc.doc}")
        # else:
            # log.info(f"Flash: {docs.doc}")
        flashpoint['docs'] += docs
        if flashpoint['trigger']:
            # log.warning('triggered')
            return
        flush = flashpoint['time']
        delay = 0 if time() > flush else flush - time()
        if not delay:
            flashpoint['time'] = time() + self.default_interval
        flashpoint['trigger'] = True
        # log.debug(f'task: {model} => delay={delay}')
        await get_event_loop().create_task(self.run(model, flashpoint, delay))
