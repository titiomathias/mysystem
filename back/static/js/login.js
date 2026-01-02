const API_URL = "http://localhost:8000";

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
        document.getElementById("error").innerText = "Credenciais inválidas";
        return;
    }

    window.location.href = "index.html";
});
