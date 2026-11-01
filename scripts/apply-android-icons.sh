#!/usr/bin/env bash
# Copies the dragon-mask launcher icons into the generated Android project.
set -euo pipefail
cd "$(dirname "$0")/.."
RES="android/app/src/main/res"
[ -d "$RES" ] || { echo "Run 'npx cap add android' first"; exit 1; }
# remove Capacitor's default launcher icons so ours are the only ones
find "$RES" -name 'ic_launcher*' -delete
cp -r android-icons/res/. "$RES/"
echo "Valiryan icons applied to $RES"
