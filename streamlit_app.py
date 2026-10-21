
import random
import time
import streamlit as st

# =========================
# CAU HINH GAME
# =========================
st.set_page_config(
    page_title="Minesweeper",
    page_icon="💣",
    layout="centered"
)

ROWS = 9
COLS = 9
MINE_COUNT = 10

# =========================
# GIAO DIEN MINESWEEPER
# =========================
st.markdown("""
<style>
.stApp {
    background: #e9edf2;
}
.block-container {
    max-width: 500px;
    padding: 1rem 0.35rem 2rem;
}
h1 {
    text-align: center;
    color: #26364b;
    font-size: 28px !important;
}
[data-testid="stHorizontalBlock"] {
    gap: 2px !important;
}
[data-testid="stColumn"] {
    min-width: 0 !important;
    padding: 0 !important;
}
[data-testid="stButton"] {
    width: 100%;
}
[data-testid="stButton"] button {
    width: 100%;
    aspect-ratio: 1 / 1;
    min-height: 0;
    height: auto;
    padding: 0;
    border-radius: 0;
    border: 2px outset #ffffff;
    background: #b9c5d3;
    color: #26364b;
    font-size: clamp(12px, 4vw, 22px);
    font-weight: 900;
    line-height: 1;
}
[data-testid="stButton"] button:disabled {
    opacity: 1;
    border: 1px solid #c4cbd3;
    background: #d9dee5;
    color: #26364b;
}
[data-testid="stButton"] button:hover:not(:disabled) {
    background: #d0dbea;
    color: #172b48;
}
div[data-testid="stCheckbox"] {
    background: #ffffff;
    padding: 8px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TAO BAN CO
# =========================
def create_board(safe_cell=None):
    all_cells = list(range(ROWS * COLS))

    if safe_cell is not None:
        all_cells.remove(safe_cell)

    mines = set(random.sample(all_cells, MINE_COUNT))
    numbers = {}

    for cell in range(ROWS * COLS):
        if cell in mines:
            continue

        r, c = divmod(cell, COLS)
        count = 0

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc

                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if nr * COLS + nc in mines:
                        count += 1

        numbers[cell] = count

    return mines, numbers


def reset_game():
    st.session_state.mines, st.session_state.numbers = (
        create_board()
    )
    st.session_state.opened = set()
    st.session_state.flags = set()
    st.session_state.started = False
    st.session_state.over = False
    st.session_state.won = False
    st.session_state.flag_mode = False
    st.session_state.start_time = None
    st.session_state.end_time = None


def open_cell(cell):
    if st.session_state.over:
        return

    if cell in st.session_state.flags:
        return

    if cell in st.session_state.opened:
        return

    # Dam bao lan mo dau tien khong trung min
    if not st.session_state.started:
        st.session_state.mines, st.session_state.numbers = (
            create_board(safe_cell=cell)
        )
        st.session_state.started = True
        st.session_state.start_time = time.time()

    if cell in st.session_state.mines:
        st.session_state.opened.add(cell)
        st.session_state.over = True
        st.session_state.won = False
        st.session_state.end_time = time.time()
        return

    # Mo o va mo rong vung so 0
    stack = [cell]

    while stack:
        current = stack.pop()

        if current in st.session_state.opened:
            continue

        if current in st.session_state.flags:
            continue

        if current in st.session_state.mines:
            continue

        st.session_state.opened.add(current)

        if st.session_state.numbers[current] == 0:
            r, c = divmod(current, COLS)

            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc

                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        neighbor = nr * COLS + nc

                        if neighbor not in st.session_state.opened:
                            stack.append(neighbor)

    if len(st.session_state.opened) == ROWS * COLS - MINE_COUNT:
        st.session_state.over = True
        st.session_state.won = True
        st.session_state.end_time = time.time()


def toggle_flag(cell):
    if st.session_state.over:
        return

    if cell in st.session_state.opened:
        return

    if cell in st.session_state.flags:
        st.session_state.flags.remove(cell)
    elif len(st.session_state.flags) < MINE_COUNT:
        st.session_state.flags.add(cell)


# =========================
# KHOI TAO
# =========================
if "mines" not in st.session_state:
    reset_game()

# =========================
# DAU GAME
# =========================
st.title("💣 MINESWEEPER")
st.caption("Tim o an toan. Tranh xa cac qua min!")

remaining = MINE_COUNT - len(st.session_state.flags)

a, b = st.columns(2)
a.metric("💣 Số mìn", remaining)
b.metric("🟩 Ô an toàn", len(st.session_state.opened))

if st.session_state.started:
    end = st.session_state.end_time or time.time()
    elapsed = int(end - st.session_state.start_time)
else:
    elapsed = 0

st.metric("⏱️ Thời gian", f"{elapsed} giây")

st.checkbox(
    "🚩 Chế độ cắm cờ",
    key="flag_mode",
    disabled=st.session_state.over
)

if st.session_state.flag_mode:
    st.info("Chạm ô để cắm hoặc gỡ cờ.")
else:
    st.info("Chạm ô để mở. Lần mở đầu tiên luôn an toàn.")

# =========================
# BAN CO VUONG
# =========================
number_colors = {
    1: "#1769d2",
    2: "#168044",
    3: "#df3030",
    4: "#5833a6",
    5: "#9c2929",
    6: "#168c91",
    7: "#222222",
    8: "#777777",
}

for r in range(ROWS):
    cols = st.columns(COLS, gap=None)

    for c in range(COLS):
        cell = r * COLS + c

        is_open = cell in st.session_state.opened
        is_flag = cell in st.session_state.flags
        is_mine = cell in st.session_state.mines

        if is_open and is_mine:
            label = "💥"
        elif is_open:
            number = st.session_state.numbers[cell]
            label = str(number) if number else " "
        elif is_flag:
            label = "🚩"
        elif st.session_state.over and is_mine:
            label = "💣"
        else:
            label = " "

        with cols[c]:
            if st.button(
                label,
                key=f"cell_{cell}",
                disabled=is_open or st.session_state.over,
                use_container_width=True
            ):
                if st.session_state.flag_mode:
                    toggle_flag(cell)
                else:
                    open_cell(cell)
                st.rerun()

# =========================
# KET QUA
# =========================
if st.session_state.over:
    st.divider()

    if st.session_state.won:
        st.balloons()
        st.success("🏆 CHIẾN THẮNG! M đã dò hết ô an toàn!")
    else:
        st.error("💥 BOOM! M đã chạm phải mìn!")

    st.write(f"Thời gian hoàn thành: {elapsed} giây")

    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset_game()
        st.rerun()
else:
    if st.button("🔄 Tạo bàn cờ mới", use_container_width=True):
        reset_game()
        st.rerun()
