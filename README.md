# VALIRYAN

Music, video, audiobook, PDF and photo player — one HTML app (`www/index.html`),
packaged as an installable **Android app** with the dragon-mask icon.

## Get the Android app (no PC needed)

1. Create a new GitHub repo and upload everything in this folder (or `git push` it).
2. Open the **Actions** tab → **Build Android APK** → wait ~5 minutes (it also runs on every push).
3. Open the finished run → **Artifacts** → download **Valiryan-APK** → unzip → install `app-debug.apk`
   (allow "install unknown apps" for your browser/Files app when Android asks).
4. "Valiryan" appears in your app drawer with the dragon icon.

## Or install it as a web app (PWA)

Repo **Settings → Pages → Source: GitHub Actions**. After the *Deploy web version* run,
open the Pages link in Chrome → ⋮ → **Install app**. The icon is the same dragon mask.

## Change the icon

Replace `assets/icon-source.jpg`, run `pip install pillow && python3 scripts/make-icons.py`, commit.
The crop is set by `TOP` in `scripts/make-icons.py`.

## Layout

```
www/                  the app (index.html, manifest, service worker, icons, vendor/jsmediatags)
assets/               icon source picture + 1024px master
android-icons/        ready-made launcher icons (legacy + adaptive) copied into the Android build
scripts/              make-icons.py, apply-android-icons.sh
.github/workflows/    android-apk.yml (APK build) · pages.yml (web deploy)
capacitor.config.json app id com.valiryan.player, name "Valiryan"
```

## Local build (optional)

```
npm install
npx cap add android
bash scripts/apply-android-icons.sh
npx cap sync android
cd android && ./gradlew assembleDebug     # needs JDK 17 + Android SDK
```

Notes: the APK is a debug build (installable, not Play Store signed). `jsmediatags` is bundled
locally so tag/cover reading works offline.
