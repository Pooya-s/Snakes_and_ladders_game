# RL-Powered Snakes & Ladders: Human vs. AI

## Overview
This project is an interactive, web-based implementation of a modified Snakes and Ladders game built with Python and Streamlit. It pits a human player against a computer agent guided by a pre-computed Reinforcement Learning (RL) optimal policy. 

### Link_to_the_game
since the streamlit deactivates the game when Idle, it probably wouldn't work, you can clone and deploy it yourself, you might decide to improve it as well!!
here goes nothing : https://snakesgame.streamlit.app/

## Features
* **Interactive UI:** A custom HTML/CSS 5x6 grid board rendered dynamically within Streamlit, featuring visual indicators for players, snakes, and ladders.
* **Strategic Gameplay:** Unlike traditional dice-rolling, players must choose between specific actions with varying risks and step ranges.
* **AI Opponent:** The computer uses a pre-calculated optimal policy dictionary derived from a Markov Decision Process (MDP) to select the best possible move for any given state.

## Game Mechanics
The objective is to reach exactly cell 30 (the terminal state). If a move pushes a player past 30, they bounce back to the start (cell 1) and incur a penalty.

### Action Space & Rewards
Players must balance the cost of a move against the distance traveled. 

| Action | Move Range | Cost/Reward |
| :--- | :--- | :--- |
| **Action 1** | Exactly 1 step | -3 |
| **Action 2** | Random (1 to 3 steps) | -1 |
| **Action 3** | Random (4 to 7 steps) | -2 |

### Board Layout
* **Ladders:** Landing on 5, 9, 11, 20, or 24 advances the player forward.
* **Snakes:** Landing on 17 sends the player backward (to 4).

## The Reinforcement Learning Agent


The computer does not play randomly. It utilizes an `optimal_policy_dict` mapped to board states. This policy was likely generated offline using dynamic programming algorithms (like Value Iteration or Policy Iteration) to maximize the expected reward while navigating the stochastic nature of Actions 2 and 3 and the board's traps.

## Installation & Execution

1. **Prerequisites:** Ensure you have Python 3.7+ installed.
2. **Install Streamlit:**
   ```bash
   pip install streamlit
