
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Minesweeper",
    page_icon="💣",
    layout="wide",
)

st.markdown("""
<style>
    #MainMenu, header, footer {
        visibility: hidden;
    }
    .stApp {
        background: #c0c0c0;
    }
    .block-container {
        max-width: 900px;
        padding: 8px 5px 20px;
    }
    iframe {
        display: block;
        width: 100%;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    background: #c0c0c0;
    color: #111;
    font-family: Tahoma, Arial, sans-serif;
    font-size: 13px;
}

button, select { font: inherit; }
button { cursor: pointer; }

.app {
    width: 100%;
    max-width: 720px;
    margin: auto;
    padding: 5px;
}

.window {
    background: #c0c0c0;
    border: 2px solid;
    border-color: white #555 #555 white;
    padding: 8px;
}

.title {
    background: navy;
    color: white;
    font-weight: bold;
    font-size: 16px;
    padding: 9px;
    margin-bottom: 8px;
}

.toolbar, .topbar, .actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 7px;
    margin-bottom: 8px;
}

select, .btn {
    background: #c0c0c0;
    border: 2px solid;
    border-color: white #555 #555 white;
    border-radius: 0;
    color: #111;
    min-height: 34px;
    padding: 5px 8px;
}

select {
    flex: 1;
    min-width: 0;
}

.btn:active, .btn.active {
    border-color: #555 white white #555;
}

.counter {
    min-width: 55px;
    padding: 5px 4px;
    background: #111;
    color: #ff2929;
    border: 2px solid;
    border-color: #555 white white #555;
    font-family: "Courier New", monospace;
    font-size: 23px;
    font-weight: bold;
    text-align: center;
    font-variant-numeric: tabular-nums;
}

.face {
    font-size: 23px;
    min-width: 43px;
    min-height: 39px;
    padding: 0 5px;
}

#message {
    padding: 8px;
    margin-bottom: 8px;
    background: #d4d0c8;
    border: 1px solid #888;
    line-height: 1.5;
    overflow-wrap: anywhere;
}

.board-frame {
    width: 100%;
    overflow: auto;
    padding: 4px;
    background: #808080;
    border: 3px solid;
    border-color: #555 white white #555;
    overscroll-behavior: contain;
}

#board {
    display: grid;
    gap: 0;
    margin: 0 auto;
    width: max-content;
    touch-action: pan-x pan-y;
    user-select: none;
    -webkit-user-select: none;
}

.cell {
    display: flex;
    align-items: center;
    justify-content: center;
    width: var(--cell);
    height: var(--cell);
    min-width: 0;
    min-height: 0;
    margin: 0;
    padding: 0;
    overflow: hidden;
    border-radius: 0;
    border: 2px solid;
    border-color: white #777 #777 white;
    background: #c0c0c0;
    box-shadow: none;
    font-family: Arial, sans-serif;
    font-size: var(--font-size);
    line-height: 1;
    font-weight: bold;
    text-align: center;
    -webkit-tap-highlight-color: transparent;
}

.cell.open {
    border: 1px solid #999;
    background: #c0c0c0;
    cursor: default;
}

.cell.n1 { color: blue; }
.cell.n2 { color: green; }
.cell.n3 { color: red; }
.cell.n4 { color: navy; }
.cell.n5 { color: maroon; }
.cell.n6 { color: teal; }
.cell.n7 { color: #111; }
.cell.n8 { color: #666; }
.cell.mine { background: #ff4444; }
.cell.exploded { background: red; }
.cell.wrong { background: #ffaaaa; }

.actions .btn { flex: 1; }

.stats {
    margin-top: 8px;
    padding: 8px;
    background: #d4d0c8;
    border: 1px solid #888;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 5px;
    margin-top: 6px;
}

.stat {
    text-align: center;
    padding: 7px 2px;
    background: #c0c0c0;
    border: 1px solid #999;
    overflow-wrap: anywhere;
}

.stat-label {
    font-size: 11px;
    margin-bottom: 5px;
}

.stat-value {
    font-size: 16px;
    font-weight: bold;
}

.hint {
    margin-top: 8px;
    color: #444;
    font-size: 11px;
    line-height: 1.6;
}

@media (max-width: 360px) {
    .window { padding: 5px; }
    .counter { min-width: 45px; font-size: 20px; }
    .face { min-width: 36px; font-size: 20px; }
    .toolbar, .topbar, .actions { gap: 4px; }
    .btn, select { padding: 4px; }
}
</style>
</head>
<body>
<div class="app">
<div class="window">

    <div class="title">💣 MINESWEEPER</div>

    <div class="toolbar">
        <select id="difficulty" aria-label="Độ khó">
            <option value="easy">Dễ — 9 × 9 · 10 mìn</option>
            <option value="medium">Trung bình — 16 × 16 · 40 mìn</option>
            <option value="hard">Khó — 30 × 16 · 99 mìn</option>
        </select>
        <button class="btn" id="soundBtn">🔊 Âm thanh</button>
    </div>

    <div class="topbar">
        <div class="counter" id="mineCounter">010</div>
        <button class="btn face" id="reset">🙂</button>
        <div class="counter" id="clock">000</div>
    </div>

    <div id="message" aria-live="polite">
        Chọn một ô để bắt đầu!
    </div>

    <div class="board-frame" id="boardFrame">
        <div id="board"></div>
    </div>

    <div class="actions">
        <button class="btn" id="flagMode">🚩 Cắm cờ: TẮT</button>
        <button class="btn" id="newGame">↻ Ván mới</button>
    </div>

    <div class="stats">
        <strong>📊 Thống kê độ khó hiện tại</strong>
        <div class="stats-grid">
            <div class="stat">
                <div class="stat-label">Ván thắng</div>
                <div class="stat-value" id="wins">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">Ván thua</div>
                <div class="stat-value" id="losses">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">Kỷ lục</div>
                <div class="stat-value" id="best">—</div>
            </div>
        </div>
    </div>

    <div class="hint">
        Máy tính: nhấp trái để mở, nhấp phải để cắm cờ.
        <br>
        Điện thoại: chạm để mở, nhấn giữ để cắm cờ.
        <br>
        Bấm ô số đã mở để mở nhanh các ô xung quanh khi số cờ khớp.
        <br>
        Lượt đầu và 8 ô xung quanh luôn an toàn.
        <br>
        Chế độ tự do: chơi liên tục, không giới hạn số ván.
    </div>
</div>
</div>

<script>
(function () {
"use strict";

const $ = id => document.getElementById(id);

const LEVELS = {
    easy:   { rows: 9, cols: 9, mines: 10 },
    medium: { rows: 16, cols: 16, mines: 40 },
    hard:   { rows: 16, cols: 30, mines: 99 }
};

let level = "easy";
let rows = 9, cols = 9, mineTotal = 10;
let cells = [];
let flagCount = 0, openedCount = 0;
let started = false, ended = false, flagMode = false;
let elapsed = 0, timerId = null;
let exploded = -1;
let soundOn = true;
let audio = null;
let holdTimer = null;
let suppressClickUntil = 0;

function say(text) {
    $("message").textContent = text;
}

function timeText(n) {
    return String(Math.min(n, 999)).padStart(3, "0");
}

function stopTimer() {
    if (timerId !== null) {
        clearInterval(timerId);
        timerId = null;
    }
}

function startTimer() {
    if (timerId !== null || ended) return;

    timerId = setInterval(function () {
        if (ended) {
            stopTimer();
            return;
        }
        elapsed++;
        $("clock").textContent = timeText(elapsed);
    }, 1000);
}

function loadStats() {
    let data = {};
    try {
        data = JSON.parse(
            localStorage.getItem("minesweeper_stats_v2") || "{}"
        ) || {};
    } catch (e) {
        data = {};
    }

    for (const key of Object.keys(LEVELS)) {
        if (!data[key] || typeof data[key] !== "object") {
            data[key] = { wins: 0, losses: 0, best: null };
        }
    }
    return data;
}

let stats = loadStats();

function saveStats() {
    try {
        localStorage.setItem("minesweeper_stats_v2", JSON.stringify(stats));
    } catch (e) {
        // Game vẫn chạy nếu trình duyệt không cho lưu.
    }
}

function showStats() {
    const s = stats[level] || { wins: 0, losses: 0, best: null };
    $("wins").textContent = s.wins;
    $("losses").textContent = s.losses;
    $("best").textContent = s.best === null ? "—" : s.best + "s";
}

function beep(type) {
    if (!soundOn) return;

    try {
        const AudioContextClass =
            window.AudioContext || window.webkitAudioContext;
        if (!AudioContextClass) return;

        if (!audio) audio = new AudioContextClass();
        if (audio.state === "suspended") audio.resume();

        const notes = {
            open: [440],
            flag: [620],
            chord: [500, 700],
            win: [523, 659, 784],
            lose: [240, 150]
        };

        const frequencies = notes[type] || [440];

        frequencies.forEach(function (freq, index) {
            const osc = audio.createOscillator();
            const gain = audio.createGain();
            const start = audio.currentTime + index * 0.1;

            osc.frequency.value = freq;
            osc.type = type === "lose" ? "sawtooth" : "sine";

            gain.gain.setValueAtTime(0.001, start);
            gain.gain.linearRampToValueAtTime(0.06, start + 0.01);
            gain.gain.linearRampToValueAtTime(0.001, start + 0.12);

            osc.connect(gain);
            gain.connect(audio.destination);
            osc.start(start);
            osc.stop(start + 0.13);
        });
    } catch (e) {
        // Âm thanh không được phép thì bỏ qua.
    }
}

function neighbors(i) {
    const r = Math.floor(i / cols);
    const c = i % cols;
    const result = [];

    for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
            if (dr === 0 && dc === 0) continue;

            const nr = r + dr;
            const nc = c + dc;

            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                result.push(nr * cols + nc);
            }
        }
    }
    return result;
}

function placeMines(first) {
    const safe = new Set([first, ...neighbors(first)]);
    const available = [];

    for (let i = 0; i < cells.length; i++) {
        if (!safe.has(i)) available.push(i);
    }

    for (let i = available.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [available[i], available[j]] = [available[j], available[i]];
    }

    for (let i = 0; i < mineTotal; i++) {
        cells[available[i]].mine = true;
    }

    for (let i = 0; i < cells.length; i++) {
        if (!cells[i].mine) {
            cells[i].number = neighbors(i)
                .filter(n => cells[n].mine).length;
        }
    }
}

function updateCounter() {
    const n = mineTotal - flagCount;
    $("mineCounter").textContent =
        (n < 0 ? "-" : "") + String(Math.abs(n)).padStart(3, "0");
}

function render(i) {
    const cell = cells[i];
    const el = $("board").children[i];
    if (!el) return;

    el.className = "cell";
    el.textContent = "";

    if (cell.open) {
        el.classList.add("open");

        if (cell.mine) {
            el.textContent = "💣";
            el.classList.add("mine");
            if (i === exploded) el.classList.add("exploded");
        } else if (cell.number > 0) {
            el.textContent = cell.number;
            el.classList.add("n" + cell.number);
        }
    } else if (cell.flag) {
        el.textContent = "🚩";
    }

    if (ended && cell.flag && !cell.mine) {
        el.textContent = "❌";
        el.classList.add("wrong");
    }
}

function renderAll() {
    for (let i = 0; i < cells.length; i++) render(i);
}

function floodReveal(first) {
    const queue = [first];
    const visited = new Set([first]);

    while (queue.length > 0) {
        const i = queue.shift();
        const cell = cells[i];

        if (cell.open || cell.flag || cell.mine) continue;

        cell.open = true;
        openedCount++;
        render(i);

        if (cell.number === 0) {
            for (const n of neighbors(i)) {
                if (!visited.has(n) &&
                    !cells[n].open &&
                    !cells[n].flag &&
                    !cells[n].mine) {
                    visited.add(n);
                    queue.push(n);
                }
            }
        }
    }
}

function reveal(i) {
    if (ended || cells[i].open || cells[i].flag) return;

    if (!started) {
        placeMines(i);
        started = true;
        startTimer();
    }

    if (cells[i].mine) {
        exploded = i;
        cells[i].open = true;
        loseGame();
        return;
    }

    const before = openedCount;
    floodReveal(i);

    if (openedCount > before) beep("open");
    checkWin();
}

function chord(i) {
    const cell = cells[i];
    if (ended || !cell.open || cell.number === 0) return;

    const around = neighbors(i);
    const numberOfFlags = around.filter(n => cells[n].flag).length;

    if (numberOfFlags !== cell.number) {
        say("Cần cắm đúng " + cell.number + " cờ xung quanh ô số này.");
        return;
    }

    const targets = around.filter(n => !cells[n].open && !cells[n].flag);
    if (!targets.length) return;

    beep("chord");

    for (const n of targets) {
        if (cells[n].mine) {
            exploded = n;
            cells[n].open = true;
            loseGame();
            return;
        }
    }

    for (const n of targets) {
        if (!cells[n].open && !cells[n].flag) floodReveal(n);
    }

    checkWin();
}

function toggleFlag(i) {
    if (ended || cells[i].open) return;

    if (!cells[i].flag && flagCount >= mineTotal) {
        say("Đã dùng hết cờ. Gỡ một cờ trước khi cắm thêm nhé!");
        return;
    }

    cells[i].flag = !cells[i].flag;
    flagCount += cells[i].flag ? 1 : -1;

    updateCounter();
    render(i);
    beep("flag");
    say(cells[i].flag ? "Đã cắm cờ 🚩" : "Đã gỡ cờ.");
}

function loseGame() {
    if (ended) return;

    ended = true;
    stopTimer();
    $("reset").textContent = "😵";

    stats[level].losses++;
    saveStats();

    for (let i = 0; i < cells.length; i++) {
        if (cells[i].mine) cells[i].open = true;
    }

    renderAll();
    showStats();
    beep("lose");
    say("💥 Dính mìn rồi! Bấm 🙂 để chơi lại.");
}

function checkWin() {
    if (ended || openedCount !== cells.length - mineTotal) return;

    ended = true;
    stopTimer();
    $("reset").textContent = "😎";

    stats[level].wins++;
    if (stats[level].best === null || elapsed < stats[level].best) {
        stats[level].best = elapsed;
    }

    for (let i = 0; i < cells.length; i++) {
        if (cells[i].mine && !cells[i].flag) {
            cells[i].flag = true;
            flagCount++;
        }
    }

    updateCounter();
    renderAll();
    saveStats();
    showStats();
    beep("win");
    say("🎉 Thắng rồi! Thời gian: " + elapsed + " giây.");
}

function setBoardSize() {
    const frameWidth = $("boardFrame").clientWidth - 14;
    const maxCell = level === "easy" ? 40 : level === "medium" ? 32 : 26;
    const cellSize = Math.max(
        18,
        Math.min(maxCell, Math.floor(frameWidth / cols))
    );

    $("board").style.setProperty("--cell", cellSize + "px");
    $("board").style.setProperty(
        "--font-size",
        Math.max(10, Math.min(19, cellSize * 0.52)) + "px"
    );
    $("board").style.gridTemplateColumns =
        "repeat(" + cols + ", " + cellSize + "px)";
    $("board").style.gridTemplateRows =
        "repeat(" + rows + ", " + cellSize + "px)";
    $("board").style.width = (cols * cellSize) + "px";
    $("board").style.height = (rows * cellSize) + "px";
}

function newGame() {
    stopTimer();

    const config = LEVELS[level];
    rows = config.rows;
    cols = config.cols;
    mineTotal = config.mines;

    cells = Array.from({ length: rows * cols }, () => ({
        mine: false,
        number: 0,
        open: false,
        flag: false
    }));

    flagCount = 0;
    openedCount = 0;
    started = false;
    ended = false;
    flagMode = false;
    elapsed = 0;
    exploded = -1;

    $("clock").textContent = "000";
    $("reset").textContent = "🙂";
    $("flagMode").textContent = "🚩 Cắm cờ: TẮT";
    $("flagMode").classList.remove("active");

    $("board").innerHTML = "";

    for (let i = 0; i < cells.length; i++) {
        const el = document.createElement("button");
        el.type = "button";
        el.className = "cell";
        el.setAttribute("aria-label", "Ô chưa mở");

        el.addEventListener("click", function () {
            if (Date.now() < suppressClickUntil || ended) return;

            if (flagMode) {
                toggleFlag(i);
            } else if (cells[i].open) {
                chord(i);
            } else {
                reveal(i);
            }
        });

        el.addEventListener("contextmenu", function (e) {
            e.preventDefault();
            suppressClickUntil = Date.now() + 500;
            toggleFlag(i);
        });

        let holdTriggered = false;

        el.addEventListener("pointerdown", function (e) {
            if (e.pointerType === "mouse" || ended) return;

            holdTriggered = false;
            clearTimeout(holdTimer);

            holdTimer = setTimeout(function () {
                holdTriggered = true;
                suppressClickUntil = Date.now() + 600;
                toggleFlag(i);
            }, 450);
        });

        function cancelHold() {
            clearTimeout(holdTimer);
        }

        el.addEventListener("pointerup", cancelHold);
        el.addEventListener("pointercancel", cancelHold);
        el.addEventListener("pointerleave", cancelHold);
        el.addEventListener("dragstart", e => e.preventDefault());

        $("board").appendChild(el);
    }

    setBoardSize();
    updateCounter();
    showStats();

    say("Chọn một ô để bắt đầu! Lượt đầu và vùng xung quanh luôn an toàn.");
}

$("difficulty").addEventListener("change", function () {
    level = this.value;
    newGame();
});

$("reset").addEventListener("click", newGame);
$("newGame").addEventListener("click", newGame);

$("flagMode").addEventListener("click", function () {
    if (ended) return;

    flagMode = !flagMode;
    this.classList.toggle("active", flagMode);
    this.textContent = flagMode ? "🚩 Cắm cờ: BẬT" : "🚩 Cắm cờ: TẮT";

    say(flagMode
        ? "Chạm ô để cắm hoặc gỡ cờ."
        : "Chạm ô để dò mìn.");
});

$("soundBtn").addEventListener("click", function () {
    soundOn = !soundOn;
    this.textContent = soundOn ? "🔊 Âm thanh" : "🔇 Âm thanh tắt";
    if (soundOn) beep("open");
});

window.addEventListener("resize", setBoardSize);

newGame();
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=1000, scrolling=True)
