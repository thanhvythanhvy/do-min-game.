
import random
import streamlit as st

st.set_page_config(
    page_title="Dò Mìn",
    page_icon="💣",
    layout="centered"
)

ROWS = 8
COLS = 8
MINE_COUNT = 10


def new_game():
    mines = set(
        random.sample(
            range(ROWS * COLS),
            MINE_COUNT
        )
    )

    numbers = {}

    for r in range(ROWS):
        for c in range(COLS):
            cell = r * COLS + c

            if cell in mines:
                continue

            count = 0

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if nr * COLS + nc in mines:
                            count += 1

            numbers[cell] = count

    st.session_state.mines = mines
    st.session_state.numbers = numbers
    st.session_state.revealed = set()
    st.session_state.flags = set()
    st.session_state.game_over = False
    st.session_state.won = False


# Khoi tao game
if "mines" not in st.session_state:
    new_game()


def reveal_cell(cell):
    if cell in st.session_state.flags:
        return

    if cell in st.session_state.revealed:
        return

    st.session_state.revealed.add(cell)

    # Trung min
    if cell in st.session_state.mines:
        st.session_state.game_over = True
        st.session_state.won = False
        return

    # Mo rong cac o so 0
    if st.session_state.numbers[cell] == 0:
        stack = [cell]

        while stack:
            current = stack.pop()
            r = current // COLS
            c = current % COLS

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        neighbor = nr * COLS + nc

                        if neighbor in st.session_state.revealed:
                            continue

                        if neighbor in st.session_state.mines:
                            continue

                        if neighbor in st.session_state.flags:
                            continue

                        st.session_state.revealed.add(neighbor)

                        if st.session_state.numbers[neighbor] == 0:
                            stack.append(neighbor)

    safe_cells = ROWS * COLS - MINE_COUNT

    if len(st.session_state.revealed) >= safe_cells:
        st.session_state.game_over = True
        st.session_state.won = True


# Giao dien
st.title("💣 DÒ MÌN")
st.caption("Tìm tất cả ô an toàn và tránh những quả mìn!")

st.write(
    f"🚩 Đã cắm cờ: "
    f"{len(st.session_state.flags)}/{MINE_COUNT}"
)

st.write(
    f"🟩 Đã mở: "
    f"{len(st.session_state.revealed)}/"
    f"{ROWS * COLS - MINE_COUNT} ô an toàn"
)

flag_mode = st.checkbox(
    "🚩 Chế độ cắm cờ (bật để đánh dấu mìn)"
)

st.info(
    "Chạm vào ô để mở. "
    "Bật chế độ cắm cờ rồi chạm ô để đánh dấu."
)

# Ban co
for r in range(ROWS):
    columns = st.columns(COLS)

    for c in range(COLS):
        cell = r * COLS + c
        is_mine = cell in st.session_state.mines
        is_revealed = cell in st.session_state.revealed
        is_flagged = cell in st.session_state.flags

        # Hien thi noi dung o
        if is_revealed:
            if is_mine:
                label = "💥"
            else:
                number = st.session_state.numbers[cell]
                label = str(number) if number > 0 else "·"
        elif st.session_state.game_over and is_mine:
            label = "💣"
        elif is_flagged:
            label = "🚩"
        else:
            label = "⬜"

        disabled = (
            is_revealed
            or st.session_state.game_over
        )

        with columns[c]:
            if st.button(
                label,
                key=f"cell_{cell}",
                disabled=disabled,
                use_container_width=True
            ):
                if flag_mode:
                    if cell in st.session_state.flags:
                        st.session_state.flags.remove(cell)
                    else:
                        st.session_state.flags.add(cell)
                else:
                    reveal_cell(cell)

                st.rerun()

# Ket qua
if st.session_state.game_over:
    st.divider()

    if st.session_state.won:
        st.balloons()
        st.success("🏆 CHIẾN THẮNG! bạn đã tìm hết các ô an toàn!")
    else:
        st.error("💥 BOOM! bạn đã chạm trúng mìn!")

    st.write("Bấm bên dưới để tạo bàn cờ mới.")

if st.button("🔄 CHƠI VÁN MỚI", use_container_width=True):
    new_game()
    st.rerun()