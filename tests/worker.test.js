import test from "node:test";
import assert from "node:assert/strict";
import worker, { handleApi } from "../worker/index.js";

test("health endpoint reports service identity", async () => {
  const response = await handleApi(new Request("https://snakey.test/api/health"));
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.status, "ok");
  assert.equal(body.service, "snakey-linux-worker");
});

test("unknown API routes return JSON 404", async () => {
  const response = await handleApi(new Request("https://snakey.test/api/nope"));
  assert.equal(response.status, 404);
  assert.equal((await response.json()).error, "not_found");
});

test("API rejects write methods", async () => {
  const response = await handleApi(new Request("https://snakey.test/api/health", { method: "POST" }));
  assert.equal(response.status, 405);
});

test("worker serves non-API requests from static assets", async () => {
  const expected = new Response("site");
  const response = await worker.fetch(new Request("https://snakey.test/"), {
    ASSETS: { fetch: async () => expected }
  });
  assert.equal(await response.text(), "site");
});

test("worker routes API requests without static asset binding", async () => {
  const response = await worker.fetch(new Request("https://snakey.test/api/health"), {});
  assert.equal(response.status, 200);
});

test("target and release routes are registered", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url) => new Response(JSON.stringify(
    String(url).includes("targets.json")
      ? { project: "Snakey Linux", schema_version: 1, targets: [{ id: "nes" }] }
      : [{ name: "v0.1.0", tag_name: "v0.1.0", assets: [] }]
  ), { status: 200, headers: { "content-type": "application/json" } });
  try {
    const targets = await handleApi(new Request("https://snakey.test/api/targets"));
    assert.equal((await targets.json()).targets[0].id, "nes");
    const releases = await handleApi(new Request("https://snakey.test/api/releases"));
    assert.equal((await releases.json()).releases[0].tag_name, "v0.1.0");
  } finally {
    globalThis.fetch = originalFetch;
  }
});