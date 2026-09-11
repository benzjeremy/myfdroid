# 📱 myfdroid

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Website](https://img.shields.io/badge/Web-Repository%20Portal-brightgreen)](https://benzjeremy.github.io/myfdroid/)
[![F-Droid Repo](https://img.shields.io/badge/F--Droid-Compatible-blue)](https://benzjeremy.github.io/myfdroid/repo)

> **Official F-Droid & Android Package Repository** for open-source applications maintained by Jeremy Benz.

Provides automated, reproducible builds, signed APK metadata, and direct repository integration for privacy-respecting Android package managers including **F-Droid**, **Droid-ify**, and **Neo Store**.

---

## 📲 Add to Your Android Device

### Repository URL
Add the following URL to your F-Droid client (under *Settings* &rarr; *Repositories* &rarr; *Add (+)*):

```text
https://benzjeremy.github.io/myfdroid/repo
```

### 1-Click QR Code & Web Portal
Visit the official repository landing page to scan the QR code directly with your device camera or F-Droid client:
👉 **[https://benzjeremy.github.io/myfdroid/](https://benzjeremy.github.io/myfdroid/)**

---

## 📦 Hosted Applications

| Application | Package ID | Current Version | Description |
|---|---|---|---|
| **learn** | `com.benzjeremy.learn` | `v2.0` (Native UI) / `v1.0` (Legacy) | Privacy-first code learning app with 9 curricula, 90-min exam, code lab, and pure native Android UI. |

---

## 🛠️ Repository Architecture

- **`main`:** Repository manifest, sync scripts, CI workflows, and documentation.
- **`web`:** Static F-Droid repository index (`repo/index-v1.json`, `repo/index.jar`), web showcase, QR code portal, and setup manual.

---

## 📜 License
This repository and its indexing pipelines are licensed under the [GNU General Public License v3.0](LICENSE).
