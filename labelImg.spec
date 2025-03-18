# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

a = Analysis(
    ['labelImg.py'],
    pathex=[],
    binaries=[],
    datas=[('libs', 'libs'), ('resources_rc.py', '.')],
    hiddenimports=['PyQt5'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

version = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    u'040904B0',
                    [
                        StringStruct(u'CompanyName', u'Khiem Tran'),
                        StringStruct(u'FileDescription', u'LabelImg Application'),
                        StringStruct(u'FileVersion', u'1.0.0.0'),
                        StringStruct(u'InternalName', u'labelImg'),
                        StringStruct(u'LegalCopyright', u'Copyright (C) 2025 Khiem Tran'),
                        StringStruct(u'OriginalFilename', u'labelImg.exe'),
                        StringStruct(u'ProductName', u'LabelImg'),
                        StringStruct(u'ProductVersion', u'1.0.0.0')
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
    ]
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='labelImg',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\icons\\app.png'],
    version=version
)
