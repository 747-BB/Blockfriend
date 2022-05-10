import os
import platform

def get_engine_path():
    '''Returns the shared library path.'''
    here = os.path.dirname(__file__)
    system = platform.system()
    arch = platform.machine()
    if system == 'Windows':
        binary = 'blockfriend_engine.exe'
        path = os.path.join(here, f'''bin/{binary}''')
    else:
        binary = 'blockfriend_engine'
        path = os.path.join(here, f'''bin/{binary}''')
    return path