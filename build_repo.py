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

# App Icon: Learn
with open("repo/icons/com.benzjeremy.learn.png", "rb") as f:
    app_icon_bytes = f.read()
app_icon_sha256 = hashlib.sha256(app_icon_bytes).hexdigest()
app_icon_size = len(app_icon_bytes)

# App Icon: Wetter
with open("repo/icons/com.benzjeremy.wetter.png", "rb") as f:
    wetter_icon_bytes = f.read()
wetter_icon_sha256 = hashlib.sha256(wetter_icon_bytes).hexdigest()
wetter_icon_size = len(wetter_icon_bytes)

# Read APK v2.0 (Pure Native Android UI)
with open("repo/learn-v2.0.apk", "rb") as f:
    apk_v2_bytes = f.read()
apk_v2_sha256 = hashlib.sha256(apk_v2_bytes).hexdigest()
apk_v2_size = len(apk_v2_bytes)

# Read APK v1.0 (WebView Container)
with open("repo/learn-v1.0.apk", "rb") as f:
    apk_v1_bytes = f.read()
apk_v1_sha256 = hashlib.sha256(apk_v1_bytes).hexdigest()
apk_v1_size = len(apk_v1_bytes)

# Read APK Wetter v1.0 (Native Android UI & Widget)
with open("repo/wetter-v1.0.apk", "rb") as f:
    wetter_apk_bytes = f.read()
wetter_apk_sha256 = hashlib.sha256(wetter_apk_bytes).hexdigest()
wetter_apk_size = len(wetter_apk_bytes)

print(f"Repo Icon (JB): {repo_icon_size} bytes")
print(f"App Icon (Learn): {app_icon_size} bytes")
print(f"App Icon (Wetter): {wetter_icon_size} bytes")
print(f"APK Learn v2.0 (Native): sha256={apk_v2_sha256}, size={apk_v2_size}")
print(f"APK Learn v1.0 (WebView): sha256={apk_v1_sha256}, size={apk_v1_size}")
print(f"APK Wetter v1.0 (Native): sha256={wetter_apk_sha256}, size={wetter_apk_size}")

# 1. index-v2.json (F-Droid v2 Schema with localized maps & multi-version support)
index_v2_data = {
    "repo": {
        "name": {
            "de-DE": "Jeremy Benz F-Droid Repository",
            "en-US": "Jeremy Benz F-Droid Repository"
        },
        "description": {
            "de-DE": "Offizielles F-Droid-Repository für freie, quelloffene und datenschutzfreundliche Android-Apps von Jeremy Benz.",
            "en-US": "Official F-Droid repository for privacy-first, free and open-source Android applications by Jeremy Benz."
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
            "Education": {
                "name": {
                    "de-DE": "Bildung",
                    "en-US": "Education"
                }
            },
            "Development": {
                "name": {
                    "de-DE": "Entwicklung",
                    "en-US": "Development"
                }
            },
            "Weather": {
                "name": {
                    "de-DE": "Wetter",
                    "en-US": "Weather"
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
        "com.benzjeremy.learn": {
            "metadata": {
                "added": ts,
                "lastUpdated": ts,
                "categories": [
                    "Education",
                    "Development"
                ],
                "name": {
                    "de-DE": "learn",
                    "en-US": "learn"
                },
                "summary": {
                    "de-DE": "Datenschutzfreundliche Lern-App nach Fachinformatiker-Standard",
                    "en-US": "Privacy-first code learning app following vocational standards"
                },
                "description": {
                    "de-DE": "Open-Source Lern-App nach Fachinformatiker-Standard. 100% native Android-UI (Zero WebView) ab v2.0. 9 modulare Curricula (Go, Cybersecurity, SQL, C#, Astro, Python, HTML/CSS, JS und PHP), 90-minütige Prüfungs-Simulation, interaktives Code-Labor und tägliche Erinnerungen.",
                    "en-US": "Open-source vocational code learning application. 100% native Android UI (zero WebView) starting in v2.0. 9 modular curricula (Go, Cybersecurity, SQL, C#, Astro, Python, HTML/CSS, JS, and PHP), 90-minute timed exam simulation, interactive code lab, and daily reminders."
                },
                "license": "GPL-3.0-or-later",
                "webSite": "https://benzjeremy.github.io/learn/",
                "sourceCode": "https://github.com/benzjeremy/learn",
                "issueTracker": "https://github.com/benzjeremy/learn/issues",
                "authorName": "Jeremy Benz",
                "authorEmail": "benzjeremy@pm.me",
                "authorWebSite": "https://benzjeremy.github.io/",
                "icon": {
                    "en-US": {
                        "name": "/icons/com.benzjeremy.learn.png",
                        "sha256": app_icon_sha256,
                        "size": app_icon_size
                    }
                },
                "preferredSigner": FINGERPRINT_HEX
            },
            "versions": {
                apk_v2_sha256: {
                    "added": ts,
                    "file": {
                        "name": "/learn-v2.0.apk",
                        "sha256": apk_v2_sha256,
                        "size": apk_v2_size
                    },
                    "manifest": {
                        "versionName": "2.0",
                        "versionCode": 200,
                        "usesSdk": {
                            "minSdkVersion": 21,
                            "targetSdkVersion": 34
                        },
                        "signer": {
                            "sha256": [
                                FINGERPRINT_HEX
                            ]
                        },
                        "usesPermission": [
                            {
                                "name": "android.permission.POST_NOTIFICATIONS"
                            },
                            {
                                "name": "android.permission.SCHEDULE_EXACT_ALARM"
                            }
                        ]
                    },
                    "whatsNew": {
                        "de-DE": "Release v2.0: Vollständig native Android-UI (Zero WebView), 9 Curricula, 90-Min-Prüfung, Code-Labor und tägliche Erinnerung.",
                        "en-US": "Release v2.0: Pure native Android UI (Zero WebView), 9 curricula, 90-minute exam simulation, code lab, and daily reminders."
                    }
                },
                apk_v1_sha256: {
                    "added": ts - 86400000,
                    "file": {
                        "name": "/learn-v1.0.apk",
                        "sha256": apk_v1_sha256,
                        "size": apk_v1_size
                    },
                    "manifest": {
                        "versionName": "1.0",
                        "versionCode": 100,
                        "usesSdk": {
                            "minSdkVersion": 21,
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
                            }
                        ]
                    },
                    "whatsNew": {
                        "de-DE": "Release v1.0: Erste Edition mit integriertem Web-Cockpit.",
                        "en-US": "Release v1.0: Initial edition with integrated web cockpit."
                    }
                }
            }
        },
        "com.benzjeremy.wetter": {
            "metadata": {
                "added": ts,
                "lastUpdated": ts,
                "categories": [
                    "Weather",
                    "Utility"
                ],
                "name": {
                    "de-DE": "Wetter",
                    "en-US": "Weather"
                },
                "summary": {
                    "de-DE": "Minimalistische Wetter-App & Solar-PV-Prognose mit Startbildschirm-Widget",
                    "en-US": "Minimalist weather forecast and solar PV yield estimation with home screen widget"
                },
                "description": {
                    "de-DE": "Werbefreie Wetter- und Solar-PV-App für Android mit interaktivem Homescreen-Widget. Direkte Open-Meteo API-Anbindung (ohne Relay-Server, ohne API-Key), 24h- und 7-Tage-Vorhersage, genaue PV-Ertragsprognose (5 kWp Modell), weltweites Geocoding und Offline-Caching.",
                    "en-US": "Ad-free weather and solar PV forecast app for Android with an interactive home screen widget. Direct Open-Meteo API integration (zero relay server, zero API key), 24h and 7-day forecast, accurate solar PV yield estimation (5 kWp reference model), global geocoding, and offline caching."
                },
                "license": "GPL-3.0-or-later",
                "webSite": "https://benzjeremy.github.io/wetter-site/",
                "sourceCode": "https://github.com/benzjeremy/wetter-site",
                "issueTracker": "https://github.com/benzjeremy/wetter-site/issues",
                "authorName": "Jeremy Benz",
                "authorEmail": "benzjeremy@pm.me",
                "authorWebSite": "https://benzjeremy.github.io/",
                "icon": {
                    "en-US": {
                        "name": "/icons/com.benzjeremy.wetter.png",
                        "sha256": wetter_icon_sha256,
                        "size": wetter_icon_size
                    }
                },
                "preferredSigner": FINGERPRINT_HEX
            },
            "versions": {
                wetter_apk_sha256: {
                    "added": ts,
                    "file": {
                        "name": "/wetter-v1.0.apk",
                        "sha256": wetter_apk_sha256,
                        "size": wetter_apk_size
                    },
                    "manifest": {
                        "versionName": "1.0",
                        "versionCode": 100,
                        "usesSdk": {
                            "minSdkVersion": 21,
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
                                "name": "android.permission.ACCESS_NETWORK_STATE"
                            }
                        ]
                    },
                    "whatsNew": {
                        "de-DE": "Release v1.0: Erste Edition mit nativer Android-UI, 24h/7-Tage-Prognose, Solar-PV-Modell und Startbildschirm-Widget.",
                        "en-US": "Release v1.0: Initial release with native Android UI, 24h/7-day forecast, solar PV modeling, and home screen widget."
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
        "numPackages": 2
    },
    "diffs": {}
}
with open("repo/entry.json", "w", encoding="utf-8") as f:
    json.dump(entry_data, f, indent=2)

# 3. index-v1.json (Kept for V1 clients with plain string fields)
index_v1_data = {
    "repo": {
        "name": "Jeremy Benz F-Droid Repository",
        "description": "Official F-Droid repository for privacy-first, free and open-source Android applications by Jeremy Benz.",
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
            "packageName": "com.benzjeremy.learn",
            "name": "learn",
            "summary": "Privacy-first vocational code learning app (Native UI v2.0)",
            "description": "Open-source code learning application following vocational software engineering standards. In-depth curricula for Go, Cybersecurity, SQL, C#, Astro, Python, HTML/CSS, JS & PHP with 90-minute exams, code lab, and native Android UI.",
            "license": "GPL-3.0-or-later",
            "webSite": "https://benzjeremy.github.io/learn/",
            "sourceCode": "https://github.com/benzjeremy/learn",
            "issueTracker": "https://github.com/benzjeremy/learn/issues",
            "authorName": "Jeremy Benz",
            "authorEmail": "benzjeremy@pm.me",
            "authorWebSite": "https://benzjeremy.github.io/",
            "icon": "icons/com.benzjeremy.learn.png",
            "categories": [
                "Education",
                "Development"
            ],
            "antiFeatures": [],
            "suggestedVersionCode": "200"
        },
        {
            "packageName": "com.benzjeremy.wetter",
            "name": "Wetter",
            "summary": "Minimalistische Wetter-App & Solar-PV-Prognose mit Startbildschirm-Widget",
            "description": "Werbefreie Wetter- und Solar-PV-App für Android mit interaktivem Homescreen-Widget. Direkte Open-Meteo API-Anbindung (ohne Relay-Server, ohne API-Key), 24h- und 7-Tage-Vorhersage, genaue PV-Ertragsprognose (5 kWp Modell), weltweites Geocoding und Offline-Caching.",
            "license": "GPL-3.0-or-later",
            "webSite": "https://benzjeremy.github.io/wetter-site/",
            "sourceCode": "https://github.com/benzjeremy/wetter-site",
            "issueTracker": "https://github.com/benzjeremy/wetter-site/issues",
            "authorName": "Jeremy Benz",
            "authorEmail": "benzjeremy@pm.me",
            "authorWebSite": "https://benzjeremy.github.io/",
            "icon": "icons/com.benzjeremy.wetter.png",
            "categories": [
                "Weather",
                "Utility"
            ],
            "antiFeatures": [],
            "suggestedVersionCode": "100"
        }
    ],
    "packages": {
        "com.benzjeremy.learn": [
            {
                "versionName": "2.0",
                "versionCode": 200,
                "size": apk_v2_size,
                "apkName": "learn-v2.0.apk",
                "hash": apk_v2_sha256,
                "hashType": "sha256",
                "minSdkVersion": 21,
                "targetSdkVersion": 34,
                "added": ts,
                "sig": PUBKEY_HEX,
                "signer": "jeremybenz"
            },
            {
                "versionName": "1.0",
                "versionCode": 100,
                "size": apk_v1_size,
                "apkName": "learn-v1.0.apk",
                "hash": apk_v1_sha256,
                "hashType": "sha256",
                "minSdkVersion": 21,
                "targetSdkVersion": 34,
                "added": ts - 86400000,
                "sig": PUBKEY_HEX,
                "signer": "jeremybenz"
            }
        ],
        "com.benzjeremy.wetter": [
            {
                "versionName": "1.0",
                "versionCode": 100,
                "size": wetter_apk_size,
                "apkName": "wetter-v1.0.apk",
                "hash": wetter_apk_sha256,
                "hashType": "sha256",
                "minSdkVersion": 21,
                "targetSdkVersion": 34,
                "added": ts,
                "sig": PUBKEY_HEX,
                "signer": "jeremybenz"
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
    <description>Official F-Droid repository for privacy-first, free and open-source Android applications by Jeremy Benz.</description>
  </repo>
  <application id="com.benzjeremy.learn">
    <id>com.benzjeremy.learn</id>
    <added>2026-09-12</added>
    <lastupdated>2026-09-12</lastupdated>
    <name>learn</name>
    <summary>Privacy-first vocational code learning app (Native UI v2.0)</summary>
    <icon>icons/com.benzjeremy.learn.png</icon>
    <desc>Open-source code learning application following vocational software engineering standards. In-depth curricula for Go, Cybersecurity, SQL, C#, Astro, Python, HTML/CSS, JS and PHP featuring 90-minute exams, code lab, and pure native Android UI.</desc>
    <license>GPL-3.0-or-later</license>
    <category>Education,Development</category>
    <web>https://benzjeremy.github.io/learn/</web>
    <source>https://github.com/benzjeremy/learn</source>
    <tracker>https://github.com/benzjeremy/learn/issues</tracker>
    <marketversion>2.0</marketversion>
    <marketvercode>200</marketvercode>
    <package>
      <version>2.0</version>
      <versioncode>200</versioncode>
      <size>{apk_v2_size}</size>
      <apkname>learn-v2.0.apk</apkname>
      <srcname>learn-v2.0.tar.gz</srcname>
      <hash type="sha256">{apk_v2_sha256}</hash>
      <sig>{PUBKEY_HEX}</sig>
      <added>2026-09-12</added>
    </package>
    <package>
      <version>1.0</version>
      <versioncode>100</versioncode>
      <size>{apk_v1_size}</size>
      <apkname>learn-v1.0.apk</apkname>
      <srcname>learn-v1.0.tar.gz</srcname>
      <hash type="sha256">{apk_v1_sha256}</hash>
      <sig>{PUBKEY_HEX}</sig>
      <added>2026-09-12</added>
    </package>
  </application>
  <application id="com.benzjeremy.wetter">
    <id>com.benzjeremy.wetter</id>
    <added>2026-09-12</added>
    <lastupdated>2026-09-12</lastupdated>
    <name>Wetter</name>
    <summary>Minimalistische Wetter-App &amp; Solar-PV-Prognose mit Startbildschirm-Widget</summary>
    <icon>icons/com.benzjeremy.wetter.png</icon>
    <desc>Werbefreie Wetter- und Solar-PV-App für Android mit interaktivem Homescreen-Widget. Direkte Open-Meteo API-Anbindung (ohne Relay-Server, ohne API-Key), 24h- und 7-Tage-Vorhersage, genaue PV-Ertragsprognose (5 kWp Modell), weltweites Geocoding und Offline-Caching.</desc>
    <license>GPL-3.0-or-later</license>
    <category>Weather,Utility</category>
    <web>https://benzjeremy.github.io/wetter-site/</web>
    <source>https://github.com/benzjeremy/wetter-site</source>
    <tracker>https://github.com/benzjeremy/wetter-site/issues</tracker>
    <marketversion>1.0</marketversion>
    <marketvercode>100</marketvercode>
    <package>
      <version>1.0</version>
      <versioncode>100</versioncode>
      <size>{wetter_apk_size}</size>
      <apkname>wetter-v1.0.apk</apkname>
      <srcname>wetter-v1.0.tar.gz</srcname>
      <hash type="sha256">{wetter_apk_sha256}</hash>
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
    "learn-v2.0.apk", "learn-v1.0.apk",
    "wetter-v1.0.apk"
]:
    if os.path.exists(os.path.join("repo", fn)):
        shutil.copy2(os.path.join("repo", fn), fn)
        print(f"Copied {fn} to root")

print("All F-Droid index files (v2, v1 & legacy) and all APKs (Learn v2/v1 & Wetter v1.0) built and signed successfully!")
