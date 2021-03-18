# -*- mode: python ; coding: utf-8 -*-
from distutils.core import setup, Extension
from setuptools import sandbox
import sys

if not ( sys.version_info[0] == 3 and sys.version_info[1] <= 7 ):
    print("Supported Python 3.8 only!")
    raise Exception("Must be using Python 3")

buildUtility = False
buildBinaries = True
buildUI = False

block_cipher = None

if buildUI:
    a = Analysis(['Main.py'],
                 pathex=['E:\\Freelance\\Bochkov\\CRISPResso2UI'],
                 binaries=[],
                 datas=[],
                 hiddenimports=[],
                 hookspath=[],
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
              [],
              exclude_binaries=True,
              name='CRISPRessoUI',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=True )
    
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   upx_exclude=[],
                   name='CRISPRessoUI')
if buildBinaries:
    sandbox.run_setup('E:\\Freelance\\Bochkov\\CRISPResso2UI\\CRISPResso2\\setup_pyx.py', ['build_ext', '--inplace'])

if buildUtility:

    added_files = [
        ( 'CRISPResso2/CRISPResso2/EDNAFULL', 'CRISPResso2' ),
        ( 'CRISPResso2/CRISPResso2/templates', 'CRISPResso2/templates' ),
        ( 'flash.exe', '.' ),
        ( 'dist/CRISPRessoUI/CRISPRessoUI.exe', '.' ),
        ( 'CRISPResso2/trimmomatic.jar', '.' ),
        ( 'CRISPResso2/adapters', 'adapters' ),
    ]

    a = Analysis(['CRISPResso2\\CRISPResso.py'],
                 pathex=['E:\\Freelance\\Bochkov\\CRISPResso2UI', 'E:\\Freelance\\Bochkov\\CRISPResso2UI\\CRISPResso2'],
                 binaries=[],
                 datas=added_files,
                 hiddenimports=[],
                 hookspath=[],
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
              [],
              exclude_binaries=True,
              name='CRISPResso',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=True )

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   upx_exclude=[],
                   name='CRISPResso')

