# -*- mode: python ; coding: utf-8 -*-
from pkgutil import iter_modules
datas = [('src/__main__.py', '.'), ('./nltk_data', 'nltk_data')]
block_cipher = None
static = [package_name for importer, package_name, _ in iter_modules() if 'orbit' in package_name]
static.append('loguru')
static.append('engineio.async_drivers.aiohttp')

print(f'Static Modules: {static}')

a = Analysis(['src/__main__.py'],
             pathex=['.'],
             binaries=[],
             datas=datas,
             hiddenimports=static,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='{{ project }}',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None )
