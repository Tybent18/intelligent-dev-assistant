const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const canvas = $("#starfield");
const context = canvas.getContext("2d");
let particles = [];

function resizeField() {
  canvas.width = innerWidth * devicePixelRatio;
  canvas.height = innerHeight * devicePixelRatio;
  context.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  particles = Array.from({ length: Math.min(130, Math.floor(innerWidth / 8)) }, () => ({
    x: Math.random() * innerWidth,
    y: Math.random() * innerHeight,
    z: Math.random() * 1 + .2,
    speed: Math.random() * .18 + .04
  }));
}

function drawField() {
  context.clearRect(0, 0, innerWidth, innerHeight);
  for (const particle of particles) {
    particle.y -= particle.speed * particle.z;
    if (particle.y < 0) particle.y = innerHeight;
    context.fillStyle = `rgba(77,231,255,${.12 + particle.z * .36})`;
    context.fillRect(particle.x, particle.y, particle.z * 1.4, particle.z * 1.4);
  }
  requestAnimationFrame(drawField);
}
addEventListener("resize", resizeField);
resizeField();
drawField();

function updateClock() {
  const now = new Date();
  $("#clock").textContent = `ONLINE // ${now.toLocaleTimeString([], { hour12: false })}`;
}
setInterval(updateClock, 1000);
updateClock();

function addMessage(author, text, kind = "obsidian") {
  const message = document.createElement("div");
  message.className = `message ${kind}`;
  const label = document.createElement("span");
  label.textContent = author;
  message.append(label, document.createTextNode(text));
  $("#conversation").append(message);
  $("#conversation").scrollTop = $("#conversation").scrollHeight;
}

function speak(text) {
  if (!("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = .94;
  utterance.pitch = .82;
  utterance.volume = .75;
  speechSynthesis.speak(utterance);
}

function clearFocus() { $$("[data-panel]").forEach(panel => panel.classList.remove("focus-panel")); }
function applyActions(actions = []) {
  clearFocus();
  for (const action of actions) {
    if (action.type === "focus") {
      const panel = $(`[data-panel="${action.target}"]`);
      if (panel) panel.classList.add("focus-panel");
    }
    if (action.type === "pulse") {
      const core = $("#holoCore");
      core.classList.remove("core-pulse");
      requestAnimationFrame(() => core.classList.add("core-pulse"));
    }
    if (action.type === "mode") $("#labShell").classList.toggle("expanded", action.target === "expanded");
    if (action.type === "render_diagnostics") renderDiagnostics(action.payload);
  }
}

function renderDiagnostics(payload) {
  const sample = payload.files.slice(0, 4).map(file => `${file.status === "valid" ? "✓" : "!"} ${file.path}`).join("<br>");
  $("#diagnosticContent").innerHTML = `${payload.valid} VALID // ${payload.errors} ERRORS<br>${sample}`;
}

async function execute(command) {
  const text = command.trim();
  if (!text) return;
  addMessage("YOU", text, "user");
  $("#commandInput").value = "";
  try {
    const response = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: text })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Command failed");
    addMessage("OBSIDIAN", result.response);
    applyActions(result.actions);
    $("#commandMetric").textContent = String(Number($("#commandMetric").textContent || 0) + 1);
    speak(result.response);
  } catch (error) {
    addMessage("SYSTEM", `Connection fault: ${error.message}`);
  }
}

$("#commandForm").addEventListener("submit", event => {
  event.preventDefault();
  execute($("#commandInput").value);
});
$$('[data-command]').forEach(button => button.addEventListener("click", () => execute(button.dataset.command)));

async function loadStatus() {
  try {
    const response = await fetch("/api/status");
    const status = await response.json();
    $("#stateMetric").textContent = status.state;
    $("#fileMetric").textContent = status.files_indexed;
    $("#moduleMetric").textContent = status.python_modules;
    $("#commandMetric").textContent = status.commands_processed;
    $("#modeLabel").textContent = status.mode.replaceAll("_", " ");
  } catch {
    $("#stateMetric").textContent = "OFFLINE";
  }
}
loadStatus();

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.addEventListener("start", () => $("#micButton").classList.add("mic-live"));
  recognition.addEventListener("end", () => $("#micButton").classList.remove("mic-live"));
  recognition.addEventListener("result", event => execute(event.results[0][0].transcript));
  $("#micButton").addEventListener("click", () => recognition.start());
} else {
  $("#micButton").disabled = true;
  $("#micButton").title = "Voice recognition is unavailable in this browser";
}

