# -*- mode: python -*-
a = Analysis(['pong.py'],
             pathex=['/home/hbq/code/programming/python/pong'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pong',
          debug=False,
          strip=None,
          upx=True,
          console=True )
