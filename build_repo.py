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
KEYSTORE = "myfdroid.keystore"
KEYPASS = "myfdroid_secret_key_2026"

ts = int(time.time() * 1000)

# 1. index-v1.json
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
            "summary": "Privacy-first code learning app with compiler lab & 90-min final exams",
            "description": "Open-source code learning application following vocational software engineering standards. In-depth curricula for Go, Cybersecurity, SQL, C#, Astro, Python, HTML/CSS, JS & PHP with 90-minute exams and in-browser compiler lab.",
            "license": "GPL-3.0-or-later",
            "webSite": "https://benzjeremy.github.io/learn/",
            "sourceCode": "https://github.com/benzjeremy/learn",
            "issueTracker": "https://github.com/benzjeremy/learn/issues",
            "authorName": "Jeremy Benz",
            "authorEmail": "benzjeremy@pm.me",
            "authorWebSite": "https://benzjeremy.github.io/",
            "categories": [
                "Education",
                "Development"
            ],
            "antiFeatures": [],
            "suggestedVersionCode": "100"
        }
    ],
    "packages": {
        "com.benzjeremy.learn": [
            {
                "versionName": "1.0",
                "versionCode": 100,
                "size": 18450000,
                "apkName": "learn-v1.0.apk",
                "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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

os.makedirs("repo", exist_ok=True)
json_bytes = json.dumps(index_v1_data, indent=2).encode("utf-8")
with open("repo/index-v1.json", "wb") as f:
    f.write(json_bytes)
json_sha256 = hashlib.sha256(json_bytes).hexdigest()
json_size = len(json_bytes)

# 2. entry.json (F-Droid v2 protocol)
entry_data = {
    "timestamp": ts,
    "version": 20000,
    "maxAge": 14,
    "index": {
        "name": "/index-v1.json",
        "sha256": json_sha256,
        "size": json_size,
        "numPackages": 1
    },
    "diffs": {}
}
with open("repo/entry.json", "w", encoding="utf-8") as f:
    json.dump(entry_data, f, indent=2)

# 3. index.xml
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
    <summary>Privacy-first code learning app with compiler lab &amp; 90-min final exams</summary>
    <icon>icon.png</icon>
    <desc>Open-source code learning application following vocational software engineering standards. In-depth curricula for Go, Cybersecurity, SQL, C#, Astro, Python, HTML/CSS, JS and PHP featuring 90-minute exams and in-browser compiler lab.</desc>
    <license>GPL-3.0-or-later</license>
    <category>Education,Development</category>
    <web>https://benzjeremy.github.io/learn/</web>
    <source>https://github.com/benzjeremy/learn</source>
    <tracker>https://github.com/benzjeremy/learn/issues</tracker>
    <marketversion>1.0</marketversion>
    <marketvercode>100</marketvercode>
    <package>
      <version>1.0</version>
      <versioncode>100</versioncode>
      <size>18450000</size>
      <apkname>learn-v1.0.apk</apkname>
      <srcname>learn-v1.0.tar.gz</srcname>
      <hash type="sha256">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</hash>
      <sig>{PUBKEY_HEX}</sig>
      <added>2026-09-12</added>
    </package>
  </application>
</fdroid>
"""
with open("repo/index.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

# 4. Sign JAR files
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

# 5. Mirror to root of repository
for fn in ["index-v1.json", "index-v1.jar", "index.xml", "index.jar", "entry.json", "entry.jar"]:
    shutil.copy2(os.path.join("repo", fn), fn)
    print(f"Copied {fn} to root")

print("All F-Droid index files (v1, v2 & legacy) built and signed successfully!")
