import streamlit as st
import random
import time

st.set_page_config(page_title="Snake Combat", layout="centered")

# --- Constants ---
GRID_SIZE = 20
SPEED = 0.25
MAX_HEALTH = 100
ENEMY_COUNT = 5

# --- Initialize State ---
def init_game():
    st.session_state.snake = [(10, 10), (10, 9), (10, 8)]
    st.session_state.direction = "RIGHT"
    st.session_state.weapon = False
    st.session_state.health = MAX_HEALTH
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.weapon_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.medkit_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.enemies = {
        i: (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        for i in range(ENEMY_COUNT)
    }

if "snake" not in st.session_state:
    init_game()

# --- Title ---
st.title("🐍 Snake Combat: Survival Edition")
st.caption("Use W/A/S/D or Arrow Keys to move. Collect 🔫 weapons, heal with 💊, and defeat 👾 enemies!")

# --- Keyboard Controls ---
key = st.key_input("Press direction key (WASD or arrows):", key="snake_key")

if key:
    if key.lower() in ["w", "arrowup"] and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
    elif key.lower() in ["s", "arrowdown"] and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
    elif key.lower() in ["a", "arrowleft"] and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
    elif key.lower() in ["d", "arrowright"] and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

# --- Drawing ---
def draw_grid():
    grid = ""
    enemy_positions = list(st.session_state.enemies.values())
    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            pos = (y, x)
            if pos in st.session_state.snake:
                row += "🟩"
            elif pos == st.session_state.weapon_tile:
                row += "🔫"
            elif pos in enemy_positions:
                row += "👾"
            elif pos == st.session_state.medkit_tile:
                row += "💊"
            else:
                row += "⬛"
        grid += row + "\n"
    return grid

# --- Move Snake ---
def move_snake():
    head_y, head_x = st.session_state.snake[0]
    if st.session_state.direction == "UP":
        head_y -= 1
    elif st.session_state.direction == "DOWN":
        head_y += 1
    elif st.session_state.direction == "LEFT":
        head_x -= 1
    elif st.session_state.direction == "RIGHT":
        head_x += 1

    new_head = (head_y, head_x)

    # Wall/self collision
    if (
        head_x < 0 or head_x >= GRID_SIZE or
        head_y < 0 or head_y >= GRID_SIZE or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # Interactions
    if new_head == st.session_state.weapon_tile:
        st.session_state.weapon = True
        st.session_state.weapon_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

    elif new_head in st.session_state.enemies.values():
        if st.session_state.weapon:
            # Defeat enemy
            for k, v in list(st.session_state.enemies.items()):
                if v == new_head:
                    del st.session_state.enemies[k]
                    break
            st.session_state.weapon = False
            st.session_state.score += 1
        else:
            # Take damage
            st.session_state.health -= 30
            if st.session_state.health <= 0:
                st.session_state.game_over = True
                return

    elif new_head == st.session_state.medkit_tile:
        st.session_state.health = min(MAX_HEALTH, st.session_state.health + 40)
        st.session_state.medkit_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    else:
        st.session_state.snake.pop()

# --- Move Enemies ---
def move_enemies():
    new_enemies = {}
    for k, (y, x) in st.session_state.enemies.items():
        direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        if direction == "UP": y -= 1
        elif direction == "DOWN": y += 1
        elif direction == "LEFT": x -= 1
        elif direction == "RIGHT": x += 1

        # keep inside grid
        y = max(0, min(GRID_SIZE - 1, y))
        x = max(0, min(GRID_SIZE - 1, x))

        new_enemies[k] = (y, x)
    st.session_state.enemies = new_enemies

# --- Main Game Loop ---
placeholder = st.empty()

if not st.session_state.game_over:
    move_snake()
    move_enemies()
    with placeholder.container():
        st.text(draw_grid())
        st.markdown(f"**Health:** ❤️ {st.session_state.health}")
        st.markdown(f"**Weapon:** {'🔫 Equipped' if st.session_state.weapon else '❌ None'}")
        st.markdown(f"**Score:** {st.session_state.score}")
    time.sleep(SPEED)
    st.rerun()
else:
    st.error("💀 Game Over!")
    st.write(f"Final Score: **{st.session_state.score}**")
    if st.button("🔁 Restart Game"):
        init_game()
        st.rerun()

