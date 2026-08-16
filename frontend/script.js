const API_URL = "http://127.0.0.1:8000";

async function analyzeScenario() {
  const text = document.getElementById("scenario").value;
  const nickname = document.getElementById("nickname").value || "Anonim";

  if (text.length < 10) {
    alert("Lütfen daha detaylı bir senaryo yaz.");
    return;
  }

  const btn = document.getElementById("analyzeBtn");
  btn.disabled = true;
  btn.innerText = "Analiz ediliyor... ⏳";

  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text, nickname }),
    });

    const data = await response.json();

    document.getElementById("verdict").innerText = data.verdict;
    document.getElementById("commentary").innerText = data.commentary;
    document.getElementById("meterFill").style.width = data.toxic_percentage + "%";
    document.getElementById("meterLabel").innerText = "%" + data.toxic_percentage + " toxic";
    document.getElementById("card").src = API_URL + data.card_url;

    document.getElementById("result").classList.remove("hidden");
  } catch (err) {
    alert("HATA OLUŞTU: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerText = "Analiz Et ✨";
  }
}

function downloadCard() {
  const link = document.createElement("a");
  link.href = document.getElementById("card").src;
  link.download = "iliski-raporu.png";
  link.click();
}