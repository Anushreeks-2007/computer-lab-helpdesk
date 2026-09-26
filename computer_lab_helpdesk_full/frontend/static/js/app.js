```javascript
let token = localStorage.getItem("token");

const email = document.getElementById("email");
const password = document.getElementById("password");
const loginForm = document.getElementById("loginForm");
const loginMsg = document.getElementById("loginMsg");
const loginCard = document.getElementById("loginCard");

const appArea = document.getElementById("appArea");
const ticketForm = document.getElementById("ticketForm");
const category = document.getElementById("category");
const deviceId = document.getElementById("deviceId");
const description = document.getElementById("description");
const ticketMsg = document.getElementById("ticketMsg");
const tickets = document.getElementById("tickets");

const H = () => ({
    "Content-Type": "application/json",
    ...(token ? { "Authorization": "Bearer " + token } : {})
});

async function login(e) {
    e.preventDefault();

    let r = await fetch("/api/auth/login", {
        method: "POST",
        headers: H(),
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });

    let d = await r.json();

    if (!r.ok) {
        loginMsg.innerHTML = '<div class="alert alert-danger">' + d.error + '</div>';
        return;
    }

    token = d.token;
    localStorage.setItem("token", token);
    show();
}

async function load() {
    let r = await fetch("/api/tickets", {
        headers: H()
    });

    let d = await r.json();

    tickets.innerHTML = d.map(t =>
        '<div class="card ticket p-3">' +
        '<b>' + t.ticket_no + '</b> ' +
        '<span class="badge text-bg-secondary">' + t.status + '</span>' +
        '<div>' + t.description + '</div>' +
        '<small>' + t.category + ' · ' + t.priority + ' · ' + (t.lab_name || "-") + '</small>' +
        '</div>'
    ).join("") || "<p>No tickets yet.</p>";
}

async function create(e) {
    e.preventDefault();

    let r = await fetch("/api/tickets", {
        method: "POST",
        headers: H(),
        body: JSON.stringify({
            category: category.value,
            device_id: deviceId.value || null,
            description: description.value
        })
    });

    let d = await r.json();

    ticketMsg.innerHTML =
        '<div class="alert alert-' +
        (r.ok ? "success" : "danger") +
        '">' +
        (d.message || d.error) +
        (d.priority ? " — " + d.priority : "") +
        '</div>';

    if (r.ok) {
        description.value = "";
        deviceId.value = "";
        load();
    }
}

function show() {
    loginCard.classList.add("d-none");
    appArea.classList.remove("d-none");
    load();
}

function logout() {
    localStorage.clear();
    location.reload();
}

loginForm.addEventListener("submit", login);
ticketForm.addEventListener("submit", create);

if (token) {
    show();
}
```
