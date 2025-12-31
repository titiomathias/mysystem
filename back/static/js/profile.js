const API_URL = "http://localhost:8000";

async function loadProfile() {
    const res = await fetch(`${API_URL}/me`, {
        credentials: "include"
    });

    if (!res.ok) {
        window.location.href = "/login.html";
        return;
    }

    const data = await res.json();
    const profile = data.profile;

    document.getElementById("username").innerText = profile.username;
    document.getElementById("level").innerText = `Nível ${profile.level}`;

    document.getElementById("str").innerText = profile.attributes.strength;
    document.getElementById("agi").innerText = profile.attributes.agility;
    document.getElementById("con").innerText = profile.attributes.stamina;
    document.getElementById("wis").innerText = profile.attributes.wisdom;
    document.getElementById("int").innerText = profile.attributes.intelligence;
    document.getElementById("cha").innerText = profile.attributes.charisma;

    // XP vem do backend
    document.getElementById("xp-text").innerText =
        `${profile.current_xp} / ${profile.next_level_xp}`;
}

async function logout() {
    await fetch(`${API_URL}/logout`, { credentials: "include" });
    window.location.href = "/login.html";
}

loadProfile();
