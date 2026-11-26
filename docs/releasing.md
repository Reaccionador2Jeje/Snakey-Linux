# Snakey release automation

The `Build and publish Snakey releases` workflow is
`.github/workflows/release-all.yml`.

## Publish all homebrew ROMs

1. Open **Actions → Build and publish Snakey releases**.
2. Select **Run workflow**.
3. Leave the release tag empty to create an automatic `snakey-preview-N`
   prerelease, or provide a tag such as `snakey-v0.1.0`.
4. Leave **Build the Slackware Live ISO** disabled unless the repository has
   a configured Snakey Slackware self-hosted runner.
5. Run the workflow. It builds NES, SNES, Game Boy, Game Boy Color, Game Boy
   Advance and Nintendo DS images, checks expected output files, generates
   SHA-256 checksums and publishes them as a GitHub prerelease.

A versioned release can also be triggered by pushing a `snakey-v*` tag:

```sh
git tag snakey-v0.1.0
git push origin snakey-v0.1.0
```

## Optional ISO build

GitHub-hosted Ubuntu runners are not treated as a supported liveslak build
host. The ISO job therefore runs only when explicitly requested and requires
a registered self-hosted runner with all of these labels:

- `self-hosted`
- `linux`
- `x64`
- `snakey-slackware`

That runner must be a supported Slackware x86_64 build host, have the
liveslak prerequisites and `git`, `python3`, and `makepkg` installed,
and have a complete local Slackware 15.0 mirror. Configure this repository
variable:

- `SNAKEY_SLACKWARE_REPO`: absolute path to the mirror root containing
  `slackware64-15.0/`.

Then run the workflow manually with **Build the Slackware Live ISO** enabled.
The ISO and its SHA-256 file are attached to the same prerelease as the ROMs.
Do not enable this option until the runner and mirror are ready.

## RetroArch testing

Load each downloaded ROM using a matching installed core:

| File | Suggested RetroArch core |
|---|---|
| `.nes` | Mesen or Nestopia |
| `.sfc` | Snes9x |
| `.gb` / `.gbc` | SameBoy or Gambatte |
| `.gba` | mGBA |
| `.nds` | melonDS |

The SNES, GBA and DS files are currently experimental generated images.
CI verifies that the files are produced and have expected basic sizes or
metadata; it does not certify that every core will boot them. The Game Boy
and Game Boy Color outputs are starter ROMs, not finished games. The release
includes `ROM-STATUS.md` and `SHA256SUMS.txt` to make those limitations
and file integrity clear.
