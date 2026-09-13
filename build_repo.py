#!/usr/bin/env python3
import os
import json
import subprocess
import zipfile
import shutil
import time
import hashlib

PUBKEY_HEX = "308203563082023ea003020102020900e75370d5332c1275300d06092a864886f70d01010c05003058310b30090603550406130244453111300f060355040b13086d796664726f69643120301e060355040a13174a6572656d792042656e7a204f70656e20536f75726365311430120603550403130b4a6572656d792042656e7a3020170d3236303931313232303035375a180f32303534303132373232303035375a3058310b30090603550406130244453111300f060355040b13086d796664726f69643120301e060355040a13174a6572656d792042656e7a204f70656e20536f75726365311430120603550403130b4a6572656d792042656e7a30820122300d06092a864886f70d01010105000382010f003082010a0282010100b3d1616750eaec5dc7727e6eedcd0f91d36be900f281d2911aed17478288e620e35f6fb1ad4d375ffd9cb17114138b8e65c92fd193eade6b81734d6641f469d060bc5d1412ae31970c86dbc9c0157738bcffbcaf2ca27c6ef7c20541a16cd31d82f02d72b76c57ab401b7ae5b0beef305f2b6e5143825b043f1b8a006e660471e9b8d80c63398e731af3fd061f6196c67e0aa94d57f49e93651f386e139f87cf4c6c8c7a10cf60e4f85b2e370408fce069e3968c55a193b7db0b454ec9a0aa4d09b3f511117e43193537780743ee311d9dc54c0f5d77d4b3ef14d0d4d89c9c21c9d3fabbf0b9200f4e4c1e6304f0f709c7f855d58d8e051251588fa787b164f10203010001a321301f301d0603551d0e04160414c8a13d376a2d592629a2a20ff3ca22ef5645d263300d06092a864886f70d01010c05000382010100239aa935cfde82fddde0674f77fa06f313f60a2029e7615522ebd2af774b67462be13d635d19543223aa7994bf967999bea2c1c3d06353f669ba95c50e2a36b2403e2a4008c67ef8fc56fca17c4987a4cb271df2a4913fadf04fe7c207e9f6585fde5af121b4f32461093125364d33aa82476cbbba3ca7a1d7f33795ece862d270e28c71a34e1b86be0ecde493ae7f0d2fa222271bfbf952179dc29eabe477c0a17242a8ce6ccf61c0b6f53c2caaf35925740c11b4e7b6a3b6088eccca9ec78f446f06b83d0fc2ed1c1e8aed444afdb0097a536287d99af39ffc53ea78fd2d4f26b8c3992196d195380adfe61d505b1d24a3206ed92b1932614c56ee3837c3e5"
FINGERPRINT = "A2:AD:02:7C:85:6A:E9:E1:11:B1:7A:55:DF:53:03:BB:42:3D:BF:8D:44:7D:C9:81:BD:B0:E2:13:46:96:3C:B7"
FINGERPRINT_HEX = "a2ad027c856ae9e111b17a55df5303bb423dbf8d447dc981bdb0e21346963cb7"
KEYSTORE = "myfdroid.keystore"
KEYPASS = "myfdroid_secret_key_2026"

ts = int(time.time() * 1000)

# Repo Icon: JB Monogram Cover
with open("repo/icon.png", "rb") as f:
    repo_icon_bytes = f.read()
repo_icon_sha256 = hashlib.sha256(repo_icon_bytes).hexdigest()
repo_icon_size = len(repo_icon_bytes)

# App Icon: BenzStore
with open("repo/icons/com.benzjeremy.benzstore.png", "rb") as f:
    benzstore_icon_bytes = f.read()
benzstore_icon_sha256 = hashlib.sha256(benzstore_icon_bytes).hexdigest()
benzstore_icon_size = len(benzstore_icon_bytes)

# Read APK BenzStore v1.0 (Unified AppStore for Android & PC)
with open("repo/benzstore-v1.0.apk", "rb") as f:
    benzstore_v10_apk_bytes = f.read()
benzstore_v10_apk_sha256 = hashlib.sha256(benzstore_v10_apk_bytes).hexdigest()
benzstore_v10_apk_size = len(benzstore_v10_apk_bytes)

# BenzStore v1.1 APK
benzstore_v11_apk_sha256 = "121c48a9d0b62372375871ea24a4fe886e0283408be0eebe336227f23bc33af5"
benzstore_v11_apk_size = 620732

print(f"Repo Icon (JB): {repo_icon_size} bytes")
print(f"App Icon (BenzStore): {benzstore_icon_size} bytes")
print(f"APK BenzStore v1.0 (Native): sha256={benzstore_v10_apk_sha256}, size={benzstore_v10_apk_size}")

# 1. index-v2.json (F-Droid v2 Schema with localized maps & multi-version support)
index_v2_data = {
    "repo": {
        "name": {
            "de-DE": "Jeremy Benz F-Droid Repository",
            "en-US": "Jeremy Benz F-Droid Repository"
        },
        "description": {
            "de-DE": "Offizielles F-Droid-Repository zur Installation von BenzStore, dem einheitlichen AppStore für Android & PC.",
            "en-US": "Official F-Droid repository for bootstrapping BenzStore, the unified AppStore for Android & PC."
        },
        "icon": {
            "en-US": {
                "name": "/icons/icon.png",
                "sha256": repo_icon_sha256,
                "size": repo_icon_size
            }
        },
        "address": "https://benzjeremy.github.io/myfdroid/repo",
        "mirrors": [
            {
                "isPrimary": True,
                "url": "https://benzjeremy.github.io/myfdroid/repo"
            },
            {
                "url": "https://benzjeremy.github.io/myfdroid"
            }
        ],
        "timestamp": ts,
        "antiFeatures": {},
        "categories": {
            "System": {
                "name": {
                    "de-DE": "System",
                    "en-US": "System"
                }
            },
            "Utility": {
                "name": {
                    "de-DE": "Dienstprogramme",
                    "en-US": "Utility"
                }
            }
        }
    },
    "packages": {
        "com.benzjeremy.benzstore": {
            "metadata": {
                "added": ts,
                "lastUpdated": ts,
                "categories": [
                    "System",
                    "Utility"
                ],
                "name": {
                    "de-DE": "BenzStore",
                    "en-US": "BenzStore"
                },
                "summary": {
                    "de-DE": "Einheitlicher AppStore für Android & PC mit Version-Picker und SHA-256 Integrität",
                    "en-US": "Unified AppStore for Android & PC with version picker and SHA-256 integrity"
                },
                "description": {
                    "de-DE": "Offizieller, moderner AppStore für freie Android- und PC-Software von Jeremy Benz. Feed-Synchronisation via GitHub Content-Branch, Versionsauswahl (Latest oder spezifische Versionen) und kryptografische SHA-256 Integritätsprüfung vor der Installation.",
                    "en-US": "Official, modern AppStore for free Android and PC software by Jeremy Benz. Feed synchronization via GitHub content branch, version picker (latest or specific versions), and cryptographic SHA-256 integrity checks prior to installation."
                },
                "license": "GPL-3.0-or-later",
                "webSite": "https://benzjeremy.github.io/benzstore/",
                "sourceCode": "https://github.com/benzjeremy/benzstore",
                "issueTracker": "https://github.com/benzjeremy/benzstore/issues",
                "authorName": "Jeremy Benz",
                "authorEmail": "benzjeremy@pm.me",
                "authorWebSite": "https://benzjeremy.github.io/",
                "icon": {
                    "en-US": {
                        "name": "/icons/com.benzjeremy.benzstore.png",
                        "sha256": benzstore_icon_sha256,
                        "size": benzstore_icon_size
                    }
                },
                "preferredSigner": FINGERPRINT_HEX
            },
            "versions": {
                benzstore_v10_apk_sha256: {
                    "added": ts,
                    "file": {
                        "name": "/benzstore-v1.0.apk",
                        "sha256": benzstore_v10_apk_sha256,
                        "size": benzstore_v10_apk_size
                    },
                    "manifest": {
                        "versionName": "1.0",
                        "versionCode": 100,
                        "usesSdk": {
                            "minSdkVersion": 26,
                            "targetSdkVersion": 34
                        },
                        "signer": {
                            "sha256": [
                                FINGERPRINT_HEX
                            ]
                        },
                        "usesPermission": [
                            {
                                "name": "android.permission.INTERNET"
                            },
                            {
                                "name": "android.permission.REQUEST_INSTALL_PACKAGES"
                            },
                            {
                                "name": "android.permission.POST_NOTIFICATIONS"
                            }
                        ]
                    },
                    "whatsNew": {
                        "de-DE": "Release v1.0: Erste Edition des nativen Android AppStore Clients mit Feed-Synchronisation, Versionsauswahl und SHA-256 Integritätsprüfung.",
                        "en-US": "Release v1.0: Initial release of the native Android AppStore client featuring feed synchronization, version picker, and SHA-256 integrity checks."
                    }
                },
                benzstore_v11_apk_sha256: {
                    "added": ts,
                    "file": {
                        "name": "/benzstore-v1.1.apk",
                        "sha256": benzstore_v11_apk_sha256,
                        "size": benzstore_v11_apk_size
                    },
                    "manifest": {
                        "versionName": "1.1",
                        "versionCode": 110,
                        "usesSdk": {
                            "minSdkVersion": 26,
                            "targetSdkVersion": 34
                        },
                        "signer": {
                            "sha256": [
                                FINGERPRINT_HEX
                            ]
                        },
                        "usesPermission": [
                            {
                                "name": "android.permission.INTERNET"
                            },
                            {
                                "name": "android.permission.REQUEST_INSTALL_PACKAGES"
                            },
                            {
                                "name": "android.permission.POST_NOTIFICATIONS"
                            }
                        ]
                    },
                    "whatsNew": {
                        "de-DE": "Release v1.1: Fix: Cryptographic hash mismatch corrected; proper versioning workflow established",
                        "en-US": "Release v1.1: Fix: Cryptographic hash mismatch corrected; proper versioning workflow established"
                    }
                }
            }
        }
    }
}

v2_bytes = json.dumps(index_v2_data, indent=2).encode("utf-8")
with open("repo/index-v2.json", "wb") as f:
    f.write(v2_bytes)
v2_sha256 = hashlib.sha256(v2_bytes).hexdigest()
v2_size = len(v2_bytes)

# 2. entry.json (Points strictly to /index-v2.json for V2 clients)
entry_data = {
    "timestamp": ts,
    "version": 30000,
    "maxAge": 14,
    "index": {
        "name": "/index-v2.json",
        "sha256": v2_sha256,
        "size": v2_size,
        "numPackages": 1
    },
    "diffs": {}
}
with open("repo/entry.json", "w", encoding="utf-8") as f:
    json.dump(entry_data, f, indent=2)

# 3. index-v1.json (Kept for V1 clients with plain string fields)
index_v1_data = {
    "repo": {
        "name": "Jeremy Benz F-Droid Repository",
        "description": "Official F-Droid repository for bootstrapping BenzStore, the unified AppStore for Android & PC.",
        "icon": "icon.png",
        "address": "https://benzjeremy.github.io/myfdroid/repo",
        "timestamp": ts,
        "version": 20000,
        "pubkey": PUBKEY_HEX,
        "fingerprint": FINGERPRINT,
        "mirrors": [
            "https://benzjeremy.github.io/myfdroid/repo",
            "https://benzjeremy.github.io/myfdroid"
        ]
    },
    "requests": {
        "install": [],
        "uninstall": []
    },
    "apps": [
        {
            "packageName": "com.benzjeremy.benzstore",
            "name": "BenzStore",
            "summary": "Einheitlicher AppStore für Android & PC mit Version-Picker (v1.0)",
            "description": "Offizieller, moderner AppStore für freie Android- und PC-Software von Jeremy Benz. Feed-Synchronisation, Versionsauswahl und SHA-256 Integritätsprüfung.",
            "license": "GPL-3.0-or-later",
            "webSite": "https://benzjeremy.github.io/benzstore/",
            "sourceCode": "https://github.com/benzjeremy/benzstore",
            "issueTracker": "https://github.com/benzjeremy/benzstore/issues",
            "authorName": "Jeremy Benz",
            "authorEmail": "benzjeremy@pm.me",
            "authorWebSite": "https://benzjeremy.github.io/",
            "icon": "icons/com.benzjeremy.benzstore.png",
            "categories": [
                "System",
                "Utility"
            ],
            "antiFeatures": [],
            "suggestedVersionCode": "100"
        }
    ],
    "packages": {
        "com.benzjeremy.benzstore": [
            {
                "versionName": "1.0",
                "versionCode": 100,
                "size": benzstore_v10_apk_size,
                "apkName": "benzstore-v1.0.apk",
                "hash": benzstore_v10_apk_sha256,
                "hashType": "sha256",
                "minSdkVersion": 26,
                "targetSdkVersion": 34,
                "signer": FINGERPRINT_HEX,
                "added": ts
            }
        ]
    }
}
v1_bytes = json.dumps(index_v1_data, indent=2).encode("utf-8")
with open("repo/index-v1.json", "wb") as f:
    f.write(v1_bytes)

# 4. index.xml (Legacy XML)
xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<fdroid>
  <repo icon="icon.png" maxage="14" name="Jeremy Benz F-Droid Repository" pubkey="{PUBKEY_HEX}" url="https://benzjeremy.github.io/myfdroid/repo" timestamp="{int(ts/1000)}">
    <description>Official F-Droid repository for bootstrapping BenzStore, the unified AppStore for Android & PC.</description>
  </repo>
  <application id="com.benzjeremy.benzstore">
    <id>com.benzjeremy.benzstore</id>
    <added>2026-09-12</added>
    <lastupdated>2026-09-12</lastupdated>
    <name>BenzStore</name>
    <summary>Einheitlicher AppStore für Android & PC mit Version-Picker (v1.0)</summary>
    <icon>icons/com.benzjeremy.benzstore.png</icon>
    <desc>Offizieller, moderner AppStore für freie Android- und PC-Software von Jeremy Benz. Feed-Synchronisation, Versionsauswahl und SHA-256 Integritätsprüfung.</desc>
    <license>GPL-3.0-or-later</license>
    <category>System,Utility</category>
    <web>https://benzjeremy.github.io/benzstore/</web>
    <source>https://github.com/benzjeremy/benzstore</source>
    <tracker>https://github.com/benzjeremy/benzstore/issues</tracker>
    <marketversion>1.0</marketversion>
    <marketvercode>100</marketvercode>
    <package>
      <version>1.0</version>
      <versioncode>100</versioncode>
      <size>{benzstore_v10_apk_size}</size>
      <apkname>benzstore-v1.0.apk</apkname>
      <srcname>benzstore-v1.0.tar.gz</srcname>
      <hash type="sha256">{benzstore_v10_apk_sha256}</hash>
      <sig>{PUBKEY_HEX}</sig>
      <added>2026-09-12</added>
    </package>
  </application>
</fdroid>
"""
with open("repo/index.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

# 5. Sign JAR files
def make_and_sign_jar(jar_name, file_to_pack, internal_name):
    tmp_jar = "tmp_" + jar_name
    if os.path.exists(tmp_jar):
        os.remove(tmp_jar)
    with zipfile.ZipFile(tmp_jar, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(file_to_pack, arcname=internal_name)

    cmd = [
        "jarsigner",
        "-keystore", KEYSTORE,
        "-storepass", KEYPASS,
        "-keypass", KEYPASS,
        "-digestalg", "SHA-256",
        "-sigalg", "SHA256withRSA",
        tmp_jar,
        "myfdroid"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("jarsigner error:", res.stderr)
        raise RuntimeError("jarsigner failed")

    shutil.move(tmp_jar, os.path.join("repo", jar_name))
    print(f"Created & signed repo/{jar_name}")

make_and_sign_jar("index-v1.jar", "repo/index-v1.json", "index-v1.json")
make_and_sign_jar("index.jar", "repo/index.xml", "index.xml")
make_and_sign_jar("entry.jar", "repo/entry.json", "entry.json")

# 6. Mirror to root of repository
for fn in [
    "index-v2.json",
    "index-v1.json", "index-v1.jar",
    "index.xml", "index.jar",
    "entry.json", "entry.jar",
    "benzstore-v1.0.apk",
    "benzstore-v1.1.apk"
]:
    if os.path.exists(os.path.join("repo", fn)):
        shutil.copy2(os.path.join("repo", fn), fn)
        print(f"Copied {fn} to root")

if os.path.exists("repo/icons"):
    os.makedirs("icons", exist_ok=True)
    for ic in os.listdir("repo/icons"):
        shutil.copy2(os.path.join("repo/icons", ic), os.path.join("icons", ic))
    print("Mirrored repo/icons to root icons")

# Clean up any remaining learn/wetter files from root and icons if any exist
for stale in [
    "learn-v1.0.apk", "learn-v2.0.apk", "learn-v2.1.apk", "learn-v2.2.apk",
    "wetter-v1.0.apk", "wetter-v1.1.apk", "wetter-v1.2.apk",
    "icons/com.benzjeremy.learn.png", "icons/com.benzjeremy.wetter.png",
    "icons-120/com.benzjeremy.learn.png", "icons-120/com.benzjeremy.wetter.png",
    "icons-640/com.benzjeremy.learn.png", "icons-640/com.benzjeremy.wetter.png"
]:
    if os.path.exists(stale):
        os.remove(stale)
        print(f"Cleaned stale {stale}")

print("F-Droid repository exclusively contains BenzStore v1.0 and is successfully rebuilt & signed!")