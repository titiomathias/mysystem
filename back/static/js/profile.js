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

    document.getElementById("str").innerText = profile.attributes.str;
    document.getElementById("agi").innerText = profile.attributes.agi;
    document.getElementById("con").innerText = profile.attributes.con;
    document.getElementById("wis").innerText = profile.attributes.wis;
    document.getElementById("int").innerText = profile.attributes.int;
    document.getElementById("cha").innerText = profile.attributes.cha;

    document.getElementById("xp-text").innerText =
        `${profile.current_xp} / ${profile.next_level_xp}`;

    renderXP(profile.current_xp, profile.next_level_xp);
}

async function logout() {
    await fetch(`${API_URL}/logout`, { credentials: "include" });
    window.location.href = "/login.html";
}

function renderXP(currentXP, nextLevelXP) {
    const circle = document.getElementById("xp-circle");
    const text = document.getElementById("xp-text");

    const percent = Math.min(currentXP / nextLevelXP, 1);
    const degrees = percent * 360;

    circle.style.background = `
        conic-gradient(
            #6366f1 ${degrees}deg,
            #1e293b ${degrees}deg
        )
    `;

    text.innerText = `${currentXP} / ${nextLevelXP}`;
}


loadProfile();