# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose
This is a number guessing game where the player tries to guess a randomly generated secret number within a limited number of attempts, with difficulty settings that adjust the number range and attempt limit. The game provides higher/lower hints after each guess and tracks a running score based on how quickly the player finds the correct answer.

### Bugs Found
1. **Backwards hints** — the hint said "Go HIGHER!" when the guess was too high and "Go LOWER!" when it was too low, the exact opposite of correct.
2. **Hard difficulty range too small** — Hard was set to 1–50, making it easier than Normal (1–100) rather than harder.
3. **Attempt counter off by one** — attempts were initialized to 1 instead of 0, causing the display to show one fewer attempt remaining than was actually allowed.
4. **New Game ignored difficulty** — clicking New Game always generated the secret from 1–100 regardless of which difficulty was selected.
5. **Info banner hardcoded to 1–100** — the "Guess a number between..." message never updated when difficulty changed.
6. **Switching difficulty kept the old secret** — changing difficulty mid-game did not regenerate the secret, leaving an out-of-range number from the previous setting.
7. **String comparison on even attempts** — every even attempt converted the secret to a string, causing lexicographic bugs where "9" > "10" even though 9 < 10.
8. **Wrong guesses could award points** — a "Too High" guess on even-numbered attempts gave +5 points instead of deducting -5, rewarding incorrect answers.
9. **Win score double-penalized attempts** — the formula used  even though attempts were already incremented before the call, over-penalizing the player.

### Fixes Applied
1. **Backwards hints** — swapped the return messages in  so "Too High" maps to "Go LOWER!" and "Too Low" maps to "Go HIGHER!".
2. **Hard difficulty range** — changed the Hard return value from  to  so it is genuinely harder than Normal.
3. **Attempt counter** — changed  initialization from  to  so the displayed count is accurate from the first load.
4. **New Game range** — replaced the hardcoded  with  so new games respect the selected difficulty.
5. **Info banner** — replaced the hardcoded  with  so the message always reflects the active difficulty range.
6. **Difficulty change reset** — added a difficulty-tracking block that detects when difficulty changes and regenerates the secret and all game state.
7. **String comparison** — removed the even/odd attempt string conversion so the secret is always an integer during comparison.
8. **Wrong guess scoring** — removed the  branch so all wrong guesses consistently deduct 5 points.
9. **Win score formula** — changed  to  to correctly calculate points.

## 📸 Demo
- [ ] ![Winning game screenshot]([Screenshot 2026-03-15 123928.png](https://github.com/cmirandavega/ai110-module1show-gameglitchinvestigator-starter/blob/main/Screenshot%202026-03-15%20123928.png))


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
