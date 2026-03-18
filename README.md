# RL-Powered Snakes & Ladders: Human vs. AI

## Overview
This project is an interactive, web-based implementation of a modified Snakes and Ladders game built with Python and Streamlit. It pits a human player against a computer agent guided by a pre-computed Reinforcement Learning (RL) optimal policy. 

**Live Demo:** [Play on Streamlit](https://snakesgame.streamlit.app/) *(Note: May require waking the app if idle).*

## Features
* **Interactive UI:** A custom HTML/CSS 5x6 grid board rendered dynamically within Streamlit, featuring visual indicators for players, snakes, and ladders.
* **Strategic Gameplay:** Unlike traditional dice-rolling, players must choose between specific actions with varying risks and step ranges.
* **AI Opponent:** The computer agent operates using a pre-calculated `optimal_policy_dict` mapped to all possible board states. This deterministic optimal policy was generated offline by formulating the stochastic game environment as a Markov Decision Process (MDP) and applying the Value Iteration algorithm to maximize expected cumulative rewards over time.
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
* **Snakes:** Landing on 17, 20, or 24 sends the player backward.

## The Reinforcement Learning Agent


The agent does not play randomly. It utilizes a pre-computed `optimal_policy_dict` mapped to board states. This deterministic optimal policy was generated offline by formulating the environment as a Markov Decision Process (MDP) and applying the Value Iteration algorithm to maximize expected cumulative rewards over time.

## Installation & Execution
Requires Python 3.7+ and Streamlit.

```bash
git clone [https://github.com/Pooya-s/RL-Snakes-Ladders.git](https://github.com/Pooya-s/Snakes_and_ladders_game.git)
cd Snakes_and_ladders_game
pip install -r requirements.txt
streamlit run app.py
