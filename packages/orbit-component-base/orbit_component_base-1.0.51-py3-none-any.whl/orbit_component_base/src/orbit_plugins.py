from pkgutil import iter_modules
from importlib.util import module_from_spec
from sys import modules
from loguru import logger as log


class Plugins:

    PLUGIN_FOLDER = 'orbit_plugins'
    REQUIRED = 'orbit_component_base'

    def __init__ (self, cls):
        self._cls = cls

    def __iter__ (self):
        plugins = {}
        for importer, package_name, _ in iter_modules([self.PLUGIN_FOLDER]):
            plugins[package_name] = importer
        for importer, package_name, _ in iter_modules():
            if package_name.startswith('orbit_component_'):
                plugins[package_name] = importer
        
        plugin = self.load(importer, self.REQUIRED)
        if hasattr(plugin, self._cls):
            yield modules[self.REQUIRED]
        plugins.pop(self.REQUIRED, None)
        
        for (package_name, importer) in plugins.items():
            plugin = self.load(importer, package_name)
            if hasattr(plugin, self._cls):
                yield modules[package_name]

    def load (self, importer, name):
        if name not in modules:
            spec = importer.find_spec(name)
            if not spec:
                log.error(f'failed to find loader for: {name}')
                return None
            modules[name] = module_from_spec(spec)
            spec.loader.exec_module(modules[name])
        return modules[name]
