import streamlit as st
import random
import time

st.set_page_config(page_title="Snake Combat", layout="centered")

# Constants
GRID_SIZE = 20
SPEED = 0.3  # seconds per move
MAX_HEALTH = 100

# Initialize game state
if "snake" not in st.session_state:
    st.session_state.snake = [(10, 10), (10, 9), (10, 8)]
if "direction" not in st.session_state:
    st.session_state.direction = "RIGHT"
if "weapon" not in st.session_state:
    st.session_state.weapon = False
if "health" not in st.session_state:
    st.session_state.health = MAX_HEALTH
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "weapon_tile" not in st.session_state:
    st.session_state.weapon_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
if "enemy_tile" not in st.session_state:
    st.session_state.enemy_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
if "medkit_tile" not in st.session_state:
    st.session_state.medkit_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

st.title("🐍 Snake Combat")
st.caption("Survive, collect weapons, defeat enemies, and heal with med-kits!")

# Control buttons
cols = st.columns(3)
with cols[1]:
    up = st.button("⬆️ Up")
with cols[0]:
    left = st.button("⬅️ Left")
with cols[2]:
    right = st.button("➡️ Right")
with cols[1]:
    down = st.button("⬇️ Down")

if up and st.session_state.direction != "DOWN":
    st.session_state.direction = "UP"
elif down and st.session_state.direction != "UP":
    st.session_state.direction = "DOWN"
elif left and st.session_state.direction != "RIGHT":
    st.session_state.direction = "LEFT"
elif right and st.session_state.direction != "LEFT":
    st.session_state.direction = "RIGHT"

# Draw grid
def draw_grid():
    grid = ""
    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            pos = (y, x)
            if pos in st.session_state.snake:
                row += "🟩"
            elif pos == st.session_state.weapon_tile:
                row += "🔫"
            elif pos == st.session_state.enemy_tile:
                row += "👾"
            elif pos == st.session_state.medkit_tile:
                row += "💊"
            else:
                row += "⬛"
        grid += row + "\n"
    return grid

# Move snake logic
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

    # Collisions with wall or self
    if (
        head_x < 0 or head_x >= GRID_SIZE
        or head_y < 0 or head_y >= GRID_SIZE
        or new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # Interactions
    if new_head == st.session_state.weapon_tile:
        st.session_state.weapon = True
        st.session_state.weapon_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

    elif new_head == st.session_state.enemy_tile:
        if st.session_state.weapon:
            st.session_state.score += 1
            st.session_state.weapon = False  # single-use weapon
            st.session_state.enemy_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        else:
            st.session_state.health -= 30
            if st.session_state.health <= 0:
                st.session_state.game_over = True
                return
            # Move enemy elsewhere
            st.session_state.enemy_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

    elif new_head == st.session_state.medkit_tile:
        st.session_state.health = min(MAX_HEALTH, st.session_state.health + 40)
        st.session_state.medkit_tile = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

    else:
        st.session_state.snake.pop()  # move forward (no growth)

# Main loop
placeholder = st.empty()

if not st.session_state.game_over:
    for _ in range(1):
        move_snake()
        with placeholder.container():
            st.text(draw_grid())
            st.markdown(f"**Health:** ❤️ {st.session_state.health}")
            st.markdown(f"**Weapon:** {'🔫 Equipped' if st.session_state.weapon else '❌ None'}")
            st.markdown(f"**Score:** {st.session_state.score}")
        time.sleep(SPEED)
    st.rerun()  # continuous auto-move
else:
    st.error("💀 Game Over!")
    st.write(f"Final Score: **{st.session_state.score}**")
    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
