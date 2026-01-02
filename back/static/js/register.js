document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const errorEl = document.getElementById("error");
    errorEl.textContent = "";

    const data = {
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    try {
        const res = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            errorEl.textContent = result.detail || "Erro ao registrar";
            return;
        }

        // Registro OK → vai direto pro app
        window.location.href = "/app/index.html";

    } catch (err) {
        errorEl.textContent = "Erro de conexão com o servidor";
    }
});
