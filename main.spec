# -*- mode: python ; coding: utf-8 -*-
from distutils.core import setup, Extension
from setuptools import sandbox

buildUtility = False
buildUI = True

block_cipher = None

if buildUtility:
    sandbox.run_setup('E:\\Freelance\\Bochkov\\CRISPResso2UI\\CRISPResso2\\setup_pyx.py', ['build_ext', '--inplace'])

    a = Analysis(['CRISPResso2\\CRISPResso.py'],
                 pathex=['E:\\Freelance\\Bochkov\\CRISPResso2UI\\CRISPResso2'],
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

#python CRISPResso.py -r1 E:\Freelance\Bochkov\9i_508__adapters_trimmed__paired_R1.fastq -r2 E:\Freelance\Bochkov\9i_508__adapters_trimmed__paired_R2.fastq -a TGGAGCCTTCAGAGGGTAAAATTAAGCACAGTGGAAGAATTTCATTCTGTTCTCAGTTTTCCTGGATTATGCCTGGCACCATTAAAGAAAATATCATTGGTGTTTCCTATGATGAATATAGATACAGAAGCGTCATCAAAGCATG -g ACCATTAAAGAAAATATCAT -amas 60 -e TGGAGCCTTCAGAGGGTAAAATTAAGCACAGTGGAAGAATTTCATTCTGTTCTCAGTTTTCCTGGATTATGCCTGGCACCATTAAAGAAAATATCATCTTTGGTGTTTCCTATGATGAATATAGATACAGAAGCGTCATCAAAGCATG -q 0 -s 0 --min_bp_quality_or_N 0 -n Experiment0002 -o Experiments\Experiment0002 -w 1 -wc -3 --exclude_bp_from_left 15 --exclude_bp_from_right 15
#CRISPResso.exe -r1 E:\Freelance\Bochkov\9i_508__adapters_trimmed__paired_R1.fastq -r2 E:\Freelance\Bochkov\9i_508__adapters_trimmed__paired_R2.fastq -a TGGAGCCTTCAGAGGGTAAAATTAAGCACAGTGGAAGAATTTCATTCTGTTCTCAGTTTTCCTGGATTATGCCTGGCACCATTAAAGAAAATATCATTGGTGTTTCCTATGATGAATATAGATACAGAAGCGTCATCAAAGCATG -g ACCATTAAAGAAAATATCAT -amas 60 -e TGGAGCCTTCAGAGGGTAAAATTAAGCACAGTGGAAGAATTTCATTCTGTTCTCAGTTTTCCTGGATTATGCCTGGCACCATTAAAGAAAATATCATCTTTGGTGTTTCCTATGATGAATATAGATACAGAAGCGTCATCAAAGCATG -q 0 -s 0 --min_bp_quality_or_N 0 -n Experiment0002 -o Experiments\Experiment0002 -w 1 -wc -3 --exclude_bp_from_left 15 --exclude_bp_from_right 15
