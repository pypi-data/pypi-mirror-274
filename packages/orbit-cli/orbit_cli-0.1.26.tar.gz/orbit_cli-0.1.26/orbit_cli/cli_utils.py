from tempfile import NamedTemporaryFile
from os import remove, environ
from subprocess import run, call as call_process
from rich import print
from rich.prompt import Confirm, Prompt
from sys import version_info
from pathlib import Path
from importlib.util import find_spec
from jinja2 import Environment, FileSystemLoader, select_autoescape


class Utils:
    
    LABEL = 'OrbitCLI'

    def __init__ (self, args):
        self._args = args
        self._vars = {}
        self._orbit = find_spec('orbit_cli').submodule_search_locations[0]
        self._templates = f'{self._orbit}/templates'
        self._env = Environment (
            loader=FileSystemLoader(self._templates),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    @property
    def project (self):
        return self._vars.get('project')

    @property
    def project_path (self):
        return self._vars.get('project_path') or self.project

    @property
    def component (self):
        return self._vars.get('component')

    @property
    def project_type (self):
        return self._args.init if self._args.init is not None else 'application'

    def call (self, msg, text):
        self.msg (msg)
        with NamedTemporaryFile(suffix='.sh', mode='w', delete=False) as io:
            io.write (text)
        call_process (['bash', io.name])
        remove(io.name)

    def shell (self, msg, cmd):            
        self.msg (msg)
        run(['bash', '-c', f'source ~/.bash_profile && source ~/.pyenv/versions/{self.project_path}/bin/activate && {cmd}'])

    def call_shell (self, msg, cmd):            
        self.msg (msg)
        # call_process ([cmd], shell=True)
        run(['bash', '-c', f'source ~/.bash_profile && {cmd}'])
   
    def run_shell (self, msg, cmd):            
        self.msg (msg)
        run(['bash', '-c', f'source ~/.pyenv/versions/{self.project_path}/bin/activate && {cmd}'])
   
    def confirm (self, text):
        return Confirm.ask(f'[cyan][{self.LABEL}][/cyan] [yellow]{text}[/yellow]')

    def ask (self, text, default):
        return Prompt.ask(f'[cyan][{self.LABEL}][/cyan] [yellow]{text}[/yellow]', default=default)

    def warn (self, text):
        print (f'[cyan][{self.LABEL}][/cyan] [yellow]{text}[/yellow]')
        
    def msg (self, text):
        print (f'[cyan][{self.LABEL}][/cyan] [blue]{text}[/blue]')
        
    def error (self, text):
        print (f'[cyan][{self.LABEL}][/cyan] [red]Error: {text}[/red]')        
        print ()
        exit (1)
        
    def get_js_components (self, project):
        try:
            for file in (Path(project) / 'client' / 'node_modules').iterdir():
                if file.is_dir():
                    name = file.as_posix().split('/')[-1]
                    if name.startswith('orbit-component-'):
                        yield name
        except FileNotFoundError:
            pass

    def get_py_components (self, project):
        path = Path(f'~/.pyenv/versions/{self.project_path}/lib/python{version_info.major}.{version_info.minor}/site-packages').expanduser()
        for p in path.glob('orbit_component_*'):
            name = str(p).split('/')[-1].split('-')[0].split('.')[0]
            yield name.replace('_', '-')
        
    def resolve_components (self, project):
        js_components = set([component for component in self.get_js_components(project)])
        py_components = set([component for component in self.get_py_components(project)])
        return (js_components, py_components)

