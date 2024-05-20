#!/usr/bin/env python3
"""
 ██████╗ ██████╗ ██████╗ ██╗████████╗    ██████╗██╗     ██╗
██╔═══██╗██╔══██╗██╔══██╗██║╚══██╔══╝   ██╔════╝██║     ██║
██║   ██║██████╔╝██████╔╝██║   ██║█████╗██║     ██║     ██║
██║   ██║██╔══██╗██╔══██╗██║   ██║╚════╝██║     ██║     ██║
╚██████╔╝██║  ██║██████╔╝██║   ██║      ╚██████╗███████╗██║
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝       ╚═════╝╚══════╝╚═╝"""
from orbit_cli.cli_main import Main
#
#   Banner from "figlet -w200 -f 'ansi-shadow'"
#
__version__ = "0.1.26"
#
#   Entry point when run as an installed package
#
def main ():
    Main(__doc__, __version__).run()
#
#   Entry point when testing
#
if __name__ == '__main__':
    main ()

