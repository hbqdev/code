# -*- mode: python -*-
a = Analysis(['particle.py'],
             pathex=['/Users/tintran/personal/code/programming/python/particle'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='particle',
          debug=False,
          strip=None,
          upx=True,
          console=True )
