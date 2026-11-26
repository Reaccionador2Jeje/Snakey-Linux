# Snakey Linux website and Cloudflare Worker

The public site lives in `site/` and is served by the Cloudflare Worker in `worker/index.js`. The Worker serves static assets and exposes a small read-only JSON API.

## API

- `GET /api/health` — service health and identity.
- `GET /api/targets` — current console registry from `platforms/targets.json`.
- `GET /api/releases` — latest non-draft GitHub Releases and their downloadable assets.

The API is read-only, uses short cache headers, and does not require secrets or user data. Upstream GitHub failures return a JSON 502 response.

## Local development

Requirements: Node.js 20+.

    npm install
    npm test
    npm run dev

Open the local URL printed by Wrangler.

## Deploy to Cloudflare

1. Create a Cloudflare API token with permission to edit Workers and deploy the project.
2. Authenticate Wrangler using `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in your local environment.
3. Run:

       npm run check
       npm run deploy

The Worker name is `snakey-linux`; the default workers.dev subdomain is enabled. The GitHub Actions workflow also deploys automatically on pushes to `main` once both repository secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are configured. Without those secrets, CI still runs the tests and Wrangler dry-run, and skips deployment. Connect a custom domain in Cloudflare after the first deployment.

## NES preview releases

Pushing a tag matching `nes-v*` starts the dedicated NES release workflow. It installs cc65, generates a fresh NROM-256 ROM from the tagged source, validates the project, checks the 40,976-byte image, calculates SHA-256, and publishes a **GitHub prerelease** containing `SnakeyNES.nes` and `SHA256SUMS.txt`.

Example (after reviewing the commit you want to publish):

    git tag nes-v0.1.0
    git push origin nes-v0.1.0

The prerelease status is intentional: the ROM is build-verified but is not yet visually verified in RetroArch or on physical hardware. Do not treat a successful CI build as proof of emulator compatibility.

## ROM testing

The site includes the RetroArch guide for the NES NROM-256 build. CI artifacts are temporary; a permanent download appears in the Releases section only after a tagged GitHub Release contains the ROM asset.
