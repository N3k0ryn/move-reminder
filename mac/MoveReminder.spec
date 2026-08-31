# -*- mode: python ; coding: utf-8 -*-
# Build this spec on macOS:  python3 -m PyInstaller --noconfirm --clean MoveReminder.spec

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Move Reminder",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Move Reminder",
)
app = BUNDLE(
    coll,
    name="Move Reminder.app",
    icon=None,
    bundle_identifier="com.movereminder.app",
    info_plist={
        "CFBundleName": "Move Reminder",
        "CFBundleDisplayName": "Move Reminder",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSUIElement": True,
    },
)
