
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Minesweeper",
    page_icon="💣",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        max-width: 1000px;
        padding: 0.5rem 0.4rem 1rem;
    }

    iframe {
        display: block;
        width: 100%;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    background: #c0c0c0;
    color: #111;
    font-family: Tahoma, Arial, sans-serif;
    font-size: 13px;
}

button, select {
    font: inherit;
}

button {
    cursor: pointer;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
}

.app {
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
    padding: 5px;
    background: #c0c0c0;
}

.window {
    border: 2px solid;
    border-color: #fff #555 #555 #fff;
    padding: 7px;
    background: #c0c0c0;
    box-shadow: 1px 1px 0 #808080;
}

.titlebar {
    background: #000080;
    color: white;
    padding: 8px 9px;
    font-weight: bold;
    font-size: 16px;
    letter-spacing: .2px;
    margin-bottom: 8px;
}

.toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 7px;
    margin-bottom: 8px;
}

select, .classic-btn {
    min-height: 32px;
    padding: 5px 8px;
    color: #111;
    background: #c0c0c0;
    border: 2px solid;
    border-color: #fff #555 #555 #fff;
    border-radius: 0;
}

select {
    flex: 1;
    min-width: 145px;
    max-width: 240px;
}

.classic-btn:active, .classic-btn.active {
    border-color: #555 #fff #fff #555;
}

.classic-btn:disabled {
    opacity: .55;
    cursor: default;
}

.top-panel {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 7px;
    margin-bottom: 8px;
}

.counter {
    background: #111;
    color: #ff2929;
    border: 2px solid;
    border-color: #555 #fff #fff #555;
    padding: 4px 5px;
    min-width: 57px;
    text-align: center;
    font-family: "Courier New", monospace;
    font-size: 25px;
    line-height: 1.15;
    font-weight: bold;
    font-variant-numeric: tabular-nums;
}

.face {
    min-width: 43px;
    min-height: 39px;
    font-size: 23px;
    padding: 1px 5px;
}

.status {
    margin: 0 0 8px;
    padding: 7px 8px;
    background: #d4d0c8;
    border: 1px solid #858585;
    line-height: 1.5;
    overflow-wrap: anywhere;
}

.status strong {
    color: #000080;
}

.board-frame {
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 3px;
    background: #808080;
    border: 3px solid;
    border-color: #555 #fff #fff #555;
    overscroll-behavior-x: contain;
}

#board {
    display: grid;
    gap: 0;
    margin: 0 auto;
    padding: 0;
    background: #808080;
    touch-action: pan-x pan-y;
    user-select: none;
    -webkit-user-select: none;
}

.cell {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-width: 0;
    min-height: 0;
    aspect-ratio: 1 / 1;
    margin: 0;
    padding: 0;
    overflow: hidden;
    border-radius: 0;
    border: 2px solid;
    border-color: #fff #777 #777 #fff;
    background: #c0c0c0;
    color: #000;
    font-family: Arial, sans-serif;
    font-size: clamp(9px, 2.7vw, 19px);
    font-weight: bold;
    line-height: 1;
    text-align: center;
    box-shadow: none;
}

.cell.open {
    border: 1px solid #999;
    background: #c0c0c0;
    cursor: default;
}

.cell.flagged {
    color: #e00000;
}

.cell.mine {
    background: #ff4242;
}

.cell.exploded {
    background: #ff0000;
}

.cell.wrong {
    background: #ffb0b0;
}

.cell.n1 { color: #0000ff; }
.cell.n2 { color: #008000; }
.cell.n3 { color: #ff0000; }
.cell.n4 { color: #000080; }
.cell.n5 { color: #800000; }
.cell.n6 { color: #008080; }
.cell.n7 { color: #111; }
.cell.n8 { color: #666; }

.stats {
    margin-top: 9px;
    padding: 8px;
    border: 1px solid #858585;
    background: #d4d0c8;
}

.stats-title {
    font-weight: bold;
    margin-bottom: 6px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 5px;
}

.stat {
    background: #c0c0c0;
    border: 1px solid #999;
    padding: 7px 3px;
    text-align: center;
    min-width: 0;
}

.stat-label {
    font-size: 11px;
    color: #444;
    margin-bottom: 4px;
}

.stat-value {
    font-size: 16px;
    font-weight: bold;
    overflow-wrap: anywhere;
}

.bottom {
    margin-top: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.bottom button {
    flex: 1;
}

.hint {
    font-size: 11px;
    color: #444;
    line-height: 1.5;
    margin-top: 8px;
}

@media (min-width: 600px) {
    .app {
        padding: 8px;
    }

    .window {
        padding: 10px;
    }

    .cell {
        font-size: clamp(10px, 1.5vw, 19px);
    }
}

@media (max-width: 360px) {
    .counter {
        min-width: 49px;
        font-size: 21px;
    }

    .face {
        min-width: 37px;
        font-size: 21px;
    }

    .toolbar {
        gap: 5px;
    }

    select {
        min-width: 125px;
    }
}
</style>
</head>

<body>
<div class="app">
<div class="window">

    <div class="titlebar">💣 MINESWEEPER</div>

    <div class="toolbar">
        <select id="difficulty" aria-label="Chọn độ khó">
            <option value="easy">Dễ — 9 × 9 · 10 mìn</option>
            <option value="medium">Trung bình — 16 × 16 · 40 mìn</option>
            <option value="hard">Khó — 30 × 16 · 99 mìn</option>
        </select>
        <button class="classic-btn" id="soundBtn">🔊 Âm thanh</button>
    </div>

    <div class="top-panel">
        <div class="counter" id="mineCounter">010</div>
        <button class="classic-btn face" id="reset" aria-label="Chơi lại">🙂</button>
        <div class="counter" id="timeCounter">000</div>
    </div>

    <div class="status" id="message" aria-live="polite">
        Chọn một ô để bắt đầu!
    </div>

    <div class="board-frame" id="boardFrame">
        <div id="board" aria-label="Bàn dò mìn"></div>
    </div>

    <div class="bottom">
        <button class="classic-btn" id="flagMode">🚩 Cắm cờ: TẮT</button>
        <button class="classic-btn" id="freeMode">♾️ Chơi tự do</button>
    </div>

    <div class="stats">
        <div class="stats-title">📊 Thống kê độ khó hiện tại</div>
        <div class="stats-grid">
            <div class="stat">
                <div class="stat-label">Số ván thắng</div>
                <div class="stat-value" id="wins">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">Số ván thua</div>
                <div class="stat-value" id="losses">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">Kỷ lục</div>
                <div class="stat-value" id="best">—</div>
            </div>
        </div>
    </div>

    <div class="hint">
        🖱️ Máy tính: nhấn trái để mở, nhấn phải để cắm cờ.
        <br>
        📱 Điện thoại: chạm để mở, nhấn giữ để cắm cờ.
        <br>
        🔢 Bấm ô số đã mở để mở nhanh các ô xung quanh khi cắm đủ cờ.
        <br>
        🛡️ Lượt đầu luôn an toàn, kể cả 8 ô xung quanh.
        <br>
        ♾️ Chế độ tự do không giới hạn số ván chơi.
    </div>

</div>
</div>

<script>
"use strict";

const DIFFICULTIES = {
    easy:   { rows: 9,  cols: 9,  mines: 10 },
    medium: { rows: 16, cols: 16, mines: 40 },
    hard:   { rows: 16, cols: 30, mines: 99 }
};

const $ = id => document.getElementById(id);

const board = $("board");
const boardFrame = $("boardFrame");
const message = $("message");
const difficultySelect = $("difficulty");

let difficulty = "easy";
let ROWS = 9;
let COLS = 9;
let TOTAL_MINES = 10;

let cells = [];
let flags = 0;
let opened = 0;
let started = false;
let ended = false;
let flagMode = false;
let freeMode = true;
let seconds = 0;
let timer = null;
let soundOn = true;
let explodedIndex = -1;
let suppressClickUntil = 0;
let audioContext = null;

const emptyStats = () => ({
    wins: 0,
    losses: 0,
    best: null
});

let stats = loadStats();

function loadStats() {
    try {
        const saved = JSON.parse(
            localStorage.getItem("minesweeper_classic_stats_v1") || "{}"
        );

        for (const key of Object.keys(DIFFICULTIES)) {
            if (!saved[key]) saved[key] = emptyStats();
        }
        return saved;
    } catch (e) {
        return {
            easy: emptyStats(),
            medium: emptyStats(),
            hard: emptyStats()
        };
    }
}

function saveStats() {
    try {
        localStorage.setItem(
            "minesweeper_classic_stats_v1",
            JSON.stringify(stats)
        );
    } catch (e) {
        // Game vẫn chơi được nếu trình duyệt không cho lưu dữ liệu.
    }
}

function showMessage(text) {
    message.textContent = text;
}

function formatTime(value) {
    return String(Math.min(value, 999)).padStart(3, "0");
}

function setTimerDisplay() {
    $("timeCounter").textContent = formatTime(seconds);
}

function renderStats() {
    const s = stats[difficulty] || emptyStats();

    $("wins").textContent = s.wins;
    $("losses").textContent = s.losses;
    $("best").textContent =
        s.best === null ? "—" : s.best + "s";
}

function playSound(type) {
    if (!soundOn) return;

    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;

        if (!audioContext) audioContext = new AudioCtx();

        if (audioContext.state === "suspended") {
            audioContext.resume();
        }

        const patterns = {
            open: [[440, 0.045, "sine"]],
            flag: [[660, 0.055, "square"]],
            chord: [[520, 0.045, "sine"], [720, 0.055, "sine"]],
            win: [[523, 0.12, "sine"], [659, 0.12, "sine"],
                  [784, 0.18, "sine"]],
            lose: [[260, 0.17, "sawtooth"], [150, 0.22, "sawtooth"]]
        };

        let offset = 0;

        for (const [frequency, duration, wave] of (patterns[type] || [])) {
            const osc = audioContext.createOscillator();
            const gain = audioContext.createGain();

            osc.type = wave;
            osc.frequency.value = frequency;

            gain.gain.setValueAtTime(0.0001, audioContext.currentTime + offset);
            gain.gain.exponentialRampToValueAtTime(
                0.07, audioContext.currentTime + offset + 0.01
            );
            gain.gain.exponentialRampToValueAtTime(
                0.0001,
                audioContext.currentTime + offset + duration
            );

            osc.connect(gain);
            gain.connect(audioContext.destination);

            osc.start(audioContext.currentTime + offset);
            osc.stop(audioContext.currentTime + offset + duration);

            offset += duration * 0.85;
        }
    } catch (e) {
        // Không để lỗi âm thanh làm hỏng trò chơi.
    }
}

function stopTimer() {
    if (timer !== null) {
        clearInterval(timer);
        timer = null;
    }
}

function startTimer() {
    if (timer !== null || ended) return;

    timer = setInterval(() => {
        if (ended) {
            stopTimer();
            return;
        }

        seconds++;
        setTimerDisplay();
    }, 1000);
}

function updateMineCounter() {
    const remaining = TOTAL_MINES - flags;
    $("mineCounter").textContent =
        (remaining < 0 ? "-" : "") +
        String(Math.abs(remaining)).padStart(3, "0");
}

function getNeighbors(index) {
    const r = Math.floor(index / COLS);
    const c = index % COLS;
    const result = [];

    for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
            if (dr === 0 && dc === 0) continue;

            const nr = r + dr;
            const nc = c + dc;

            if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) {
                result.push(nr * COLS + nc);
            }
        }
    }

    return result;
}

function placeMines(safeIndex) {
    // Vùng 3 x 3 quanh lượt mở đầu tiên không có mìn.
    const safe = new Set([safeIndex, ...getNeighbors(safeIndex)]);
    const available = [];

    for (let i = 0; i < cells.length; i++) {
        if (!safe.has(i)) available.push(i);
    }

    // Fisher-Yates shuffle.
    for (let i = available.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [available[i], available[j]] = [available[j], available[i]];
    }

    for (let i = 0; i < TOTAL_MINES; i++) {
        cells[available[i]].mine = true;
    }

    for (let i = 0; i < cells.length; i++) {
        if (!cells[i].mine) {
            cells[i].number = getNeighbors(i)
                .filter(n => cells[n].mine).length;
        }
    }
}

function renderCell(index) {
    const cell = cells[index];
    const el = board.children[index];

    if (!el) return;

    el.className = "cell";
    el.textContent = "";
    el.removeAttribute("title");

    if (cell.open) {
        el.classList.add("open");

        if (cell.mine) {
            el.textContent = "💣";
            el.classList.add("mine");
            if (index === explodedIndex) el.classList.add("exploded");
            el.setAttribute("aria-label", "Mìn");
        } else if (cell.number > 0) {
            el.textContent = cell.number;
            el.classList.add("n" + cell.number);
            el.setAttribute(
                "aria-label",
                cell.number + " mìn xung quanh"
            );
        } else {
            el.setAttribute("aria-label", "Ô trống");
        }
    } else if (cell.flag) {
        el.textContent = "🚩";
        el.classList.add("flagged");
        el.setAttribute("aria-label", "Ô có cờ");
    } else {
        el.setAttribute("aria-label", "Ô chưa mở");
    }

    if (ended && cell.flag && !cell.mine) {
        el.classList.add("wrong");
        el.textContent = "❌";
        el.setAttribute("title", "Cắm cờ sai");
    }
}

function renderAll() {
    for (let i = 0; i < cells.length; i++) renderCell(i);
}

function floodReveal(startIndex) {
    const queue = [startIndex];
    const queued = new Set(queue);

    while (queue.length) {
        const index = queue.shift();
        const cell = cells[index];

        if (cell.open || cell.flag || cell.mine) continue;

        cell.open = true;
        opened++;
        renderCell(index);

        if (cell.number === 0) {
            for (const n of getNeighbors(index)) {
                if (
                    !queued.has(n) &&
                    !cells[n].open &&
                    !cells[n].flag &&
                    !cells[n].mine
                ) {
                    queued.add(n);
                    queue.push(n);
                }
            }
        }
    }
}

function reveal(index) {
    if (ended || cells[index].open || cells[index].flag) return;

    if (!started) {
        placeMines(index);
        started = true;
        startTimer();
    }

    if (cells[index].mine) {
        explodedIndex = index;
        cells[index].open = true;
        renderCell(index);
        loseGame();
        return;
    }

    const oldOpened = opened;
    floodReveal(index);

    if (opened > oldOpened) playSound("open");

    checkWin();
}

function chord(index) {
    if (ended || !cells[index].open || cells[index].number === 0) return;

    const neighbors = getNeighbors(index);
    const adjacentFlags = neighbors.filter(n => cells[n].flag).length;

    if (adjacentFlags !== cells[index].number) {
        showMessage(
            "Ô này có " + cells[index].number +
            " mìn xung quanh. Cắm đúng số cờ để mở nhanh."
        );
        return;
    }

    const targets = neighbors.filter(
        n => !cells[n].open && !cells[n].flag
    );

    if (!targets.length) return;

    playSound("chord");

    for (const n of targets) {
        if (cells[n].mine) {
            explodedIndex = n;
            cells[n].open = true;
            renderCell(n);
            loseGame();
            return;
        }
    }

    for (const n of targets) {
        if (!cells[n].open && !cells[n].flag) floodReveal(n);
    }

    checkWin();
}

function toggleCellFlag(index) {
    if (ended || cells[index].open) return;

    if (!cells[index].flag && flags >= TOTAL_MINES) {
        showMessage(
            "Đã cắm đủ " + TOTAL_MINES +
            " cờ. Hãy gỡ một cờ trước khi cắm thêm!"
        );
        return;
    }

    cells[index].flag = !cells[index].flag;
    flags += cells[index].flag ? 1 : -1;

    updateMineCounter();
    renderCell(index);
    playSound("flag");

    showMessage(
        cells[index].flag
            ? "Đã cắm cờ 🚩"
            : "Đã gỡ cờ."
    );
}

function loseGame() {
    if (ended) return;

    ended = true;
    stopTimer();

    $("reset").textContent = "😵";
    stats[difficulty].losses++;
    saveStats();

    // Hiện toàn bộ mìn sau khi thua.
    for (let i = 0; i < cells.length; i++) {
        if (cells[i].mine) cells[i].open = true;
        renderCell(i);
    }

    renderStats();
    playSound("lose");
    showMessage("💥 Dính mìn rồi! Bấm 😵 để chơi lại.");
}

function checkWin() {
    if (ended || opened !== cells.length - TOTAL_MINES) return;

    ended = true;
    stopTimer();

    $("reset").textContent = "😎";

    const s = stats[difficulty];
    s.wins++;

    if (s.best === null || seconds < s.best) {
        s.best = seconds;
    }

    // Tự cắm cờ vào các quả mìn còn lại.
    for (let i = 0; i < cells.length; i++) {
        if (cells[i].mine && !cells[i].flag) {
            cells[i].flag = true;
            flags++;
        }
    }

    updateMineCounter();
    renderAll();
    saveStats();
    renderStats();

    playSound("win");
    showMessage("🎉 Chiến thắng! Thời gian: " + seconds + " giây.");
}

function toggleFlagMode() {
    if (ended) return;

    flagMode = !flagMode;
    $("flagMode").classList.toggle("active", flagMode);
    $("flagMode").textContent =
        flagMode ? "🚩 Cắm cờ: BẬT" : "🚩 Cắm cờ: TẮT";

    showMessage(
        flagMode
            ? "Chế độ cắm cờ đang bật. Chạm ô để đặt hoặc gỡ cờ."
            : "Chế độ dò mìn. Chạm ô để mở."
    );
}

function newGame() {
    stopTimer();

    const config = DIFFICULTIES[difficulty];
    ROWS = config.rows;
    COLS = config.cols;
    TOTAL_MINES = config.mines;

    cells = Array.from(
        { length: ROWS * COLS },
        () => ({
            mine: false,
            number: 0,
            open: false,
            flag: false
        })
    );

    flags = 0;
    opened = 0;
    started = false;
    ended = false;
    flagMode = false;
    seconds = 0;
    explodedIndex = -1;
    suppressClickUntil = 0;

    $("timeCounter").textContent = "000";
    $("reset").textContent = "🙂";
    $("flagMode").classList.remove("active");
    $("flagMode").textContent = "🚩 Cắm cờ: TẮT";

    updateMineCounter();

    board.style.gridTemplateColumns =
        "repeat(" + COLS + ", minmax(0, 1fr))";
    board.style.gridTemplateRows =
        "repeat(" + ROWS + ", minmax(0, 1fr))";
    board.style.aspectRatio = COLS + " / " + ROWS;

    // Bàn 9 hoặc 16 cột co theo màn hình.
    // Bàn 30 cột có chiều rộng tối thiểu để ô vẫn vuông,
    // dễ nhìn và có thể cuộn ngang trên điện thoại.
    const isHard = difficulty === "hard";
    const minBoardWidth = isHard ? 540 : 0;

    board.style.width = isHard
        ? "max(100%, " + minBoardWidth + "px)"
        : "100%";

    board.style.maxWidth = "100%";
    boardFrame.style.overflowX = isHard ? "auto" : "hidden";

    board.innerHTML = "";

    for (let i = 0; i < cells.length; i++) {
      