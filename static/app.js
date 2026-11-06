const form = document.getElementById("cat-form");
const message = document.getElementById("message");
const rows = document.getElementById("cat-rows");

const COLUMNS = ["id", "name", "breed", "age", "gender", "color", "owner_name", "owner_phone", "created_at"];

function showMessage(text, ok) {
    message.textContent = text;
    message.className = ok ? "ok" : "err";
}

async function loadCats() {
    const res = await fetch("/api/cats");
    const cats = await res.json();
    rows.replaceChildren(...cats.map((cat) => {
        const tr = document.createElement("tr");
        for (const col of COLUMNS) {
            const td = document.createElement("td");
            td.textContent = cat[col] ?? "";
            tr.appendChild(td);
        }
        return tr;
    }));
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    try {
        const res = await fetch("/api/cats", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const body = await res.json();
        if (!res.ok) {
            showMessage(body.errors.join(" "), false);
            return;
        }
        showMessage(`${data.name} registered (ID ${body.id}).`, true);
        form.reset();
        loadCats();
    } catch (err) {
        showMessage("Could not reach the server.", false);
    }
});

loadCats();