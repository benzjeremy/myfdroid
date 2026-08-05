import os

# Base URL targeting GitHub Pages
repo_url = "https://benzjeremy.github.io/myfdroid/repo"
repo_name = "Automated Custom F-Droid Repo"
repo_icon = "icon.png"
repo_description = "Automatically built and deployed via GitHub Actions."

# Keystore configuration reading from GitHub Actions Environment
keystore = "keystore.p12"
keystorepass = os.getenv("FDROID_KEYSTORE_PASSWORD", "SUPER_SECRET_PASSWORD")
keypass = keystorepass
keyalias = "fdroid"
