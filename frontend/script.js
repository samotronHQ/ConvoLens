async function analyzeChat() {
  const chatInput = document.getElementById("chatInput");
  const results = document.getElementById("results");
  const chat = chatInput.value;

  if (!chat.trim()) {
    alert("Paste some chat first.");
    return;
  }

  results.classList.remove("hidden");
  results.innerHTML = `
    <div class="card">
      <h3>Analyzing...</h3>
      <p>AI is reading the conversation.</p>
    </div>
  `;

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ chat })
    });

    if (!response.ok) {
      throw new Error("Stand ability failed to activate");
    }

    const data = await response.json();
    const analysis = data.analysis;

    results.innerHTML = `
      <div class="summary-card">
        <h3>summary</h3>
        <p>${analysis.summary}</p>

        <div class="participant-note">
          ${analysis.participants?.length || 0} participants<br>
          ${analysis.participants?.join(", ") || "Unknown"}
        </div>
      </div>

      <div class="card">
        <h3>the vibe •</h3>
        ${
          Object.entries(analysis.emotional_tone || {}).map(([person, info]) => `
            <div class="vibe-item">
              <div class="avatar">${person[0]}</div>
              <div>
                <strong>${info.tone || "unknown"}</strong>
                <p>${info.explanation || ""}</p>
              </div>
            </div>
          `).join("")
        }
      </div>

      <div class="card">
        <h3>numbers</h3>
        <div class="metrics">
          <p>effort <span><span class="metric-number">${analysis.response_effort || 0}</span> / 1</span></p>
          <p>initiation <span><span class="metric-number">${analysis.initiation_ratio || 0}</span></span></p>
        </div>

        <h3>imbalance</h3>
        <div class="imbalance-grid">
          <p>status <span>${analysis.imbalance?.status || "Unknown"}</span></p>
          <p>dominant <span>${analysis.imbalance?.dominant_participant || "None detected"}</span></p>
          <p>least engaged <span>${analysis.imbalance?.least_engaged || "None detected"}</span></p>
        </div>
      </div>

      <div class="card">
        <h3>the pattern i see ✤</h3>
        <strong class="pattern-name">${analysis.communication_pattern?.pattern || "Not detected"}</strong>
        <p>${analysis.communication_pattern?.explanation || ""}</p>
      </div>

      <div class="off-ok">
        <div class="card">
          <h3>🚩 what feels off</h3>
          ${
            analysis.red_flags?.length
              ? analysis.red_flags.map(flag => `
                  <div class="flag red">
                    <strong>${flag.label || "Concern"} (${flag.severity || "Medium"})</strong>
                    <p>${flag.explanation || ""}</p>
                    <em>"${flag.evidence || ""}"</em>
                  </div>
                `).join("")
              : "<p>nothing obvious</p>"
          }
        </div>

        <div class="card">
          <h3>🍃 what feels okay</h3>
          ${
            analysis.green_flags?.length
              ? analysis.green_flags.map(flag => `
                  <div class="flag green">
                    <strong>${flag.label || "Positive sign"}</strong>
                    <p>${flag.explanation || ""}</p>
                    <em>"${flag.evidence || ""}"</em>
                  </div>
                `).join("")
              : "<p>nothing stands out</p>"
          }
        </div>
      </div>
    `;

  } catch (error) {
    console.error(error);

    results.innerHTML = `
      <div class="card">
        <h3>Error</h3>
        <p>Something went wrong. Stand ability failed to activate.</p>
      </div>
    `;
  }
}