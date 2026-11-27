<p align="center">
  <img src="docs/assets/icon-192.png" width="96" height="96" alt="Duo Clone app icon">
</p>

<h1 align="center">Duo Clone</h1>

<p align="center">
  The official developer repository for Duo Clone, an Android app cloner for running two or more accounts of the same app on one phone.
</p>

<p align="center">
  <a href="https://xlabcompany.github.io/duoclone/"><img src="https://img.shields.io/badge/developer%20page-xlabcompany.github.io%2Fduoclone-00a95c" alt="Developer page"></a>
  <img src="https://img.shields.io/badge/platform-Android%206%20to%2016-0e2a1f" alt="Platform: Android 6 to 16">
  <img src="https://img.shields.io/badge/official%20channel-Google%20Play-ff48b0" alt="Official channel: Google Play">
</p>

---

Duo Clone lets you clone an app you already use, sign in with a second account in the copy, and keep your work and personal accounts apart. It is developed by [XLAB](https://xlabcompany.com/). This repository holds the developer page, the release notes and the developer notes, and it is the place to report bugs.

> **Official channel.** Google Play is the official channel for Duo Clone. This page does not offer an APK download.

## What Duo Clone does

- **Clones apps you already have**, so you can use two accounts or more of the same app at the same time.
- **Groups copies by Account.** Apps in the same Account share one Google sign-in; a new Account gets its own.
- **Private Space** hides copies behind a fingerprint or PIN lock.
- **Encrypted backup** saves a copy to a password-protected file you can restore later.
- **Memory and storage per copy**, with force stop and clear cache.
- **Quick switch** between running copies from a quiet notification or a floating bubble.
- **Custom icon and name** for each copy, to keep it private on your home screen.
- **23 languages**, with light and dark themes.

Good to know: apps that ask not to run in a virtual space cannot be cloned, including many banking and payment apps. Copies keep accounts apart but share one Android user ID, so they are separate logins, not a security sandbox. Google sign-in inside copies uses [microG](https://github.com/microg/GmsCore), an open-source project under the Apache License 2.0.

## Latest release

**Version 0.1.37 (build 40), 25 November 2026**

- A copy with a lot of data now backs up. Backups are written in pieces, so a copy of a few hundred megabytes no longer fails, and restore reads the file straight from where you saved it. Backup files from earlier versions still restore.
- When the phone or the folder you picked is out of space, a backup or restore now says Not enough free storage for the backup and tells you to free some space and try again.

Since 0.1.30 you also got Clear data for a single copy, Notifications from closed clones, Sign in with Google inside copies and a menu on the clone badge.

Every version, newest first: [Duo Clone changelog](https://xlabcompany.github.io/duoclone/changelog/).

## Developer notes

How an Android app cloner works underneath, written by the developer:

- [REQUIRE_SECURE_ENV: how an Android app opts out of app cloners](https://xlabcompany.github.io/duoclone/notes/require-secure-env/)
- [How app copies stay separate, and where the limits are](https://xlabcompany.github.io/duoclone/notes/how-app-copies-stay-separate/)
- [What Android 15 and 16 changed for app cloners](https://xlabcompany.github.io/duoclone/notes/android-15-16-app-cloners/)
- [Shipping microG inside an app cloner: licence, Accounts and limits](https://xlabcompany.github.io/duoclone/notes/microg-in-an-app-cloner/)
- [Chunked backup encryption: why large clone backups failed and how Duo Clone fixed it](https://xlabcompany.github.io/duoclone/notes/chunked-backup-encryption/)
- [Push notifications in app copies, including copies you have closed](https://xlabcompany.github.io/duoclone/notes/push-notifications-in-app-clones/)
- [Choosing honest foreground service types in an app cloner](https://xlabcompany.github.io/duoclone/notes/foreground-service-types-app-cloner/)
- [Fingerprint and face prompts inside an app copy: why they did not show and what changed](https://xlabcompany.github.io/duoclone/notes/biometric-prompts-in-app-clones/)
- [Keeping the copy number in order next to right-to-left text](https://xlabcompany.github.io/duoclone/notes/copy-number-right-to-left-text/)

## Guides on duoclone.com

The notes above are written for developers. If you use Duo Clone rather than build on Android, [duoclone.com](https://duoclone.com/) has the plain-language version: start with [a short explanation of what an app cloner is](https://duoclone.com/blog/what-is-app-cloner/), then follow [a walk-through of cloning an app for the first time](https://duoclone.com/blog/clone-app-android/). Before you rely on a copy, it is worth reading [how to keep a copy's data safe with a backup](https://duoclone.com/blog/backup-restore-cloned-app/), and if your phone slows down, there are [tips for keeping battery and memory use down](https://duoclone.com/blog/cloned-apps-battery-ram/). Every screen and button is covered, in the app's own words, in the [step-by-step user guide](https://duoclone.pages.dev/).

## Report a bug or suggest an idea

[Open an issue](https://github.com/XLABCOMPANY/duoclone/issues) and include:

1. Your phone model and Android version.
2. The app you were cloning, and its version if you know it.
3. What you did, what you expected, and what happened instead.

You can also turn on crash reports in Duo Clone's Settings; they help us find problems with specific apps faster.

## Privacy

What Duo Clone collects and why is set out in the [privacy policy](https://duoclone.com/privacy/). The installed-app list Duo Clone shows never leaves your phone, and crash reports are sent only if you turn them on.

## About this repository

The site in `docs/` is published with GitHub Pages at [xlabcompany.github.io/duoclone](https://xlabcompany.github.io/duoclone/). It is plain HTML and CSS generated by the scripts in `src/` (`python3 src/build.py`, then `python3 src/covers.py` and `python3 src/og.py` for the drawings and share images). Fonts are Bricolage Grotesque and Be Vietnam Pro under the SIL Open Font License 1.1 (`docs/assets/fonts/LICENSES.txt`).

---

Duo Clone is developed by [XLAB](https://xlabcompany.com/). Duo Clone is not affiliated with any app it can clone.
