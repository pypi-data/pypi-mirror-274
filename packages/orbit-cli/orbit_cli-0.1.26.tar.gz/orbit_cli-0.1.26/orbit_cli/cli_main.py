from argparse import ArgumentParser
from rich.console import Console
from rich import print
from orbit_cli.cli_application import Application
from orbit_cli.cli_common import Common
from pathlib import Path


class Main:

    def __init__ (self, banner, version):
        print(f'[blue]{ banner }[/blue]')
        print(f'[blue]=>[/blue][magenta] Mad Penguin Consulting Ltd (c) 2023 (MIT License)[/magenta] [blue]v{version}[/blue]')
        print()
        path = Path('~/.bash_profile').expanduser()
        if not path.exists():
            with open(str(path), 'w') as io:
                io.write('#!/usr/bin/env bash\n')

    # FIXME: strip trailing "/" from project name"
    def run (self):       
        try:
            parser = ArgumentParser ()
            parser.add_argument ("--init",        type=str, metavar="TYPE", help="Specify whether we're working with an 'application' or 'component'")
            parser.add_argument ("--update",      type=str, metavar="PROJECT", help="Update main.js based on currently installed components")
            parser.add_argument ("--build",       type=str, metavar="PROJECT", help="Build a .DEB intaller for the specified project")
            parser.add_argument ("--list",        type=str, metavar="PROJECT", help="List installed components")
            parser.add_argument ("--add",         type=str, metavar='PROJECT', help="Add new components")
            parser.add_argument ("--rem",         type=str, metavar='PROJECT', help="Remove installed components")
            parser.add_argument ("--components",  type=str, nargs='*', metavar=('COMPONENTS'), help="Components to operate on")
            parser.add_argument ("--populate",    type=str, metavar="PROJECT", help="Download sample data into project folder from sample API")
            parser.add_argument ("--reset",       action='store_true', help="Remove and reinstall all tools [pyenv, nvm etc]")
            parser.add_argument ("--local-pypi",  type=str, metavar='REPO', help='Local PYPI repository')
            parser.add_argument ("--local-npm",   type=str, metavar='REGISTRY', help='Address of local NPM registry')
            parser.add_argument ("--upgrade",     action='store_true', help='Upgrade the orbit_cli code to the latest version via PIP')
            application = Application(args := parser.parse_args ())
            if   args.init:         application.component_create ()
            elif args.update:       application.component_update ()
            elif args.build:        application.component_build ()
            elif args.list:         application.component_list ()
            elif args.rem:          application.component_remove ()
            elif args.add:          application.component_add ()
            elif args.populate:     application.component_populate ()
            elif args.reset:        Common(args).reset()
            elif args.upgrade:      application.component_upgrade ()
            else:
                print ('No action specified!\n')
        except KeyboardInterrupt:
            pass
        except Exception:
            Console().print_exception(show_locals=True)
