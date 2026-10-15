# Cryoflam3 Anime Extensions for Nekoyomi

A collection of 266 anime extensions for Nekoyomi: 251 from Yūzōnō and 15 from Cursedyomi. It includes 189 standard extensions and 77 marked NSFW, with the original APKs and signatures preserved.

The repository files and downloads have passed automated checks. Installation and playback still need testing on an Android device.

## Add the repository

Copy this URL:

```text
https://raw.githubusercontent.com/Cryoflam3/nekoyomi-anime-extensions/main/index.min.json
```

1. In Nekoyomi 0.20.6, open **More → Settings → Browse → Anime extension repos**.
2. Tap **Add**, paste the URL, and confirm.
3. Go to **Browse → Anime Extensions** and refresh the list. Check your language filters if an extension is missing.
4. Install the extensions you want. Android may ask you to allow installations from Nekoyomi.
5. If an extension needs to be trusted, compare its certificate with the entry in [upstreams.lock.json](upstreams.lock.json) before trusting it.
6. To see adult extensions, enable **Show NSFW content** in Browse settings.

Use the URL exactly as shown. Adding `/repo.json/` before `index.min.json` causes the invalid-repository error. Your manga repositories do not need any changes.

## What has been checked?

Both indexes and the repository metadata returned HTTP 200. All 266 APKs and 266 icons downloaded successfully and matched their recorded SHA-256 hashes. The APKs also passed signature and package metadata checks.

See the [validation report](reports/VALIDATION.md), [download checks](reports/live-validation.json), and [successful publishing run](https://github.com/Cryoflam3/nekoyomi-anime-extensions/actions/runs/38819882222).

These checks do not prove that every source can browse or play videos. Source websites can change independently of this repository.

## Existing installations and updates

The APKs here keep their original signatures. If you already have the same package from another provider, its signature may differ and Android may reject the update. Check the [signing conflicts](reports/signing-conflicts.json) and back up your library and source settings before switching providers.

Because this collection has several original signers, it uses Nekoyomi's `NOFINGERPRINT` option. You may need to trust individual extensions, including after an update.

## Hentaigasm

[Hentaigasm 14.2 has its own repository](https://github.com/Cryoflam3/hentaigasm-aniyomi-repo). It has a new icon and a new personal signing key. Read its migration instructions before installing it over an older version. It is separate from this 266-extension index.

## Maintenance

The lock file records versions, hashes, certificates and the exact upstream commits used. Validation catches duplicate packages, duplicate source IDs, unexpected signer changes and version regressions.

GitHub Actions checks pushes and pull requests. A weekly workflow reports upstream changes for review; it does not automatically import them. The manual publishing workflow validates the files before publishing them.

To check or reconstruct the repository locally, use Python 3, Java and Android Build Tools 35.0.0:

```sh
python3 scripts/validate.py --build-tools "$ANDROID_HOME/build-tools/35.0.0"
python3 scripts/build_repository.py --output /tmp/nekoyomi-dist
python3 scripts/validate.py --root /tmp/nekoyomi-dist --build-tools "$ANDROID_HOME/build-tools/35.0.0"
python3 scripts/check_updates.py > upstream-changes.json
python3 scripts/verify_live.py
```

The build script assembles the repository from the reviewed APKs. It does not compile new APKs. Rebuilt extensions need an appropriate signing key and device testing before release. Never commit signing keys or passwords.

## Credits

Thanks to the Yūzōnō, Cursedyomi and AwkwardPeak7 developers. Their notices and Apache-2.0 licenses are preserved under [licenses](licenses/). The supporting scripts use the [MIT license](LICENSE); this does not change the licenses of third-party code or artwork.

The [exclusion list](reports/excluded.json) explains which original builds were left out and why.
