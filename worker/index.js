const REPO = "Reaccionador2Jeje/Snakey-Linux";
const JSON_HEADERS = { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=60, s-maxage=300", "x-content-type-options": "nosniff" };

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}

async function githubJson(url) {
  const response = await fetch(url, {
    headers: { Accept: "application/vnd.github+json", "User-Agent": "Snakey-Linux-Worker" },
    cf: { cacheTtl: 300, cacheEverything: true }
  });
  if (!response.ok) throw new Error(`GitHub API returned ${response.status}`);
  return response.json();
}

async function handleApi(request) {
  const url = new URL(request.url);
  if (request.method !== "GET" && request.method !== "HEAD") {
    return json({ error: "method_not_allowed", message: "Only GET and HEAD are supported." }, 405);
  }
  if (url.pathname === "/api/health") {
    return json({ status: "ok", service: "snakey-linux-worker", repository: REPO, apiVersion: 1 });
  }
  if (url.pathname === "/api/targets") {
    try {
      const registry = await githubJson(`https://raw.githubusercontent.com/${REPO}/main/platforms/targets.json`);
      return json({ project: registry.project, schema_version: registry.schema_version, targets: registry.targets || [] });
    } catch {
      return json({ error: "upstream_unavailable", message: "The platform registry is temporarily unavailable." }, 502);
    }
  }
  if (url.pathname === "/api/releases") {
    try {
      const releases = await githubJson(`https://api.github.com/repos/${REPO}/releases?per_page=5`);
      return json({ releases: releases.filter((release) => !release.draft).map((release) => ({
        name: release.name, tag_name: release.tag_name, published_at: release.published_at,
        html_url: release.html_url,
        assets: (release.assets || []).map((asset) => ({ name: asset.name, browser_download_url: asset.browser_download_url, size: asset.size }))
      })) });
    } catch {
      return json({ error: "upstream_unavailable", message: "Release information is temporarily unavailable." }, 502);
    }
  }
  return json({ error: "not_found" }, 404);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/api/")) return handleApi(request);
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405, headers: { Allow: "GET, HEAD" } });
    }
    return env.ASSETS.fetch(request);
  }
};

export { handleApi };