
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dò mìn",
    page_icon="💣",
    layout="centered"
)

st.markdown("""
<style>
    .block-container {
        max-width: 430px !important;
        padding: 1rem 0.5rem !important;
    }
    header, footer, #MainMenu {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 8px 0;
    background: #171a20;
    color: #e5e7eb;
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
}

.game {
    width: 100%;
    max-width: 360px;
    padding: 12px;
    background: #252a32;
    border: 1px solid #414854;
    border-radius: 10px;
}

h2 {
    text-align: center;
    margin: 0 0 12px;
    font-size: 22px;
}

.info {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    margin-bottom: 10px;
}

.counter {
    background: #101318;
    color: #ff6666;
    font-family: monospace;
    font-size: 20px;
    padding: 6px 8px;
    border-radius: 4px;
    min-width: 65px;
    text-align: center;
}

#reset, #flagMode {
    border: 1px solid #626b79;
    background: #373e49;
    color: white;
    border-radius: 5px;
    padding: 8px;
    font-size: 14px;
    cursor: pointer;
}

#flagMode.active {
    background: #806326;
    border-color: #e8b94e;
}

#board {
    display: grid;
    grid-template-columns: repeat(9, minmax(0, 1fr));
    gap: 2px;
    width: 100%;
    aspect-ratio: 1 / 1;
    padding: 4px;
    background: #11151a;
    border: 1px solid #454d58;
    touch-action: manipulation;
}

.cell {
    min-width: 0;
    min-height: 0;
    padding: 0;
    margin: 0;
    border-radius: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: clamp(12px, 4vw, 19px);
    font-weight: bold;
    line-height: 1;
    overflow: hidden;
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    border: 2px outset #9299a3;
    background: #69727e;
    color: #111;
}

.cell.open {
    border: 1px solid #343a43;
    background: #c2c7ce;
    cursor: default;
}

.cell.flagged { color: #e53935; }
.cell.mine { background: #ed6262; }

.n1 { color: #155bd5; }
.n2 { color: #16813c; }
.n3 { color: #d32f2f; }
.n4 { color: #5929a3; }
.n5 { color: #8c2424; }
.n6 { color: #008b99; }
.n7 { color: #242424; }
.n8 { color: #666666; }

#message {
    min-height: 24px;
    text-align: center;
    margin-top: 10px;
    font-size: 14px;
    color: #d6dbe3;
}

.hint {
    text-align: center;
    font-size: 12px;
    color: #aab2bf;
    margin-top: 5px;
}
</style>
</head>
<body>
<div class="game">
    <h2>💣 DÒ MÌN</h2>

    <div class="info">
        <div class="counter" id="mines">010</div>
        <button id="reset" onclick="newGame()">🙂</button>
        <button id="flagMode" onclick="toggleFlag()">🚩 Cắm cờ</button>
        <div class="counter" id="time">000</div>
    </div>

    <div id="board"></div>
    <div id="message">Chọn một ô để bắt đầu!</div>
    <div class="hint">9 × 9 ô · 10 quả mìn</div>
</div>

<script>
const SIZE = 9;
const TOTAL_MINES = 10;

let cells = [];
let flags = 0;
let opened = 0;
let started = false;
let ended = false;
let flagMode = false;
let seconds = 0;
let timer = null;

const board = document.getElementById("board");
const message = document.getElementById("message");

function newGame() {
    clearInterval(timer);
    cells = [];
    flags = 0;
    opened = 0;
    started = false;
    ended = false;
    flagMode = false;
    seconds = 0;

    document.getElementById("time").textContent = "000";
    document.getElementById("reset").textContent = "🙂";
    document.getElementById("flagMode").classList.remove("active");
    document.getElementById("mines").textContent = "010";
    message.textContent = "Chọn một ô để bắt đầu!";

    board.innerHTML = "";

    for (let i = 0; i < SIZE * SIZE; i++) {
        cells.push({
            mine: false,
            number: 0,
            open: false,
            flag: false
        });

        const el = document.createElement("button");
        el.className = "cell";
        el.type = "button";
        el.setAttribute("aria-label", "Ô chưa mở");

        el.addEventListener("click", () => {
            if (flagMode) toggleCellFlag(i);
            else reveal(i);
        });

        el.addEventListener("contextmenu", e => {
            e.preventDefault();
            toggleCellFlag(i);
        });

        board.appendChild(el);
    }
}

function neighbors(i) {
    const r = Math.floor(i / SIZE);
    const c = i % SIZE;
    const result = [];

    for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
            if (dr === 0 && dc === 0) continue;

            const nr = r + dr;
            const nc = c + dc;

            if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE) {
                result.push(nr * SIZE + nc);
            }
        }
    }
    return result;
}

function placeMines(safeIndex) {
    let available = [];

    for (let i = 0; i < cells.length; i++) {
        if (i !== safeIndex) available.push(i);
    }

    for (let i = available.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [available[i], available[j]] = [available[j], available[i]];
    }

    available.slice(0, TOTAL_MINES).forEach(i => {
        cells[i].mine = true;
    });

    cells.forEach((cell, i) => {
        if (!cell.mine) {
            cell.number = neighbors(i).filter(n => cells[n].mine).length;
        }
    });
}

function startTimer() {
    if (started) return;
    started = true;

    timer = setInterval(() => {
        if (ended) return;
        seconds++;
        document.getElementById("time").textContent =
            String(Math.min(seconds, 999)).padStart(3, "0");
    }, 1000);
}

function reveal(i) {
    if (ended || cells[i].open || cells[i].flag) return;

    if (!started) {
        placeMines(i);
        startTimer();
    }

    if (cells[i].mine) {
        cells[i].open = true;
        renderCell(i);
        loseGame();
        return;
    }

    floodReveal(i);
    checkWin();
}

function floodReveal(startIndex) {
    const queue = [startIndex];

    while (queue.length) {
        const i = queue.shift();
        const cell = cells[i];

        if (cell.open || cell.flag || cell.mine) continue;

        cell.open = true;
        opened++;
        renderCell(i);

        if (cell.number === 0) {
            neighbors(i).forEach(n => {
                if (!cells[n].open && !cells[n].flag && !cells[n].mine) {
                    queue.push(n);
                }
            });
        }
    }
}

function toggleFlag() {
    if (ended) return;
    flagMode = !flagMode;
    document.getElementById("flagMode").classList.toggle("active", flagMode);
    message.textContent = flagMode
        ? "Chạm ô để cắm hoặc gỡ cờ 🚩"
        : "Chọn ô để dò mìn!";
}

function toggleCellFlag(i) {
    if (ended || cells[i].open) return;

    cells[i].flag = !cells[i].flag;
    flags += cells[i].flag ? 1 : -1;

    document.getElementById("mines").textContent =
        String(Math.max(-99, TOTAL_MINES - flags)).padStart(3, "0");

    renderCell(i);
}

function renderCell(i) {
    const cell = cells[i];
    const el = board.children[i];

    el.className = "cell";
    el.textContent = "";
    el.setAttribute("aria-label", "Ô chưa mở");

    if (cell.flag && !cell.open) {
        el.textContent = "🚩";
        el.classList.add("flagged");
        el.setAttribute("aria-label", "Ô có cờ");
    } else if (cell.open) {
        el.classList.add("open");

        if (cell.mine) {
            el.textContent = "💣";
            el.classList.add("mine");
            el.setAttribute("aria-label", "Mìn");
        } else if (cell.number > 0) {
            el.textContent = cell.number;
            el.classList.add("n" + cell.number);
            el.setAttribute("aria-label", "Có " + cell.number + " mìn xung quanh");
        } else {
            el.setAttribute("aria-label", "Ô trống an toàn");
        }
    }
}

function loseGame() {
    ended = true;
    clearInterval(timer);
    document.getElementById("reset").textContent = "😵";

    cells.forEach((cell, i) => {
        if (cell.mine) {
            cell.open = true;
            renderCell(i);
        }
    });

    message.textContent = "💥 Dính mìn rồi! Bấm 🙂 để chơi lại.";
}

function checkWin() {
    if (opened === SIZE * SIZE - TOTAL_MINES) {
        ended = true;
        clearInterval(timer);
        document.getElementById("reset").textContent = "😎";
        message.textContent = "🎉 Thắng rồi! Bạn dò sạch mìn!";
    }
}

newGame();
</script>
</body>
</html>
""", height=490, scrolling=False)
