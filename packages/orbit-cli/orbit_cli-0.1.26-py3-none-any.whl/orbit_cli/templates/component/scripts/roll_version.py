#!/usr/bin/env python3
from json import loads, dumps

VERSION_FILE = '.version'

with open(VERSION_FILE) as io:
    version = loads(io.read())
    
version['sub'] += 1
with open(VERSION_FILE, 'w') as io:
    io.write(dumps(version, indent=4))


def Process(filename, label, quoted=False, comma=False):
    with open(filename) as io:
        text = io.read()
        lines = text.split("\n")
        output = []
        for line in lines:
            if line.startswith(label):
                line = f"""{label} {'"' if quoted else ''}{version["major"]}.{version["minor"]}.{version["sub"]}{'"' if quoted else ''}{',' if comma else ''}"""
            output.append(line)

    with open(filename, 'w') as io:  
        io.write("\n".join(output))
        
def Replace (infile, outfile, token):
    new_version = f'{version["major"]}.{version["minor"]}.{version["sub"]}'
    with open(infile) as src:
        with open(outfile, 'w') as dst:
            dst.write(src.read().replace(token, new_version))

Process('apt/DEBIAN/control', 'Version:')
Process('server/pyproject.toml', 'version =', True)
Process('client/package.json', '  "version":', True, True)
Process('server/src/version.py', '__version__ =', True)
print(f'Updated to: {version["major"]}.{version["minor"]}.{version["sub"]}')
with open('scripts/VERSION', 'w') as io:
    io.write(f'{version["major"]}.{version["minor"]}.{version["sub"]}')
