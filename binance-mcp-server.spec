# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/binance_context_server/server.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'dateparser',
        'dateparser.data',
        'python_binance',
        'binance',
        'pandas_ta',
        'numba',
        'llvmlite',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='binance-mcp-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)