#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path
from datetime import datetime
from loguru import logger as log
from orbit_component_base.src.orbit_shared import world
from platform import system
from cryptography.fernet import Fernet, InvalidToken


class Section:

    def __init__ (self, name):
        self._name = name

    def __getattr__(self, key):
        try:
            return super().__getattr__(key)
        except AttributeError:
            return None


class OrbitConfig:

    BASE_authentication = 'autoenroll'
    BASE_name = 'localhost'
    BASE_network_host = '127.0.0.1'
    BASE_network_port = '8445'

    @property
    def path (self):            return Path(self._conf.get('BASE', 'path')).expanduser()

    @property
    def code (self):            return Path(self._conf.get('BASE', 'code')).expanduser()

    @property
    def authentication (self):  return self._conf.get('BASE', 'authentication')

    @property
    def name (self):            return self._conf.get('SSL', 'name')

    @property
    def ssl (self):             return self.mkpath('SSL', 'ssl')

    @property
    def secure (self):          return self._conf.getboolean('SSL', 'secure')
    
    @property
    def host (self):            return self._conf.get('NETWORK', 'host')

    @property
    def port (self):            return self._conf.getint('NETWORK', 'port')

    @property
    def sio_debug (self):       return self._conf.getboolean('NETWORK', 'sio_debug')

    @property
    def engineio_debug (self):  return self._conf.getboolean('NETWORK', 'engineio_debug')

    @property
    def vite_port (self):       return self._conf.getint('DEV', 'vite_port')

    @property
    def debug (self):           return self._conf.getboolean('DEV', 'debug')

    @property
    def make_keys (self):       
        return self._conf.get('DEV' if world.args.dev else 'BASE', 'make_keys')

    @property
    def database (self):        return self.mkpath('DATA', 'database')

    @property
    def tmp (self):             return self.mkpath('DATA', 'tmp')

    @property
    def templates (self):       return self.mkcode('DATA', 'templates')
    
    @property
    def web (self):             return self.mkcode('DATA', 'web')

    @property
    def logs (self):             return self.mkpath('DATA', 'logs')

    @property
    def writemap (self):        return self._conf.get('DATA', 'writemap')

    @property
    def token (self):           return self._conf.get('ENCRYPTION', 'token').encode()

    def __init__ (self, application):
        self._appl = application
        self._path = Path('~/.local/' + application).expanduser()
        self._file = (self._path / 'config.ini').expanduser()
        self._conf = None
        self._changed = False

    def setup_logging (self):
        try:
            level = log.level('RPC')
        except ValueError:
            log.level('RPC', no=10, color="<magenta>", icon='🗒️')
        if world.args and not world.args.dev:
            log.remove()
            Path(self.logs).mkdir(exist_ok=True)
            log.add((self.logs / 'orbit_access.log').as_posix(), level='RPC', colorize=True, rotation="10 MB", retention="3 days",
                filter=lambda record: record['name'] == 'src.orbit_decorators', enqueue=True)
            log.add((self.logs / 'orbit_system.log').as_posix(), colorize=True, rotation="10 MB", retention="3 days",
                filter=lambda record: record['name'] != 'src.orbit_decorators', enqueue=True)

    def _option (self, section, name, value, comment):
        if not self._conf.has_option(section, name):
            self._conf.set(section, f'# {name}', comment)
            self._conf.set(section, name, value)
            self._changed = True

    def mkpath (self, section, option):
        return self.mk(section, option, self.path)
    
    def mkcode (self, section, option):
        return self.mk(section, option, self.code)

    def mk (self, section, option, path):
        value = self._conf.get(section, option)
        if not value:
            return None
        if value[0] in './~':
            p = Path(self._conf.get(section, option)).expanduser()
        else:
            p = path / self._conf.get(section, option)
        try:
            if not world.args or not world.args.dev:
                p.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass
        return p

    def open (self):
        self._path.mkdir(parents=True, exist_ok=True)
        self._conf = ConfigParser()
        self._conf.read(self._file.as_posix())
        #
        #   V2, generate read-only object
        #
        for section in self._conf.sections ():
            local_section = Section (section)
            for key in self._conf[section]:
                setattr (local_section, key, self._conf[section][key])
            setattr (self, section, local_section)
        #
        #
        #
        for section in ['BASE', 'NETWORK', 'TOOLS', 'DATA', 'SSL', 'DEV', 'ENCRYPTION']:
            if section not in self._conf.sections():
                self._conf.add_section(section)
                self._changed = True
                
        if system() == 'Darwin':
            code_path = f'/Applications/{self._appl}.app/Contents/Resources/'
        else:
            if world.args and world.args.dev:
                code_path = f'~/{self._appl}/server'
            else:
                code_path = f'/opt/{self._appl}'

        self._option('BASE', 'path', f'~/.local/{self._appl}', 'base location for this application')
        self._option('BASE', 'code', code_path, "where the application's code is located")
        self._option('BASE', 'authentication', self.BASE_authentication, 'the default type of authentication (autoenroll/secure)')
        self._option('BASE', 'make_keys', f'{code_path}/scripts/make_keys.sh', 'the folder we store our make_keys script in')        
        self._option('SSL', 'name', self.BASE_name, 'the host name (CN) for our SSL certificate')
        self._option('SSL', 'ssl', 'ssl', 'the folder to store SSL files in')
        self._option('SSL', 'secure', 'true', 'whether to use SSL or not')
        self._option('NETWORK', 'host', self.BASE_network_host, 'the host to expose the server on, use "0.0.0.0" for a local network')
        self._option('NETWORK', 'port', self.BASE_network_port, "the port to expose the server on")
        self._option('DEV', 'vite_port', '5173', 'the port to run "vite" on')
        self._option('DEV', 'debug', 'false', 'whether debugging is enabled or not')
        self._option('DEV', 'make_keys', 'scripts/make_keys.sh', 'the folder we store our make_keys script in')
        self._option('NETWORK', 'sio_debug', 'false', 'SIO debugging')
        self._option('NETWORK', 'engineio_debug', 'false', 'AIO debugging')
        self._option('DATA', 'database', 'orbit_database', 'the path name of the folder to store data in')
        self._option('DATA', 'tmp', 'tmp', 'the path name of a temporary folder')
        self._option('DATA', 'templates', 'templates', 'the path name of the folder to store templates in')
        self._option('DATA', 'web', 'web', 'the path name of the folder to store web assets for in production mode')
        self._option('DATA', 'logs', 'logs', 'the path name of the folder to store logs in')
        self._option('DATA', 'writemap', 'true', 'whether to use WRITEMAP on the database')
        self._option('ENCRYPTION', 'token', Fernet.generate_key().decode(), 'a default field encryption key for the database [back this up!]')
        if self._changed:
            with open(self._file.as_posix(), 'w') as configfile:
                self._conf.set('DEFAULT', 'updated', datetime.now().isoformat())
                self._conf.write(configfile)
        self.setup_logging()                
        return self


if __name__ == '__main__':
    conf = OrbitConfig('Demo').open()
    print("Path           =", conf.path)
    print("Code           =", conf.code)
    print("Name           =", conf.name)
    print("SSL            =", conf.ssl)
    print("Host           =", conf.host)
    print("Port           =", conf.port)
    print("sio_debug      =", conf.sio_debug)
    print("engineio_debug =", conf.engineio_debug)
    print("make_keys      =", conf.make_keys)
    print("database       =", conf.database)
    print("templates      =", conf.templates)
    print("web            =", conf.web)
    print("token          =", conf.token)
