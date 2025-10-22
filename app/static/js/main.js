// app/static/js/main.js
const API = {
  register: (body) =>
    fetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then((r) => r.json()),

  login: (body) =>
    fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      credentials: "include",
    }).then((r) => r.json()),

  me: () =>
    fetch("/auth/me", { credentials: "include" }).then((r) =>
      r.ok ? r.json() : null
    ),

  quests: () =>
    fetch("/api/quests", { credentials: "include" }).then((r) => r.json()),

  submission: (body) =>
    fetch("/api/submissions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      credentials: "include",
    }).then((r) => r.json()),

  leaderboard: () =>
    fetch("/api/leaderboard", { credentials: "include" }).then((r) => r.json()),

  logout: () =>
    fetch("/auth/logout", { method: "POST", credentials: "include" }).then(
      (r) => r.json()
    ),
};

function qs(s) {
  return document.querySelector(s);
}

async function init() {
  // nav login/logout
  const me = await API.me();
  const navLogin = qs("#nav-login");
  const navLogout = qs("#nav-logout");
  if (navLogin && navLogout) {
    if (me) {
      navLogin.style.display = "none";
      navLogout.style.display = "inline";
    } else {
      navLogin.style.display = "inline";
      navLogout.style.display = "none";
    }
    navLogout.addEventListener("click", async (e) => {
      e.preventDefault();
      await API.logout();
      location.href = "/";
    });
  }

  // register
  const regForm = qs("#register-form");
  if (regForm)
    regForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(regForm).entries());
      const res = await API.register(body);
      qs("#register-msg").textContent = res.error
        ? res.error
        : "Registered! You can log in now.";
    });

  // login
  const loginForm = qs("#login-form");
  if (loginForm)
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(loginForm).entries());
      const res = await API.login(body);
      if (res.error) qs("#login-msg").textContent = res.error;
      else location.href = "/quests";
    });

  // ---- Quests list + dropdown population ----
  const list = qs("#quests-list");
  const select = qs("#quest-select");

  if (list) {
    const rows = await API.quests();

    // Render each quest as a card with visible #id and a "Use" button
    list.innerHTML =
      rows && rows.length
        ? rows
            .map(
              (r) => `
        <div class="card" style="margin:.4rem 0;">
          <div><strong>${r.title}</strong> <small>#${r.id}</small> — ${r.description}</div>
          <div><small>(${r.starts_on} → ${r.ends_on}) • ${r.points} pts</small></div>
          <button type="button" class="pick-quest" data-id="${r.id}">Use</button>
        </div>
      `
            )
            .join("")
        : "<em>No quests yet.</em>";

    // Populate the <select> used by the submission form
    if (select) {
      if (rows && rows.length) {
        select.innerHTML =
          '<option value="" disabled selected>Select a quest…</option>' +
          rows
            .map(
              (r) =>
                `<option value="${r.id}">${r.title} (#${r.id}) — ${r.points} pts</option>`
            )
            .join("");
        select.disabled = false;
      } else {
        select.innerHTML =
          '<option value="" disabled selected>No quests available</option>';
        select.disabled = true;
      }
    }

    // Clicking "Use" sets the dropdown value to that quest
    list.addEventListener("click", (e) => {
      const btn = e.target.closest(".pick-quest");
      if (!btn) return;
      if (select) {
        select.value = String(btn.dataset.id);
        select.dispatchEvent(new Event("change"));
        select.focus();
      }
    });
  }

  // ---- Submission form ----
  const subForm = qs("#submission-form");
  if (subForm)
    subForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(subForm).entries());

      const user = await API.me();
      if (!user)
        return (qs("#submission-msg").textContent = "Login first.");

      const qid = Number(body.quest_id);
      if (!qid)
        return (qs("#submission-msg").textContent = "Select a quest first.");

      body.quest_id = qid;
      body.user_id = user.id;

      const res = await API.submission(body);
      qs("#submission-msg").textContent = res.error
        ? res.error
        : `Submitted! id=${res.id}`;
    });

  // ---- Leaderboard table (if present on page) ----
  const board = qs("#board tbody");
  if (board) {
    const rows = await API.leaderboard();
    board.innerHTML = rows
      .map((r) => `<tr><td>${r.user}</td><td>${r.points}</td></tr>`)
      .join("");
  }
}

window.addEventListener("DOMContentLoaded", init);
