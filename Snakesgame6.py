import streamlit as st
import time
import random

# --- Game Engine Functions ---

def play_turn(position, action, snakes_and_ladders, board_size=30, terminal_state=30):
    """Given a position and an action, compute the next position with rewards and check for terminal state."""
    if position == terminal_state:
        return 0, position, True
    if action == 1:
        move = 1
        cost = -3
    elif action == 2:
        move = random.choice([1, 2, 3])
        cost = -1
    elif action == 3:
        move = random.choice([4, 5, 6, 7])
        cost = -2
    else:
        raise ValueError("Invalid action. Must be 1, 2, or 3.")
    
    temp_position = position + move
    if temp_position > board_size:
        extra_steps = temp_position - board_size
        reward = cost - extra_steps
        next_position = 1
    elif temp_position == board_size:
        reward = cost + 10
        next_position = temp_position
    else:
        reward = cost
        next_position = temp_position
    
    # Apply snakes or ladders
    if next_position in snakes_and_ladders:
        next_position = snakes_and_ladders[next_position]
    
    done = (next_position == terminal_state)
    return reward, next_position, done

def optimal_policy(state):
    """Returns the optimal action for a given state (used by the computer)."""
    optimal_policy_dict = {
        1: 3, 2: 3, 3: 3, 4: 3, 6: 3, 7: 3, 8: 3, 10: 3,
        12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 18: 3, 19: 3,
        21: 3, 22: 3, 23: 3, 25: 3, 26: 2, 27: 2, 28: 2, 29: 1
    }
    return optimal_policy_dict.get(state, 1)

def generate_board_html(player_positions, snakes_and_ladders):
    """
    Generate HTML for the board.
    player_positions: dict with keys "player" and "computer" and their current cell numbers.
    """
    board = []
    # Build a 5x6 board with zigzag rows
    for row in range(5):
        row_start = row * 6 + 1
        row_end = row_start + 6
        row_positions = list(range(row_start, row_end))
        if row % 2 == 1:
            row_positions.reverse()
        board.append(row_positions)

    # Enhanced CSS styling for a visually appealing board
    html = """
    <style>
    .board {
        display: grid;
        grid-template-columns: repeat(6, 80px);
        gap: 4px;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        padding: 10px;
        border: 3px solid #333;
        border-radius: 15px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
        width: fit-content;
        margin: auto;
    }
    .cell {
        width: 80px;
        height: 80px;
        background-color: #fff;
        border: 2px solid #ddd;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        position: relative;
    }
    .player {
        background-color: yellow;
        border: 2px solid #f39c12;
    }
    .computer {
        background-color: #d1f0ff;
        border: 2px solid #3498db;
    }
    .ladder {
        background-color: #a8e6cf; /* Soft green */
    }
    .snake {
        background-color: #ff8b94; /* Soft red */
    }
    </style>
    <div class="board">
    """

    # Populate the grid with cells
    for row in board:
        for pos in row:
            cell_class = "cell"
            content = f"{pos}"
            
            # Mark snakes or ladders
            if pos in snakes_and_ladders:
                if snakes_and_ladders[pos] > pos:
                    cell_class += " ladder"
                    content = f"🪜 {pos}"
                else:
                    cell_class += " snake"
                    content = f"🐍 {pos}"
            
            # Check if players occupy this cell
            cell_icons = ""
            if pos == player_positions.get("player"):
                cell_class += " player"
                cell_icons += "🚶"
            if pos == player_positions.get("computer"):
                cell_class += " computer"
                cell_icons += "🤖"
            if cell_icons:
                content = f"{cell_icons} {pos}"
            
            html += f'<div class="{cell_class}">{content}</div>'
    html += "</div>"
    return html

# --- Streamlit Game Setup ---

st.title("Two-Player Snakes and Ladders: You vs Computer")

# Define a reset function to reinitialize game state
def reset_game():
    st.session_state.p1_position = 1
    st.session_state.p2_position = 1
    st.session_state.turn = "player"  # 'player' or 'computer'
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.winner = ""

# Create a Reset Game button that calls reset_game when clicked
st.button("Reset Game", on_click=reset_game)

# Initialize game state in session_state if not already set
if "p1_position" not in st.session_state:
    reset_game()
    st.session_state.snakes_and_ladders = {5: 7, 9: 27, 11: 29, 17: 4, 20: 6, 24: 16}
    st.session_state.board_size = 30
    st.session_state.terminal_state = 30

# Create placeholders for game info and board display
info_placeholder = st.empty()
board_placeholder = st.empty()

# --- Game Logic with Callbacks Instead of Forcing a Rerun ---

# Player's Turn
if not st.session_state.game_over and st.session_state.turn == "player":
    st.write("**Your Turn!** Choose your action:")
    # Descriptive labels for each action
    actions = {
        1: "Action 1: Move exactly 1 step (Cost: -3)",
        2: "Action 2: Move between 1 and 3 steps (Cost: -1)",
        3: "Action 3: Move between 4 and 7 steps (Cost: -2)"
    }
    with st.form("player_form", clear_on_submit=True):
        action = st.radio("Select an action:", options=list(actions.keys()),
                          format_func=lambda x: actions[x])
        submitted = st.form_submit_button("Make Move")
    if submitted:
        reward, new_pos, done = play_turn(
            st.session_state.p1_position,
            action,
            st.session_state.snakes_and_ladders,
            st.session_state.board_size,
            st.session_state.terminal_state
        )
        st.session_state.p1_position = new_pos
        st.session_state.message = f"You chose {actions[action]} and moved to {new_pos} (Reward: {reward})."
        if done:
            st.session_state.game_over = True
            st.session_state.winner = "You"
        else:
            st.session_state.turn = "computer"

# Computer's Turn
if not st.session_state.game_over and st.session_state.turn == "computer":
    st.write("**Computer's Turn...**")
    time.sleep(1)  # Simulate thinking
    comp_action = optimal_policy(st.session_state.p2_position)
    reward, new_pos, done = play_turn(
        st.session_state.p2_position,
        comp_action,
        st.session_state.snakes_and_ladders,
        st.session_state.board_size,
        st.session_state.terminal_state
    )
    st.session_state.p2_position = new_pos
    st.session_state.message = f"Computer chose Action {comp_action} and moved to {new_pos} (Reward: {reward})."
    if done:
        st.session_state.game_over = True
        st.session_state.winner = "Computer"
    else:
        st.session_state.turn = "player"

# --- Update the Display ---
player_positions = {
    "player": st.session_state.p1_position,
    "computer": st.session_state.p2_position
}
board_html = generate_board_html(player_positions, st.session_state.snakes_and_ladders)

info_placeholder.markdown(f"""
**Your Position:** {st.session_state.p1_position}  
**Computer Position:** {st.session_state.p2_position}  
**Message:** {st.session_state.message}
""")

board_placeholder.markdown(board_html, unsafe_allow_html=True)

if st.session_state.game_over:
    st.write(f"**Game Over! Winner: {st.session_state.winner}**")
