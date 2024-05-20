from pathlib import Path
from shutil import copyfile
from rich.console import Console
from rich.table import Table
from orbit_cli.cli_common import Common
from json import dump
from requests import get as requests_get
from urllib.parse import urlparse


class Application (Common):
            
    def configure_component (self):
        self.msg ('Creating folders ...')
        server_src = f'server/orbit_component_{self.project}/'
        for path in [
            'client/src/stores',
            'client/src/widgets',
            'client/src/views',
            'server/scripts',
            'scripts',
            f'{server_src}/schema']:
                self.ensure_folder(self.project_path, path)
        self.install ('README.md')
        self.install ('Makefile')
        self.install ('.gitignore')
        self.install ('.version')
        self.install ('server/README.md'        , 'server')
        self.install ('server/pyproject.toml'   , 'server')
        self.install ('server/Makefile'         , 'server')
        self.install ('server/__init__.py'      , f'{server_src}')
        self.install ('server/plugin.py'        , f'{server_src}')
        self.install ('server/MyTable.py'       , f'{server_src}/schema')    
        self.install ('scripts/roll_version.py' , 'scripts', chmod=0o755)
        self.install ('client/Makefile'         , 'client')
        self.install ('client/package.json'     , 'client')       
        self.install ('client/vite.config.js'   , 'client')
        self.install ('client/index.js'         , 'client')
        self.install ('client/menu.js'          , 'client')
        self.install ('client/main.vue'         , f'client/src/{self.project}.vue', full=True)
        # self.install ('client/mainComponent.vue', f'client/src/{self.project}Component.vue', full=True)
        self.install ('client/mytableStore.js'  , 'client/src/stores')    

    def configure_application (self):
        self.msg ('Creating folders ...')
        for path in [
            'apt/etc/systemd/system',
            'apt/usr/local/bin',
            'apt/DEBIAN',
            f'apt/opt/{self.project}/scripts',
            f'apt/opt/{self.project}/web/assets',
            'client/public',
            'client/src/assets',
            'client/src/components',
            'client/src/views',
            'scripts',
            'server/src',
            'server/scripts']:
                self.ensure_folder(self.project, path)
        self.install ('README.md')
        self.install ('Makefile')
        self.install ('.gitignore')
        self.install ('.version')
        self.install ('server/README.md'       , 'server')
        self.install ('server/pyproject.toml'  , 'server')
        self.install ('server/orbit.spec'      , 'server')
        self.install ('server/Makefile'        , 'server')
        self.install ('server/__main__.py'     , 'server/src')
        self.install ('server/version.py'      , 'server/src')
        self.install ('server/make_keys.sh'    , 'server/scripts')
        self.install ('apt/DEBIAN/control'     , 'apt/DEBIAN')
        self.install ('apt/DEBIAN/postinst'    , 'apt/DEBIAN', chmod=0o755)
        self.install ('apt/etc/systemd/system/project.service' , f'apt/etc/systemd/system/{self.project}.service', full=True)
        self.install ('apt/opt/service/scripts/make_keys.sh' , f'apt/opt/{self.project}/scripts', chmod=0o755)
        self.install ('scripts/roll_version.py', 'scripts', chmod=0o755)
        self.install ('client/index.html'      , 'client')
        self.install ('client/Makefile'        , 'client')
        self.install ('client/package.json'    , 'client')       
        self.install ('client/vite.config.js'  , 'client')
        self.install ('client/App.vue'         , 'client/src')
        self.install ('client/main.js'         , 'client/src')
        self.install ('client/main.css'        , 'client/src/assets')
        self.install ('common/orbit-logo.png'  , 'client/src/assets', binary=True)
        self.install ('common/favicon.ico'     , 'client/public', binary=True)
                
    def ensure_folder (self, project, path):
        if Path(path).exists():
            return self.warn (f'Already exists: {path}')
        self.msg (f'Creating folder: {path}')
        (Path(project) / path ).mkdir(parents=True)
        
    def install (self, src, dst='.', full=False, binary=False, force=False, chmod=None):
        name = src.split('/')[-1]
        self.msg (f'Installing [bold]{name}[/bold] in [bold]{dst}[/bold]')
        target = f'{self.project_path}/{dst}/{name}' if not full else f'{self.project_path}/{dst}'
        if Path(target).exists() and not force:
            return self.warn (f'Skipped: [bold]{target}[/bold] - already exists!')    
        source = f'{self._templates}/{self.project_type}/{src}'
        if not Path(source).exists():
            return self.warn (f'Skipped: [bold]{source}[/bold] - template is MISSING!')
        if binary:
            with open(target, 'wb') as out:
                with open(source, 'rb') as inp:
                    out.write(inp.read())
        else:
            with open(target, 'w') as io:
                io.write (self._env.get_template(f'{self.project_type}/{src}').render(self._vars))
        if chmod:
            Path(target).chmod(chmod)

    def component_update (self):
        if not self.project:
            self._vars['project'] = self._args.update
        if not Path(self.project_path) or not Path(self.project_path).is_dir():
            self.error (f"Can't see project: {self.project_path}")
        self.manage_local_repos()
        self.msg (f'Running [bold]update_components[/bold] for project [bold]{self.project}[/bold]')
        self.install ('common/fonts.txt', 'client/src/components/fonts.template', full=True, force=True)  
        components = set(self.get_js_components(self.project_path))
        if 'orbit-component-shell' not in components:
            components.add('orbit-component-shell')
        if 'orbit-component-base' in components:            
            components.remove('orbit-component-base')

        installed = []
        for component in components:
            name = component[16:]
            src = Path(f'{self.project_path}/client/node_modules/{component}/menu.js')
            dst = Path(f'{self.project_path}/client/src/components/{name}.js.template')
            copyfile (src, dst)
            
            if Path(f'{self.project}/client/src/components/{name}.js').exists():
                installed.append((component.replace('-', '_'), f'@/components/{name}.js'))
            else:
                installed.append((component.replace('-', '_'), f'@/../node_modules/{component}/menu.js'))
                
        if not (src := Path(f'{self.project_path}/client/src/components/fonts.txt')).exists():
            src = f'{self._templates}/{self.project_type}/common/fonts.txt'
        fonts = []
        with open(src) as io:
            while line := io.readline():
                fonts.append(line.split('\n')[0])
                
        self._vars['fonts'] = fonts
        self._vars['components'] = installed
        self.install ('client/main.js', 'client/src', force=True)
        
    def component_build (self):
        self._vars['project'] = self._args.build
        self.shell(
            f'Build a .DEB installer for [bold]{self._args.build}[/bold] >>>>',
            f'cd {self.project_path} && make build_deb')
        self.msg ('<<<<')

    def component_list (self):
        self._vars['project'] = self._args.list
        js_components, py_components = self.resolve_components(self.project)
        tab = Table(min_width=50)
        for field in ['Idx', 'Name', 'Front-End', 'Back-End']:
            tab.add_column(field, style='cyan', header_style='deep_sky_blue4', no_wrap=True)
        for (idx, name) in enumerate(py_components | js_components):
            tab.add_row(
                str(idx),
                name,
                'installed' if name in js_components else '[magenta]none[/magenta]',
                'installed' if name in py_components else '[magenta]none[/magenta]'
            )
        Console().print(tab)

    def component_add (self):
        self.manage_local_repos()
        self._vars['project'] = self._args.add
        for component in self._args.components:
            self._vars['component'] = component
            self.msg (f"Adding component [bold]{self.component}[/bold] to [bold]{self.project}[/bold]")
            js_components, py_components = self.resolve_components(self.project)
            if self.component not in js_components:
                # registry = f'--registry={self._args.local_npm} --force' if self._args.local_npm else ""
                self.call_shell(
                    f'Installing JS component [bold]{self.component}[/bold] >>>>',
                    f'cd {self.project_path}/client && npm install {self.component}')
                    # f'cd {self.project_path}/client && npm install {self.component};npm run build')
                self.msg ('<<<<')
            else:
                self.msg ('[red]already installed[/red]')
            if self.component not in py_components:
                if self.component:
                    self.run_shell(
                        f'Installing PY component [bold]{self.component}[/bold] >>>>',
                        f'cd {self.project_path}/server && poetry add {self.component}')
                    self.msg ('<<<<')
            else:
                self.msg ('[red]already installed[/red]')
        self.component_update ()
        self.msg ('Complete.')

    def component_remove (self):
        self._vars['project'] = self._args.rem
        for component in self._args.components:
            self._vars['component'] = component
            self.msg (f"Removing component [bold]{self.component}[/bold] from [bold]{self.project}[/bold]")
            js_components, py_components = self.resolve_components(self.project)
            if self.component in js_components:
                self.run_shell(
                    f'Removing JS component [bold]{self.component}[/bold] >>>>',
                    f'cd {self.project_path}/client;npm uninstall {self.component}')
                self.msg ('<<<<')
            else:
                self.msg ('[red]not installed[/red]')            
            if self.component in py_components:
                self.run_shell(
                    f'Removing PY component [bold]{self.component}[/bold] >>>>',
                    f'cd {self.project_path}/server && poetry add {self.component}')
                self.msg ('<<<<')
            else:
                self.msg ('[red]not installed[/red]')            
        self.component_update ()
        self.msg ('Complete.')

    def create_project (self, project):
        if not self.confirm (f'Create project [bold]{project}[/bold]?'):
            self.error ('Aborted!')
        if self.project_type == 'application':
            project_path = project
        else:
            project = project.replace('-', '_')
            project_path = f"orbit-component-{project}"
        if Path(project_path).mkdir():
            self.error ('Unable to create the project!')
        self.call_shell(
            f'Creating virtual env [project_path]',
            f'pyenv virtualenv {project_path}')
        return project_path
    
    def collect_project_information (self):
        self.msg ('Collecting project information...')
        while True:
            project = self.ask('Enter your project name', 'my-demo-project' if self.project_type == 'application' else 'mycomp')
            if not Path(project).exists():
                break
            self.msg ('[red]Project folder already exists![/red]')
        self._vars['project'] = project
        self._vars['description'] = self.ask('Enter your project description', 'Just an example Orbit application' if self.project_type == 'application' else 'A Demo Component')
        self._vars['author'] = self.ask('Enter your name (project author)', 'John Doe')
        self._vars['email'] = self.ask('Enter your email address (bugs email)', 'support@madpenguin.uk')
        self._vars['url'] = self.ask('Enter your project home page', 'https://linux.uk')
        self._vars['project_path'] = self.create_project(project)

    def manage_local_repos (self):
        if self._args.local_npm:
            self.call_shell(
                f'Setting local NPM registry to: {self._args.local_npm}',
                f'cd {self.project_path}/client && npm config set registry {self._args.local_npm} && npm config set legacy-peer-deps true')
        if self._args.local_pypi:
            host = urlparse(self._args.local_pypi).netloc.split(':')[0]
            self.run_shell(
                f'Setting local PYPI registry to: {self._args.local_pypi}',
                f'cd {self.project_path}/server && pip config --user set global.index-url {self._args.local_pypi} && pip config --user set global.trusted-host {host}')
            self.run_shell(
                f'Setting local Poetry registry to: {self._args.local_pypi}',
                f"""
                    cd {self.project_path}/server &&\n
                    poetry source add borg {self._args.local_pypi} --priority="primary" &&\n
                    poetry source add pypi --priority="supplemental"
                """)

    # def repo_create (self):
    #     self.shell(
    #         f'Installing local Python REPOSITORY [bold]{self._args.local_repo[0]}[/bold] >>>>',
    #         f"""
    #             cd {self.project_path}/server &&\n
    #             poetry source add {self._args.local_repo[0]} {self._args.local_repo[1]} --priority="primary" &&\n
    #             poetry source add pypi --priority="supplemental"
    #         """)
   
    def component_install_nltk (self):
        self.run_shell(
            f'Installing NLTK for FTX indexing ...',
            f"""cd {self.project_path}/server && python -c 'import nltk;nltk.download("stopwords");nltk.download("punkt")' """)

    def component_create (self):
        self.ensure_tools()
        self.collect_project_information ()
        self.ensure_poetry()
        if self.project_type == 'application':
            self.configure_application()
        elif self.project_type == 'component':
            self.configure_component()
        else:
            self.error ('unknown type, must be application or component')
        self.manage_local_repos()
        # registry = f'--registry={self._args.local_npm} --force' if self._args.local_npm else ""
        self.call_shell(
            f'Installing JS components >>>>',
            f'cd {self.project_path}/client;npm install')
        self.msg ('<<<<')
        # if self._args.local_repo:
        #     self.repo_create ()
        self.run_shell(
            f'Installing PY components >>>>',
            f'cd {self.project_path}/server && poetry install')
        self.msg ('<<<<')
        if self.project_type == 'application':
            self.component_install_nltk()
            self.component_update ()
        self.msg ('Complete.')

    def component_populate (self):
        self._vars['project'] = self._args.populate
        self.msg (f'Populating [bold]{self.project}[/bold] data')
        r = requests_get(f'https://swapi.dev/api/')
        if r.status_code != 200:
            self.error (f'unable to read remote table [code={r.status_code}]')
        for table in r.json():
            self.msg (f'Processing [bold]{table}[/bold] ...')
            count = 0
            page = 1
            with open(f'{self.project}/demo_data_{table}.json', 'w') as io:
                io.write('{\n')
                while True:
                    r = requests_get(f'https://swapi.dev/api/{table}?page={page}')
                    if r.status_code != 200:
                        self.error (f'problem reading page: {page} for {table}')
                    json = r.json()
                    self.msg (f'=> {page}...')
                    for result in json['results']:
                        if count: io.write(',\n')
                        io.write(f'  "{count}": ')
                        dump(result, io)
                        count += 1
                    if not json['next']:
                        break
                    page += 1
                io.write('\n}\n')
                break
        self.msg ('Complete')
        
    def component_upgrade (self):
        if not self.confirm (f'Upgrade [bold]ORBIT_CLI[/bold] via PIP?'):        
            self.error ('Aborted!')
        self.call_shell(
            f'Running "pip -q install --upgrade orbit-cli"',
            f'pip -q install --upgrade orbit-cli')
        self.msg ('Complete')
