#!/bin/bash
# Build Hogwarts TV: copy a TV-sized copy of the page into the app (hogwarts/tools/tv_assets.py), then build the APK.
#   ./build.sh            the release APK (signed with your key in hogwarts-tv/release/, or else your debug key)
#   ./build.sh install    and install it on the TV adb is connected to
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/hogwarts/tools/tv_assets.py"
(cd "$HERE/hogwarts-tv" && ./gradlew assembleRelease --console=plain -q)
APK="$HERE/hogwarts-tv/app/build/outputs/apk/release/app-release.apk"
echo "$APK"
if [ "$1" = "install" ]; then adb install -r "$APK"; fi
