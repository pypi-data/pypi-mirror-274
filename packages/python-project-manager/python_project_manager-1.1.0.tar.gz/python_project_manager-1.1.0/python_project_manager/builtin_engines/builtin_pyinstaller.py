import os

from python_project_manager.app import sanitize_string_for_module
from python_project_manager.config import Config


def init(_method, **kwargs) -> bool:
    print('Initializing PyInstaller Engine...')
    initRunner = kwargs['initRunner']
    initRunner['Dependencies'].append('pyinstaller==6.5.0 --dev')

    set_default_scripts(initRunner)
    create_template_app(initRunner)
    return True

def create_template_app(initRunner: object) -> None:
    src_dir = initRunner['ConfigValues']['src_dir']
    initRunner['Files'].append({'Target': f'{src_dir}/app.py', 'Content': '''import os
import sys

try: # PyInstaller creates a temp folder and stores path in _MEIPASS
    resource_dir = sys._MEIPASS
except AttributeError: # If not running as a PyInstaller created executable
    resource_dir = 'src/resources'

# Example: os.path.join(resource_dir, 'file.ext')

def app(): # This function is the entry point of the application.
    print("Hello World.")

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)
    # This line is used to prevent the console from closing immediately after the program finishes execution.
    input("Press Enter to continue...")
'''})
    
    initRunner['Folders'].append(f'{src_dir}/resources')

def set_default_scripts(initRunner: object) -> None:
    
    buildcmd: str = (
        f'pyinstaller %src_dir%/app.py' +
        f' --noconfirm --clean --onefile --name %project_name%_v%version%' +
        f' --add-data %src_dir%/resources:.'
        )
    
    initRunner['ConfigValues']['src_dir'] = 'src'
    initRunner['ConfigValues']['version'] = '0.0.0'
    initRunner['ConfigValues']['scripts.build'] = buildcmd
    initRunner['ConfigValues']['scripts.start'] = f'python -m %src_dir%.app'