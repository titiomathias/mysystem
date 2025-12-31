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

function openTaskModal(task) {
    document.getElementById("modal-title").innerText = task.name;
    document.getElementById("modal-description").innerText = task.description || "Sem descrição";
    document.getElementById("modal-category").innerText = task.category;
    document.getElementById("modal-xp").innerText = task.base_xp;
    document.getElementById("modal-frequency").innerText = task.frequency;
    document.getElementById("modal-streak").innerText = task.streak_count ?? 0;

    const attrList = document.getElementById("modal-attributes");
    attrList.innerHTML = "";

    if (task.attributes.length === 0) {
        attrList.innerHTML = "<li>Nenhum atributo afetado</li>";
    } else {
        task.attributes.forEach(attr => {
            const li = document.createElement("li");
            li.innerText = `${attr.attribute.toUpperCase()} +${attr.value}`;
            attrList.appendChild(li);
        });
    }

    document.getElementById("task-modal").classList.remove("hidden");
    document.getElementById("task-modal").classList.add("flex");
}

function closeModal() {
    const modal = document.getElementById("task-modal");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
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
        el.className = `
            flex items-center gap-3
            bg-slate-700
            border border-slate-600
            rounded-xl
            px-4 py-3
            cursor-pointer
            hover:bg-slate-600
            transition
        `;

        el.innerHTML = `
            <input
                type="checkbox"
                ${task.completed ? "checked" : ""}
                class="accent-indigo-500"
            />

            <div class="flex-1">
                <strong>${task.name}</strong>
                <p class="text-xs text-slate-400">${task.category}</p>
            </div>

            <button
                class="text-slate-400 hover:text-white"
                title="Detalhes"
            >
                ℹ️
            </button>
        `;

        // ✔️ completar tarefa (card ou checkbox)
        el.addEventListener("click", () => completeTask(task.id));

        // ℹ️ abrir modal (sem completar!)
        const infoBtn = el.querySelector("button");
        infoBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            openTaskModal(task);
        });

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