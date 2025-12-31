const API_URL = "http://localhost:8000";

async function loadProfile() {
    const res = await fetch(`${API_URL}/me`, {
        credentials: "include"
    });

    if (!res.ok) {
        alert("Não autenticado");
        window.location.href = "/login.html";
        return;
    }

    const data = await res.json();

    document.getElementById("username").innerText = data.profile.username;
    document.getElementById("level").innerText = `Level ${data.profile.level}`;
}

async function loadTasks() {
    const res = await fetch(`${API_URL}/tasks`, {
        credentials: "include"
    });

    if (!res.ok) {
        alert("Erro ao carregar tarefas");
        return;
    }

    const data = await res.json();
    renderTasks(data);
}

function renderTasks(tasks) {
    const urgent = document.getElementById("urgent-tasks");
    const daily = document.getElementById("daily-tasks");
    const weekly = document.getElementById("weekly-tasks");

    urgent.innerHTML = "";
    daily.innerHTML = "";
    weekly.innerHTML = "";

    tasks.forEach(task => {
        const el = document.createElement("div");
        el.className = "task";

        el.innerHTML = `
            <strong>${task.name}</strong>
            <small>${task.category}</small>
        `;

        el.onclick = () => completeTask(task.id);

        if (task.frequency === "daily") {
            daily.appendChild(el);
        } else if (task.frequency === "weekly") {
            weekly.appendChild(el);
        } else {
            urgent.appendChild(el);
        }
    });
}


async function completeTask(taskId) {
    const res = await fetch(`${API_URL}/tasks/${taskId}/complete`, {
        method: "POST",
        credentials: "include"
    });

    if (!res.ok) {
        const err = await res.json();
        alert(err.detail || "Erro ao completar task");
        return;
    }

    const data = await res.json();
    alert(`+${data.xp_earned} XP | Streak: ${data.streak}`);

    await loadProfile();
    await loadTasks();
}

async function completeTask(taskId) {
    const res = await fetch(`${API_URL}/tasks/${taskId}/complete`, {
        method: "POST",
        credentials: "include"
    });

    if (!res.ok) {
        const err = await res.json();
        alert(err.detail || "Erro ao completar task");
        return;
    }

    const data = await res.json();
    alert(`+${data.xp_earned} XP | Streak: ${data.streak}`);

    await loadProfile();
    await loadTasks();
}

loadTasks();
loadProfile();