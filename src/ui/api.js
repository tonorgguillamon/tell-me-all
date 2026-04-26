export const API = "http://localhost:8000";

// ── Auth helpers ──────────────────────────────────────────────
export async function logout() {
  await fetch(`${API}/auth/logout`, { method: "POST", credentials: "include" }).catch(() => {});
  window.location.href = "/ui/index.html";
}

// Uses raw fetch — bypasses request() so a 401 never triggers auto-logout.
// Safe to call on any page including index.html.
export async function requireAuth() {
  const res = await fetch(`${API}/auth/me`, { credentials: "include" });
  if (!res.ok) {
    window.location.href = "/ui/index.html";
    throw new Error("Not authenticated");
  }
}

// ── Core fetch wrapper ────────────────────────────────────────
async function request(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    ...options,
    credentials: "include",   // always send the HttpOnly cookie
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (res.status === 401) { await logout(); return; }
  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) throw new Error(data?.detail || "Request failed");
  return data;
}

// ── Auth ──────────────────────────────────────────────────────
export async function register(email, password) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email, password) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getMe() {
  return request("/auth/me");
}

// ── Dashboards ────────────────────────────────────────────────
export async function getDashboards() {
  return request("/api/v1/dashboards");
}

export async function createDashboard(name) {
  return request("/api/v1/dashboards", {
    method: "POST",
    body: JSON.stringify({ name }),
  });
}

export async function deleteDashboard(id) {
  return request(`/api/v1/dashboards/${id}`, { method: "DELETE" });
}

// ── Cards ─────────────────────────────────────────────────────
export async function getCards(dashboardId) {
  return request(`/api/v1/dashboards/${dashboardId}/cards`);
}

export async function createCard(dashboardId, title, topic, role, creativity) {
  return request(`/api/v1/dashboards/${dashboardId}/cards`, {
    method: "POST",
    body: JSON.stringify({ dashboard_id: dashboardId, title, topic, role, creativity }),
  });
}

export async function updateCard(cardId, data) {
  return request(`/api/v1/cards/${cardId}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function deleteCard(cardId) {
  return request(`/api/v1/cards/${cardId}`, { method: "DELETE" });
}

// ── Sources ───────────────────────────────────────────────────
export async function getSources() {
  return request("/api/v1/sources");
}

export async function createSource(sourceType, name, configJson = {}) {
  return request("/api/v1/sources", {
    method: "POST",
    body: JSON.stringify({ source_type: sourceType, name, config_json: configJson }),
  });
}

export async function getSourcesForCard(cardId) {
  return request(`/api/v1/cards/${cardId}/sources`);
}

export async function attachSource(cardId, sourceId) {
  return request(`/api/v1/cards/${cardId}/sources/${sourceId}`, { method: "POST" });
}

export async function updateSource(id, data) {
  return request(`/api/v1/sources/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function deleteSource(id) {
  return request(`/api/v1/sources/${id}`, { method: "DELETE" });
}

// ── Events ────────────────────────────────────────────────────
export async function getEventsForCard(cardId) {
  return request(`/api/v1/cards/${cardId}/events`);
}

// ── UI helpers ────────────────────────────────────────────────
export function showToast(msg, isError = false) {
  let t = document.getElementById("toast");
  if (!t) {
    t = document.createElement("div");
    t.id = "toast";
    t.className = "toast";
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.className = "toast" + (isError ? " error" : "");
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 3000);
}

export function openModal(id) {
  document.getElementById(id).classList.add("open");
}

export function closeModal(id) {
  document.getElementById(id).classList.remove("open");
}
