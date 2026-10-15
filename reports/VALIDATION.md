# Validation report — 2026-10-15

## Result and limits

Prepared locally: **266 APKs**, **77 NSFW / 189 standard**, from three Apache-2.0 source projects after duplicate resolution (selected packages originate from two projects). No public repository has been created or modified. No new release was replaced. Manga repositories were not touched.

All 301 APK entries across the five originals passed Android Build Tools 35.0.0 `apksigner verify`, package/version consistency, anime feature, source class descriptor presence, manifest NSFW and Nekoyomi API-range checks. This is static compatibility evidence, not proof of source initialization or playback. The 266-file consolidated tree passed the standalone validator, and reconstruction reproduced its indexes and assets byte-for-byte.

321 HTTP HEAD checks: all five supplied nested index URLs returned 404; all five correct metadata and index endpoints returned 200. All 300 expected upstream APK paths outside Cryoflam3 returned 200. Cryoflam3's expected `/apk/` path returned 404. Git clones supplied the actual APK bytes for all 301 entries. Full evidence: `http-audit.json` and `apk-audit.json`.

## Application investigation

Latest stable release observed: [Nekoyomi v0.20.6](https://github.com/Seguaz/Nekoyomi/releases/tag/v0.20.6), published September 11, 2026. Source commit: `680e243e3d3410fdc75d038c15abeacee7d61069`.

Code paths at that commit:

- `domain/.../extensionrepo/anime/interactor/CreateAnimeExtensionRepo.kt`: requires HTTPS, strips `/index.min.json`, `/index.json` or `/index.pb` and trailing slashes. It does **not** strip `/repo.json`.
- `domain/.../extensionrepo/service/ExtensionRepoService.kt`: requests `<base>/repo.json`, parses `meta` and returns invalid repository when the request or decoding fails.
- `domain/.../extensionrepo/service/ExtensionRepoDto.kt`: `name`, nullable `shortName`, `website`, `signingKeyFingerprint`. `AppModule.kt` uses `explicitNulls=false`, so omitted nullable shortName is accepted.
- `app/.../extension/anime/api/AnimeExtensionApi.kt`: fetches `<base>/index.min.json` as a list, expects package, name, version, code, language, APK filename, NSFW flag, optional torrent flag and nullable sources; source IDs use Kotlin Long. APK paths are `<base>/apk/<filename>`, icons `<base>/icon/<package>.png`.
- `app/.../extension/anime/util/AnimeExtensionLoader.kt`: accepts API versions 12–16, requires `tachiyomi.animeextension`, checks certificate trust and NSFW settings, then loads source classes.
- `app/.../domain/extension/anime/interactor/TrustAnimeExtension.kt`: trusts a matching configured repository signer or an explicitly trusted package/version/signature tuple. `UpdateAnimeExtensionRepo.kt` recognizes the `NOFINGERPRINT` prefix.

Thus the supplied path `<base>/repo.json/index.min.json` normalizes to `<base>/repo.json`, then triggers `<base>/repo.json/repo.json`, which also returns 404 for all five repositories. There is no evidence of a blanket anime-repository prohibition. Manga and anime have separate stores/loaders; their difference in observed behavior does not require changing the user's working manga settings.

Adding a repository happens before downloading or loading an APK. APK signing cannot explain this specific metadata-fetch failure, although it can cause later installation/trust problems.

## Per-repository findings

| Repository | Published entries | Prepared import | Status and exact blocker |
|---|---:|---:|---|
| Cryoflam3 Hentaigasm | 1 | 0 | Corrected index resolves, but APK/icon sit at root instead of `apk/` and `icon/`. `no-info` is not a real certificate. APK is byte-identical to Addons Hentaigasm and signed `5db0…c2ff`. Source identified as `aniyomi-addons/hentaigasm-ext`; README permits personal use, not clearly public redistribution. Icon/version 14.2 change prepared separately, build/signing pending. |
| Yūzōnō Anime | 251 | 251 | Corrected metadata and index valid; APKs, API range and signatures validated. Apache-2.0 source at `yuzono/anime-extensions`. All selected. Runtime untested. |
| AwkwardPeak7 | 2 | 0 | Apache-2.0; archived January 14, 2025. Both signed APKs pass checks, but Jav Guru and MissAV have source IDs identical to selected Yūzōnō sources under different package names. Excluded from primary index to avoid source ownership collisions. Licensed maintenance is possible, but no unneeded rebuild performed. |
| Aniyomi Addons | 16 | 0 | Corrected repo and APK URLs work and signatures validate. Published metadata still names Goddivor. Examined individual source repositories; no LICENSE files found, several READMEs explicitly say personal use. No clear blanket public redistribution grant established. Seven package names overlap Yūzōnō with a different certificate. Permission required for these particular builds. |
| Cursedyomi | 31 | 15 | Apache-2.0. All APKs pass static checks. Sixteen duplicate packages are supplied by Yūzōnō, whose selected versions are newer or equal; signer differences are recorded. Fifteen additional packages selected unchanged. Runtime untested. |

### Corrected original URLs (HTTP 200 verified, not device acceptance)

- Cryoflam3: `https://raw.githubusercontent.com/Cryoflam3/hentaigasm-aniyomi-repo/main/index.min.json` — APK download still broken until the original file layout is repaired.
- Yūzōnō: `https://raw.githubusercontent.com/yuzono/anime-repo/repo/index.min.json`
- AwkwardPeak7: `https://raw.githubusercontent.com/AwkwardPeak7/aniyomi-extensions/repo/index.min.json`
- Addons: `https://raw.githubusercontent.com/aniyomi-addons/anime-extensions-repo/repo/index.min.json`
- Cursedyomi: `https://raw.githubusercontent.com/Claudemirovsky/cursedyomi-extensions/repo/index.min.json`

## Signing and version policy

Original APK certificates, confirmed for every entry:

| Provider | SHA-256 certificate |
|---|---|
| Yūzōnō | `cbec121aa82ebb02aaa73806992e0368a97d47b5451ed6524816d03084c45905` |
| Cursedyomi | `7950facf5b1693fbf4bb4e74c01db2d74ece28b4a2a3eb613be38f8b626d13a3` |
| AwkwardPeak7 | `45ab79cda84203f0c2aa6bd54db46932f9d7085da9f2444dc32de58e4696655e` |
| Addons and Cryoflam3 Hentaigasm | `5db0f9f3466f0835234c827747ee1986e9341eb192530623e415b43dbe89c2ff` |

The consolidated repo intentionally does not assert one of these is the signer of every APK. Its unique `NOFINGERPRINT` marker allows individual trust rather than a forged signing identity. Manual trust may need repeating for a new version. Existing installs with the selected certificate retain the same identity; installs from another provider may conflict. No original private keys are available here.

`check_transition.py` blocks versionCode/API regression, changed APKs without a versionCode increase and signer switches. `check_updates.py` reports upstream changes for review rather than automatically importing unreviewed binaries. Package and source-ID collisions are rejected by validation.

## Licenses and attribution

Preserved project Apache-2.0 license and README attribution for Yūzōnō, AwkwardPeak7 and Cursedyomi. Source projects, inspected commits, build files and license discoveries are recorded in `source-catalog.json`; selected APK provenance is pinned to publication commits in `upstreams.lock.json`. Inspected source heads are not a claim of bit-reproducible builds. No blanket permission is inferred from a public GitHub URL, a signed binary, or the user's ownership of a copied repository.

## Hentaigasm requested change

Separate personal-use bundle includes the new non-explicit crimson/violet H/play icon at all five Android densities and versionCode 2 (versionName 14.2). Source package and NSFW flag are preserved. Build scaffold derives from the Apache-2.0 Cursedyomi project and is scoped to this module. Local Gradle invocation failed before compilation with `java.net.SocketException: Network is unreachable` during Gradle distribution download. No rebuilt APK, installation or playback success is claimed. A private GitHub Actions build recipe and signing script are supplied, but neither has run on GitHub.

An in-place update requires the existing signer's private key. A new owner-controlled key requires explicit migration; changing only the index version or re-signing a copied binary is not a compatibility repair. No secret keys or passwords are included.

## Remaining tests before calling this working

1. Approve creation/publication of the new candidate repository; confirm its real raw URL returns the exact metadata, index and APK bytes.
2. Run GitHub Actions and verify success on the published commit.
3. On Nekoyomi 0.20.6: add the anime repo and confirm extension list appears. Do not edit manga repos.
4. Download and install at least one standard and one NSFW extension, verify fingerprints and trust them as appropriate.
5. Exercise popular/latest, search, details, episodes and playback for each source you use. Record errors and app logs for targeted fixes.
6. Test a same-signer version upgrade on-device. Cross-provider duplicates are migrations, not guaranteed updates.
7. Confirm NSFW visibility toggles work. This checks app filtering, not the safety or legality of all content served by external sites.

No Android device/emulator, app acceptance, installation, source runtime or update-installation test was available in this session. Prepared workflows are not represented as successfully executed workflows.

Additional tooling verification: all Python scripts compile; actionlint 1.7.12 passed all four workflows. Negative tests rejected signer changes, version downgrades and changed APK bytes without a version increase. A per-package device-test matrix records every runtime check as not-tested.
