const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
const platformGrid = $("#platform-grid");
const releaseList = $("#release-list");

$("#year").textContent = new Date().getFullYear();
const workerStatus = $("#worker-status");
getJson("/api/health").then((health) => {
  workerStatus.textContent = `API ${health.status.toUpperCase()}`;
  workerStatus.classList.add("online");
}).catch(() => {
  workerStatus.textContent = "API NO DISPONIBLE";
  workerStatus.classList.add("offline");
});
const navToggle = $("#nav-toggle");
navToggle.addEventListener("click", () => {
  const nav = $("#primary-nav");
  const open = nav.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", String(open));
});
$("#primary-nav").addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    $("#primary-nav").classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
  }
});

async function getJson(path) {
  const response = await fetch(path, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function loadPlatforms() {
  try {
    const data = await getJson("/api/targets");
    const targets = data.targets || [];
    if (!targets.length) throw new Error("El registro no contiene plataformas.");
    platformGrid.innerHTML = targets.map((target) => {
      const status = target.status || "unknown";
      const label = status === "buildable" ? "BUILDABLE" : status.toUpperCase();
      return `<article class="platform-card">
        <div class="platform-top"><span class="platform-code">${escapeHtml(target.id)}</span><span class="status ${status === "buildable" ? "buildable" : ""}">${escapeHtml(label)}</span></div>
        <h3>${escapeHtml(target.name)}</h3><p>${escapeHtml(target.output?.join(" / ") || "Formato por definir")} · ${target.linux_capable ? "Linux-capable" : "Homebrew nativo"}</p>
      </article>`;
    }).join("");
  } catch (error) {
    platformGrid.innerHTML = `<div class="loading-card">No se pudo cargar el registro. Puedes consultarlo directamente en <a href="https://github.com/Reaccionador2Jeje/Snakey-Linux/blob/main/platforms/targets.json">GitHub ↗</a>.</div>`;
  }
}

async function loadReleases() {
  try {
    const data = await getJson("/api/releases");
    if (!data.releases?.length) {
      releaseList.innerHTML = '<div class="loading-card">Todavía no hay Releases oficiales. La primera ROM pública aparecerá aquí cuando se publique una versión estable.</div>';
      return;
    }
    releaseList.innerHTML = data.releases.map((release) => {
      const assets = (release.assets || []).map((asset) =>
        `<a href="${escapeHtml(asset.browser_download_url)}" target="_blank" rel="noreferrer">${escapeHtml(asset.name)} ↓</a>`
      ).join(" ");
      return `<article class="release-row"><div><h3>${escapeHtml(release.name || release.tag_name)}</h3><p>${escapeHtml(release.tag_name)} · ${escapeHtml((release.published_at || "").slice(0, 10))}</p></div><div>${assets || `<a href="${escapeHtml(release.html_url)}" target="_blank" rel="noreferrer">Ver publicación ↗</a>`}</div></article>`;
    }).join("");
  } catch {
    releaseList.innerHTML = '<div class="loading-card">No se pudieron consultar las Releases. <a href="https://github.com/Reaccionador2Jeje/Snakey-Linux/releases">Abrir GitHub Releases ↗</a>.</div>';
  }
}
loadPlatforms();
loadReleases();