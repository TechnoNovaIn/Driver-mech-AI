import os
import sys
import shutil
import zipfile
import subprocess
import zlib
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "app" / "src" / "main" / "assets"
BUILD_DIR = ROOT / "build" / "apk_pack"
OUTPUT_DIR = ROOT / "app" / "build" / "outputs" / "apk" / "debug"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOADS_DIR = Path(r"C:\Users\punee\Downloads")
BASE_APK = DOWNLOADS_DIR / "app-debug (1).apk"
if not BASE_APK.exists():
    BASE_APK = DOWNLOADS_DIR / "app-debug.apk"

import stat

print(f"Base APK: {BASE_APK}")
if not BASE_APK.exists():
    print("ERROR: Base APK not found!")
    sys.exit(1)

def on_rmtree_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

# Clean temp directory
if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR, onexc=on_rmtree_error)
BUILD_DIR.mkdir(parents=True, exist_ok=True)

UNPACK_DIR = BUILD_DIR / "unpacked"
UNPACK_DIR.mkdir(parents=True, exist_ok=True)

print("Extracting base APK...")
with zipfile.ZipFile(BASE_APK, "r") as z:
    for item in z.infolist():
        # Skip old signatures in META-INF
        if item.filename.startswith("META-INF/") and any(item.filename.endswith(ext) for ext in [".SF", ".RSA", ".DSA", ".MF"]) or item.filename == "META-INF/MANIFEST.MF":
            continue
        z.extract(item, UNPACK_DIR)

print("Injecting enhanced assets into unpacked APK...")
apk_assets_dir = UNPACK_DIR / "assets"
apk_assets_dir.mkdir(parents=True, exist_ok=True)

# Copy all assets
for asset_file in ASSETS_DIR.glob("*"):
    if asset_file.is_file() and asset_file.name != "preview.html":
        dest = apk_assets_dir / asset_file.name
        shutil.copy2(asset_file, dest)
        print(f" - Injected asset: {asset_file.name} ({asset_file.stat().st_size} bytes)")

# Ensure classes3.dex has 100% valid checksum and SHA-1 signature
dex_path = UNPACK_DIR / "classes3.dex"
if dex_path.exists():
    dex_bytes = bytearray(dex_path.read_bytes())
    wipe_target = b"try{localStorage.removeItem('mahindra_secure_token_v1');localStorage.removeItem('mahindra_secure_user_v1');localStorage.removeItem('mahindra_user_role_v2');}catch(e){};"
    if wipe_target in dex_bytes:
        safe_repl = b"/* mahindra driver guide session: preserve active login state */".ljust(len(wipe_target), b" ")
        dex_bytes = bytearray(dex_bytes.replace(wipe_target, safe_repl, 1))
        print(" - Neutralized destructive session wipe in classes3.dex")
    
    # Always recompute file size, SHA-1 signature, and Adler32 checksum
    dex_bytes[32:36] = len(dex_bytes).to_bytes(4, 'little')
    dex_bytes[12:32] = hashlib.sha1(dex_bytes[32:]).digest()
    dex_bytes[8:12] = (zlib.adler32(dex_bytes[12:]) & 0xffffffff).to_bytes(4, 'little')
    dex_path.write_bytes(dex_bytes)
    print(" - Recomputed classes3.dex SHA-1 signature and Adler32 checksum successfully")

# Validate all DEX files in unpack dir
for dex_file in UNPACK_DIR.glob("*.dex"):
    data = dex_file.read_bytes()
    stored_ck = int.from_bytes(data[8:12], 'little')
    calc_ck = zlib.adler32(data[12:]) & 0xffffffff
    stored_sha = data[12:32]
    calc_sha = hashlib.sha1(data[32:]).digest()
    if stored_ck != calc_ck or stored_sha != calc_sha:
        raise RuntimeError(f"FATAL: DEX integrity check failed for {dex_file.name}")
    print(f" - Verified DEX integrity: {dex_file.name} (Valid Checksum & SHA-1)")

UNALIGNED_APK = BUILD_DIR / "unaligned.apk"
print(f"Creating unaligned APK: {UNALIGNED_APK}...")
with zipfile.ZipFile(UNALIGNED_APK, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(UNPACK_DIR):
        for f in files:
            full_path = Path(root) / f
            arc_name = full_path.relative_to(UNPACK_DIR).as_posix()
            # Uncompressed for certain files as per Android spec (e.g. .so, resources.arsc)
            if arc_name == "resources.arsc" or arc_name.endswith(".so"):
                z.write(full_path, arc_name, compress_type=zipfile.ZIP_STORED)
            else:
                z.write(full_path, arc_name, compress_type=zipfile.ZIP_DEFLATED)

ZIPALIGN = Path(r"C:\Users\punee\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe")
APKSIGNER = Path(r"C:\Users\punee\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat")
KEYTOOL = Path(r"C:\Program Files\Java\jdk-24\bin\keytool.exe")

KEYSTORE = BUILD_DIR / "debug.keystore"
if not KEYSTORE.exists():
    print("Generating debug keystore...")
    gen_cmd = [
        str(KEYTOOL),
        "-genkeypair",
        "-v",
        "-keystore", str(KEYSTORE),
        "-storepass", "android",
        "-alias", "androiddebugkey",
        "-keypass", "android",
        "-keyalg", "RSA",
        "-keysize", "2048",
        "-validity", "10000",
        "-dname", "CN=Mahindra BSVI Driver Guide AI, OU=Fleet, O=Mahindra, L=Bengaluru, ST=Karnataka, C=IN"
    ]
    subprocess.run(gen_cmd, check=True)

ALIGNED_APK = BUILD_DIR / "aligned.apk"
print(f"Zipaligning APK using {ZIPALIGN}...")
subprocess.run([str(ZIPALIGN), "-p", "-f", "4", str(UNALIGNED_APK), str(ALIGNED_APK)], check=True)

# Verify zipalign
print(f"Verifying zip alignment...")
subprocess.run([str(ZIPALIGN), "-c", "4", str(ALIGNED_APK)], check=True)

print(f"Signing APK using {APKSIGNER}...")
sign_cmd = [
    str(APKSIGNER),
    "sign",
    "--ks", str(KEYSTORE),
    "--ks-pass", "pass:android",
    "--ks-key-alias", "androiddebugkey",
    "--key-pass", "pass:android",
    "--v1-signing-enabled", "true",
    "--v2-signing-enabled", "true",
    str(ALIGNED_APK)
]
subprocess.run(sign_cmd, check=True)

print("Verifying signed APK...")
verify_cmd = [str(APKSIGNER), "verify", "--verbose", str(ALIGNED_APK)]
subprocess.run(verify_cmd, check=True)

# Copy final APK to target destinations
FINAL_APK_PROJECT = OUTPUT_DIR / "Mahindra-BSVI-Driver-Guide-AI-final.apk"
FINAL_APK_DOWNLOADS = DOWNLOADS_DIR / "Mahindra-BSVI-Driver-Guide-AI-final.apk"
FINAL_APK_DESKTOP = Path(r"c:\Users\punee\OneDrive\Desktop\Driver mech\Mahindra-BSVI-v2.0.0-Latest-Final.apk")
FINAL_APK_VERSIONS = ROOT / "APK_Versions" / "Mahindra-BSVI-v2.0.0-Latest-Final.apk"

shutil.copy2(ALIGNED_APK, FINAL_APK_PROJECT)
shutil.copy2(ALIGNED_APK, FINAL_APK_DOWNLOADS)
shutil.copy2(ALIGNED_APK, FINAL_APK_DESKTOP)
shutil.copy2(ALIGNED_APK, FINAL_APK_VERSIONS)

print("=========================================================")
print(f"SUCCESS! Final APK packaged, aligned, signed, and verified:")
print(f"1. Workspace Desktop Path: {FINAL_APK_DESKTOP}")
print(f"2. Downloads Path:         {FINAL_APK_DOWNLOADS}")
print(f"3. Project Output Path:    {FINAL_APK_PROJECT}")
print(f"Size: {FINAL_APK_DESKTOP.stat().st_size:,} bytes")
print("=========================================================")
