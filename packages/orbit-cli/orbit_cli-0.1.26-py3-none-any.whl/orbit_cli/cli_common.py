from requests import get as requests_get
from pathlib import Path
from shutil import which
from tempfile import NamedTemporaryFile
from subprocess import call as call_process
from orbit_cli.cli_utils import Utils


class Common (Utils):

    PYENV = 'export PATH="$PATH:$HOME/.pyenv/bin:$HOME/.local/bin"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"\n'
    NVENV = 'export NVM_DIR="$HOME/.nvm"\n[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"\n[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"\n'
    PYENV_INSTALLER = 'https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer'
    NVM_INSTALLER = 'https://raw.githubusercontent.com/creationix/nvm/master/install.sh'
       
    def reset (self):
        yn = self.confirm ('This will [bold]REMOVE[/bold], pyenv, nvm, npm, poetry etc from this users profile, are you sure?')
        if not yn:
            self.error (f'Nothing to do here!')
        with NamedTemporaryFile(suffix='.sh', mode='w') as io:
            io.write('#!/usr/bin/env bash\n')
            io.write('rm -rf .pyenv\n')
            io.write('rm -rf .nvm\n')
            io.write('rm -rf .npm\n')
            io.flush()
            call_process (['bash', io.name])
        path = Path('~/.bash_profile').expanduser()
        if path.exists():
            self.strip_from_file('~/.bash_profile', ['pyenv', 'NVM'])
        self.msg ('[red]Complete, please log out and in again![/red]')

    def ensure_tools (self):
        self.ensure_pyenv()
        self.ensure_nvm()
        self.ensure_npm()

    def ensure_pyenv (self):
        if not self.ensure('pyenv'):
            self.download_and_run('pyenv', self.PYENV_INSTALLER)
            self.add_to_file('~/.bash_profile', 'pyenv', self.PYENV)
            return False
        return True
           
    def ensure_nvm (self):
        if not self.ensure ('nvm'):
            self.download_and_run('nvm', self.NVM_INSTALLER)
            self.add_to_file('~/.bash_profile', 'nvm', self.NVENV)
            return False
        return True
       
    def ensure_npm (self):
        if not self.ensure('npm'):
            with NamedTemporaryFile(suffix='.sh', mode='w') as io:
                io.write('#!/usr/bin/env bash\n')
                io.write('source ~/.bash_profile\n')
                io.write('export NVM_DIR="$HOME/.nvm"\n')
                io.write('export PATH="$PATH:$HOME/.local/bin"\n')
                io.write('[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"\n')
                io.write('[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"\n')
                io.write('nvm install node\n')
                io.flush()
                call_process (['bash', io.name])
                return False
        return True
        
    def ensure_poetry (self):
        if not self.ensure('poetry', which('poetry')):
            result = self.shell(
                f'Installing [bold]Poetry[/bold] >>>>',
                f'pip install poetry')
            return False
        return True

    def ensure (self, name, test=None):        
        self.msg(f'Ensuring [bold]{name}[/bold] is set up ...')
        if test is None:
            test = Path(f'~/.{name}').expanduser().exists()
        if test:
            return True
        yn = self.confirm (f'Unable to locate [bold]{name}[/bold], would you like to install it?')
        if not yn:
            self.error (f'Unable to continue without [bold]{name}[/bold]')
        return False

    def download_and_run (self, name, url):
            self.msg (f'Downloading [bold]{name}[/bold] installer ...')
            result = requests_get(url)
            if result.status_code != 200:
                self.error ('Failed to download installer: [bold]{r.status_code}[/bold]')
            self.call (f'Running [bold]{name}[/bold] installer ...', result.text)

    def add_to_file (self, file_name: str, token: str, text: str):
        path = Path(file_name).expanduser()
        if path.exists():
            with open(path) as io:
                file = io.read()
        else:
            file = ''
        if token in file:
            self.warn (f'We already seem to have [bold]{token}[/bold] in .bash_profile, please check!')
            return
        with open(path, 'w') as io:
            io.write(file + text)

    def strip_from_file (self, file_name: str, tokens: list):
        path = Path(file_name).expanduser()
        with open(path) as io:
            lines = io.read().split('\n')
        output = []
        for line in lines:
            remove = False
            for token in tokens:
                if token in line:
                    remove = True
            if not remove:
                output.append(line)
        with open(path, 'w') as io:
            io.write('\n'.join(output))
            