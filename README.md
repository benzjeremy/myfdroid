# 📲 myfdroid — Official F-Droid Repository

[![F-Droid Compatible](https://img.shields.io/badge/F--Droid-Compatible-38bdf8.svg?logo=fdroid)](https://benzjeremy.github.io/myfdroid/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)
[![Status: Pre-Release](https://img.shields.io/badge/Status-Pre--Release%20%2F%20WIP-orange.svg)](https://benzjeremy.github.io/myfdroid/)
[![Apps: learn & wetter](https://img.shields.io/badge/Apps-learn%20%7C%20wetter-10b981.svg)](https://benzjeremy.github.io/myfdroid/#apps)
[![Security: RSA-4096 / SHA-256](https://img.shields.io/badge/Signatures-RSA--4096%20%2F%20SHA--256-8b5cf6.svg)](https://benzjeremy.github.io/myfdroid/)

> [!IMPORTANT]
> ### 🚧 Pre-Release / Active Development Notice
> **This repository infrastructure and indexed software applications are not yet finalized and remain under active development.**  
> All APKs, repository indices, and packages are **Pre-Releases** (Work in Progress), even if released under major version tags.

> The official cryptographically signed F-Droid repository for privacy-first, free and open-source Android applications developed by Jeremy Benz ([@benzjeremy](https://github.com/benzjeremy)).

---

## 🌟 Repository Overview

* **Repository URL:** `https://benzjeremy.github.io/myfdroid/repo`
* **Signing Fingerprint (SHA-256):**  
  `A2:AD:02:7C:85:6A:E9:E1:11:B1:7A:55:DF:53:03:BB:42:3D:BF:8D:44:7D:C9:81:BD:B0:E2:13:46:96:3C:B7`
* **Hex Fingerprint:**  
  `a2ad027c856ae9e111b17a55df5303bb423dbf8d447dc981bdb0e21346963cb7`
* **Schema Standards:** F-Droid v2 (`index-v2.json`, `entry.jar`), v1 (`index-v1.json`, `index-v1.jar`), and legacy XML (`index.xml`, `index.jar`).

---

## 📱 Hosted Applications

### 1. `com.benzjeremy.learn` (learn)
* **Latest Version:** `v2.2` (Code: `220`)
* **Key Features:**
  * 100% Pure Native Android UI (zero WebView overhead).
  * 45 beginner-friendly didactic coding lessons across 9 technical domains (Go, Cybersecurity, SQL, Python, Web/CSS, JavaScript, C#, Astro, PHP).
  * 90-minute timed vocational exam simulation with authentic German grading scale (1–6).
  * Native offline legal compliance: Full Impressum (§ 5 DDG) and Privacy Policy (GDPR / § 25 TDDDG) directly inside the interface.
  * Zero internet permissions requested (`android.permission.INTERNET` omitted) — 100% guaranteed offline privacy.
  * Configurable local habit reminder alarms.

### 2. `com.benzjeremy.wetter` (Wetter)
* **Latest Version:** `v1.2` (Code: `120`)
* **Key Features:**
  * Real-time weather data via direct HTTPS queries to Open-Meteo REST API (zero intermediary relay servers, zero telemetry).
  * Rooftop and balcony solar photovoltaic (PV) generation modeling (5 kWp reference setup).
  * Interactive Android App Widget with live real-time clock (`TextClock`), temperature, conditions, and solar stats.
  * Configurable auto-refresh background interval (15m, 30m, 1h, or manual only) scheduled via `AlarmManager`.
  * Embedded native offline legal notice (§ 5 DDG Impressum, GDPR Privacy Policy & GPL-3.0).

---

## 🚀 How to Add to Your Android Client

1. Open your preferred F-Droid client (**F-Droid**, **Droid-ify**, or **Neo Store**).
2. Go to **Settings → Repositories → Add (+)**.
3. Paste the following URL:
   ```text
   https://benzjeremy.github.io/myfdroid/repo?fingerprint=A2AD027C856AE9E111B17A55DF5303BB423DBF8D447DC981BDB0E21346963CB7
   ```
4. Synchronize repositories to receive automatic cryptographically verified updates.

---

## 🛠️ Repository Maintenance & Build Pipeline

To regenerate all index files and re-sign with the release keystore:
```bash
python3 build_repo.py
```
This automatically updates `index-v2.json`, `entry.json`, `index-v1.json`, `index.xml`, generates signed JAR envelopes with `jarsigner`, and mirrors artifacts to the repository root.

---

## ⚖️ Legal & Privacy

* **Impressum (§ 5 DDG):** [https://benzjeremy.github.io/myfdroid/impressum.html](https://benzjeremy.github.io/myfdroid/impressum.html)
* **Datenschutz (GDPR):** [https://benzjeremy.github.io/myfdroid/datenschutz.html](https://benzjeremy.github.io/myfdroid/datenschutz.html)
* **Contact:** [benzjeremy@pm.me](mailto:benzjeremy@pm.me)

---

## 📜 License

Licensed under the [GNU General Public License v3.0 (GPL-3.0)](LICENSE).
