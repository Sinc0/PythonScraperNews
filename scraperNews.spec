from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path

a = Analysis(['scraperNews.py'],
             pathex=['C:\\Users\\tempUser\\Desktop\\tempFolder\\pythonScraperNews'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('Code\pythonScraperNews.kv', 'C:\\Users\\tempUser\\Desktop\\tempFolder\\pythonScraperNews\\pythonScraperNews.kv', 'DATA')]

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='scraperNews',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

coll = COLLECT(exe, 
               Tree('C:\\Users\\tempUser\\Desktop\\tempFolder\\pythonScraperNews\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='scraperNews')