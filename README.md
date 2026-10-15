# Cryoflam3 Nekoyomi Anime Extensions

**Prepared release candidate — not yet published or tested on an Android device.**
This repository contains 266 original, signature-verified APKs: 251 from Yūzōnō and 15 additional Cursedyomi packages. It preserves 77 NSFW and 189 standard extension flags. These flags come from APK manifests; they do not certify the content of every source.

## Installation after publication

The following is the **intended URL**, not a currently verified live endpoint:

`https://raw.githubusercontent.com/Cryoflam3/nekoyomi-anime-extensions/main/index.min.json`

1. In Nekoyomi 0.20.6, open **More → Settings → Browse → Anime extension repos**.
2. Tap **+ / Add**, paste the URL above, and confirm. A base URL ending in `/main` is also accepted by this version.
3. Open **Browse → Anime Extensions**, refresh, and enable the relevant language filters.
4. Install an extension. Allow Android's “Install unknown apps” permission for Nekoyomi if prompted.
5. If Nekoyomi marks it untrusted, compare its SHA-256 certificate with `upstreams.lock.json`, then use the extension's **Trust** action if you accept that signer.
6. Enable **Show NSFW content** in Browse settings if desired. Check source visibility and language filters too.
7. Test source browsing, search, details, episode listing and playback. No successful device test is claimed yet.

Do not add a path containing `/repo.json/index.min.json`. `repo.json` and `index.min.json` are sibling files, not directories. Do not change manga repositories.

## Signatures and existing installations

APKs are copied unchanged, never re-signed. Nekoyomi supports one repository fingerprint, while this collection contains multiple original signers. The repository uses the app-supported `NOFINGERPRINT` convention and requires manual extension trust rather than falsely claiming one certificate signs everything.

An installed APK from the **same provider and signer** retains its Android signing identity. A matching package installed from a **different provider** can have a different certificate and cannot be seamlessly updated by this mirror. Review `reports/signing-conflicts.json`. Back up your library and source settings before considering a provider migration; do not uninstall extensions blindly.

The lock records each APK's SHA-256, signing certificate, version, source index, immutable download origin and icon checksum. Updates must retain signer identity and increase versionCode for changed APK bytes. Upstream removals and signer rotations require review.

## Build and validate

Requires Python 3, Java and Android SDK Build Tools 35.0.0.

```sh
python3 scripts/validate.py --build-tools "$ANDROID_HOME/build-tools/35.0.0"
python3 scripts/build_repository.py --output /tmp/nekoyomi-dist
python3 scripts/validate.py --root /tmp/nekoyomi-dist --build-tools "$ANDROID_HOME/build-tools/35.0.0"
python3 scripts/check_updates.py > upstream-changes.json
```

`build_repository.py` assembles the distribution from reviewed original APKs; it is not an APK compiler. It downloads only pinned, hash-checked files when local copies are absent. No APK rebuild was needed to fix the malformed repository URLs.

GitHub Actions validates pushes and pull requests, reconstructs the distribution, and produces a weekly report of upstream changes. The manually dispatched publish workflow validates before committing generated files, does not force-push and does not replace releases. Configure the `public-publishing` environment with a required reviewer before using it. These workflows are prepared but have not yet run on GitHub. Protect `main` and require the validation job before merging changes; files committed directly to `main` are public before Actions completes.

## Rebuilding extensions

Upstream build sources and inspected commits are pinned in `upstreams.lock.json`. Yūzōnō uses `gradle/build-logic`, `src/<lang>/<source>/build.gradle` and `.github/workflows/build_push.yml`; Cursedyomi and AwkwardPeak7 use `common.gradle`, `buildSrc` and their build workflows. Inspected source heads are not asserted to reproduce every published APK byte-for-byte.

Rebuilding changes signing requirements. Do not distribute debug-signed packages as releases. Store a long-lived private keystore and its passwords in restricted GitHub Actions secrets or an external signing service, never in this repository. Only the original signer can produce an ordinary in-place update to an original APK. A new key requires a documented migration and runtime testing. There is no newly generated key or claim of signing authority in this project.

The requested Hentaigasm 14.2 icon/version change is maintained in a separate **personal-use build bundle**. It is not included in this public candidate: compilation and signing remain blocked, and its source does not clearly permit public redistribution.

## Coverage and attribution

See `reports/VALIDATION.md` for all five requested repositories, URLs, exclusions and device-test checklist. Original copyright and license texts are retained under `licenses/`. All mirrored APKs are unchanged Apache-2.0 project artifacts; upstream ownership is preserved. Supporting script code in this repository is licensed under MIT (see `LICENSE`); that does not relicense third-party APKs, artwork or source code.
