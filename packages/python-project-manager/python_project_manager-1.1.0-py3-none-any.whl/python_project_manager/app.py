import importlib
import os
import re
from types import ModuleType
from typing import Any, Callable
import click
from python_project_manager import Config

VENV = f'venv\\Scripts\\activate'

InitRunner = {
    'ConfigValues': {},
        'scripts.start': 'py -m %src_dir%.app',
        'src_dir': 'src',
        'version': '0.0.0',
    'Dependencies': [],
    'Files': [],
    'Folders': []
}

def sanitize_string_for_file(string: str) -> str:
    """
    Sanitizes a string for use as a file name by removing leading/trailing whitespace
    and replacing spaces and hyphens with underscores.

    Args:
        string (str): The string to be sanitized.

    Returns:
        str: The sanitized string.
    """
    sanitized_string = string.strip()
    sanitized_string = re.sub(r' |-', '_', sanitized_string)
    return sanitized_string

def sanitize_string_for_module(string: str) -> str:
    """
    Sanitizes a string for use as a module name.

    Args:
        string (str): The string to be sanitized.

    Returns:
        str: The sanitized string.

    """

    sanitized_string = string.strip()
    sanitized_string = re.sub(r' ', '_', sanitized_string)
    return sanitized_string

def pass_command_to_engine(_command: str, _method: Callable[..., bool], **_kwargs) -> bool:
    try:
    # built-in engines
        
        engine = get_engine(_kwargs.get('_engine', Config.get('engine')))
        method: Callable[..., bool] = getattr(engine, _command, None)
        if method:
            keep_processing = method(_method, **_kwargs)
            # If keep_processing is None or True, continue processing
            if keep_processing is None or keep_processing:
                return _method(**_kwargs)
        else:
            return _method(**_kwargs)

    except Exception as e:
        if Config.get('engine') == '':
            return _method(**_kwargs)
        else:
            raise e

def get_engine(engine_name: str) -> ModuleType | None:
    if engine_name == None or engine_name == '':
        return None
    match engine_name:
        case 'ppm-builtin-setuptools': # Built-in engine
            return importlib.import_module('.builtin_engines.builtin_setuptools', package='python_project_manager')
        case 'ppm-builtin-pyinstaller': # Built-in engine
            return importlib.import_module('.builtin_engines.builtin_pyinstaller', package='python_project_manager')
        case _: # External engine
            return importlib.import_module(sanitize_string_for_file(engine_name))
        
@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_name', type=str, required=True)
@click.option('--engine', '-e', type=str, default='',
    help='Choose the engine \'module\' to use. Built in engines are \'ppm-builtin-setuptools\' and \'ppm-builtin-pyinstaller\'.')
@click.option('--force', '-f', is_flag=True, help='Force initialization of the project')
# @click.option('--python', '-p', type=str, default='', help='Python version to use')
def init(project_name: str, engine: str, force: bool) -> None:
    '''
    <project_name> - Name of the project to be setup
    '''
    # Check if the project has already been initialized
    if not force and Config.load():
        print('Project already initialized')
        return False
    
    # Check if the engine is available
    try:
        get_engine(engine)
    except ImportError:
        print(f"Engine '{engine}' not found")
        return False

    # Set the project name and engine
    InitRunner['ConfigValues']['project_name'] = project_name
    InitRunner['ConfigValues']['engine'] = engine

    # Even though the looks like it belongs in the '_init' method,
    # it is placed here so external engines can not stop nessary files from being created

    # Create the requirements.txt and requirements-dev.txt files
    with open(os.path.join(os.getcwd(), 'requirements.txt'), 'w') as file:
        pass
    with open(os.path.join(os.getcwd(), 'requirements-dev.txt'), 'w') as file:
        pass

    # Create the venv
    os.system('python -m venv venv')

    # Initialize the project
    pass_command_to_engine('init', _init,
        initRunner=InitRunner, _engine=engine)    

def _init(**kwargs) -> bool:
    initRunner = kwargs['initRunner']

    # Set up the configuration values
    for key, value in initRunner['ConfigValues'].items():
        Config.set(key, value)
    Config.save()

    # Install the dependencies
    for dep in initRunner['Dependencies']:
        os.system(f'ppm install {dep}')

    # Create the project directory
    src_dir = os.path.join(os.getcwd(), initRunner['ConfigValues']['src_dir'])
    os.makedirs(src_dir, exist_ok=True)

    # Create the project directories
    for folder in initRunner['Folders']:
        os.makedirs(os.path.join(os.getcwd(), folder), exist_ok=True)

    # Create the project files    
    for file in initRunner['Files']:
        with open(os.path.join(os.getcwd(), file['Target']), 'w') as f:
            f.write(file['Content'])

    return True

@cli.command()
@click.argument('script_name', type=str, required=True)
def run(script_name) -> None:
    '''
    <script_name> - Name of the script to be run
    '''
    
    cli_command: str = Config.get(f'scripts.{script_name}')
    
    pass_command_to_engine('run', _run,
        script_name=script_name, cli_command=cli_command)

def _run(**kwargs) -> bool:
    cli_command: str = kwargs.get('cli_command', None)
    script_name: str = kwargs.get('script_name', None)

    if not cli_command:
        print(f"Script '{script_name}' not found")
        return

    ## Smart change directory
    cwd = os.getcwd() # Get the current working directory

    # Check if the command has a change directory command
    has_change_directory_command = re.search(r'(^|\s)cd\s\w*', cli_command)
    if not has_change_directory_command:
        # Searches for the 'python' command along with the script path
        python_command = re.search(r'python.*\.py', cli_command)
        if python_command:
            # Get the python path
            python_path = re.search(r'\S*\.py', python_command[0])
            if python_path:
                # Get the first dir in python path
                targ_dir = re.search(r'^\w*(.|\|/)(?!py)', python_path[0])
                if targ_dir:
                    # Join the target dir with the current working directory
                    cwd = os.path.join(cwd, targ_dir[0][:-1])
                    # Remove targ_dir from python_path
                    cli_command = cli_command.replace(python_path[0],python_path[0].replace(targ_dir[0], ""))
                    if targ_dir[0][:-1] == Config.get('test_dir'):
                        cli_command = f'set PYTHONPATH=C:\\{Config.get('src_dir')};%PYTHONPATH% && {cli_command}'
                        
    os.chdir(cwd) # Change the current working directory
    os.system(f'{VENV} && {cli_command}') # Run the command

@cli.command()
@click.argument('action', type=click.Choice(['inc', 'dec', 'show', 'set', 'sync']), required=True, default='show')
@click.option('--major', '-M', type=int, default=0, help='Change the major version')
@click.option('--minor', '-m', type=int, default=0, help='Change the minor version')
@click.option('--patch', '-p', type=int, default=0, help='Change the patch version')
@click.option('--timestamp', '-t', is_flag=True, help='Include timestamp in the version')
def version(action, major, minor, patch, timestamp) -> None:
    '''
    <action> - Action to perform on the version
    '''
    if action == 'show':
        print(Config.get('version'))
        return

    pass_command_to_engine('version', _version,
        action=action, major=major, minor=minor, patch=patch, timestamp=timestamp)

def _version(**kwargs) -> bool:
    action: str = kwargs.get('action', None)
    if action == 'sync':
        print('No built-in sync action, external engine sync action may have been called')
        return True
    
    major: str = kwargs.get('major', None)
    minor: str = kwargs.get('minor', None)
    patch: str = kwargs.get('patch', None)
    timestamp: str = kwargs.get('timestamp', None)

    # Split the version by '.' and '+'
    version_list = re.split(r'\.', Config.get('version'))
    ver_major = int(version_list[0])
    ver_minor = int(version_list[1])
    ver_patch = int(version_list[2])
    ver_timestamp = version_list[3] if len(version_list) > 3 else ''

    # Increment the version
    if action == 'set':
        if major:
            ver_major = major
        if minor:
            ver_minor = minor
        if patch:
            ver_patch = patch
    elif action == 'inc':
        if major:
            ver_minor = 0
            ver_patch = 0
        elif minor:
            ver_patch = 0
        elif patch:
            pass

        ver_major += major
        ver_minor += minor
        ver_patch += patch
    elif action == 'dec':
        ver_major -= major
        ver_minor -= minor
        ver_patch -= patch

    if timestamp:
        import time
        ver_timestamp = time.strftime('%Y%m%d%H%M%S')

    #concat the version
    version = f'{ver_major}.{ver_minor}.{ver_patch}'
    if timestamp:
        version = f'{version}.{ver_timestamp}'

    print(f'Version: {Config.get('version')} -> {version}')
    Config.set('version', version)
    Config.save()
    return True

# Pip commands
@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.option('--help', '-h', is_flag=True) # Allows '--help' to be passed as an argument
def list(args, help) -> None:
    '''
    Uses pip's 'list' command
    '''
    if help:
        os.system(f'{VENV} && pip list --help')
    else:
        os.system(f'{VENV} && pip list {' '.join(args)}')

@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.option('--dev', '-d', is_flag=True) # Add the package to the dev requirements
@click.option('--help', '-h', is_flag=True) # Allows '--help' to be passed as an argument
def install(args, help, dev) -> None:
    '''
    Uses pip's 'install' command
    '''
    # Create the command
    cmd = f'{VENV} && pip install {" ".join(args)}'.strip()

    # If 'pip install pip' is passed, install pip
    if cmd == f'{VENV} && pip install pip':
        os.system(f'{VENV} && python -m ensurepip')
        return

    # Use the help command if the '--help' flag is passed
    if help:
        os.system(f'{VENV} && pip install --help')
        return

    # If no arguments are passed, install the requirements
    if cmd == f'{VENV} && pip install':
        os.system(f'{VENV} && pip install -r requirements.txt -r requirements-dev.txt')

    # Otherwise, install the packages
    output = os.popen(cmd)

    # Read and print each line of the output
    for line in output:
        print(line.strip())
        if 'Successfully installed' in line:
            # Update the requirements file
            update_requirements(line.strip(), dev)

    # Close the output stream
    output.close()
    
def update_requirements(packages_to_update: str, is_dev=False) -> None:
    requirement_file = 'requirements-dev.txt' if is_dev else 'requirements.txt'
    packages_to_update = packages_to_update.replace('Successfully installed ', '').split(' ')
    packages_to_update = [re.split(r'-(?=[^-]*$)', package) for package in packages_to_update]
    packages_to_update = [(package[0], package[1]) for package in packages_to_update]
    
    packages_to_keep = []
    with open(requirement_file, 'r') as file:
        for line in file:
            package_name = re.match(r'^(\w|_|-|\d)*', line.strip())[0]
            if package_name not in [package[0] for package in packages_to_update]:
                packages_to_keep.append(line)

    packages_to_write = []

    for package in packages_to_update:
        packages_to_write.append(f'{package[0]}~={package[1]}'.strip())
    for package in packages_to_keep:
        packages_to_write.append(f'{package}'.strip())

    packages_to_write.sort()

    with open(requirement_file, 'w') as file:
        file.write('\n'.join(packages_to_write))

if __name__ == '__main__':
    cli()