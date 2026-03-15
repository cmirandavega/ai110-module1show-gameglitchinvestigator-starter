# Bug Fix Log

After refactoring, core game logic now lives in `logic_utils.py` and UI/session state lives in `app.py`.
Bug fixes are documented against the current file structure.

---

## Bug 1 — Backwards hint messages
**File:** `logic_utils.py` — `check_guess()`, lines 38–41

The hint messages were swapped. A guess that was too high told the player to go higher,
and a guess that was too low told them to go lower — actively misleading the player.

```python
# Before (wrong direction):
if guess > secret:
    return "Too High", "📈 Go HIGHER!"
else:
    return "Too Low", "📉 Go LOWER!"

# After (correct direction):
if guess > secret:
    return "Too High", "📉 Go LOWER!"
else:
    return "Too Low", "📈 Go HIGHER!"
```

---

## Bug 2 — Hard difficulty range was easier than Normal
**File:** `logic_utils.py` — `get_range_for_difficulty()`, line 12

Hard returned `(1, 50)`, making its range narrower — and therefore easier — than Normal `(1, 100)`.

```python
# Before:
if difficulty == "Hard":
    return 1, 50

# After:
if difficulty == "Hard":
    return 1, 200
```

---

## Bug 3 — Attempts counter initialized to 1 instead of 0
**File:** `app.py` — lines 36 and 45

The attempts counter started at 1, so the "Attempts left" display was off by one on load.
This affected both the difficulty-change reset block (line 36) and the fallback initializer (line 45).

```python
# Before:
st.session_state.attempts = 1

# After:
st.session_state.attempts = 0
```

---

## Bug 4 — New Game button ignored difficulty setting
**File:** `app.py` — `if new_game:` block, line 85

Clicking New Game always generated a secret in the range 1–100, ignoring the selected difficulty.
The fix uses `low` and `high`, which are already resolved from `get_range_for_difficulty()` at line 28.

```python
# Before:
st.session_state.secret = random.randint(1, 100)

# After:
st.session_state.secret = random.randint(low, high)
```

---

## Bug 5 — Info banner hardcoded "between 1 and 100"
**File:** `app.py` — `st.info(...)`, line 59

The info text always read "between 1 and 100" regardless of the selected difficulty.

```python
# Before:
f"Guess a number between 1 and 100. "

# After:
f"Guess a number between {low} and {high}. "
```

---

## Bug 6 — Switching difficulty mid-game kept the old secret
**File:** `app.py` — lines 33–39

The secret was only generated on first load. Switching difficulty kept the previous secret,
so the game range shown to the player and the actual secret were out of sync.

The fix adds a difficulty-change check before the existing `if "secret" not in st.session_state` guard,
fully resetting all session state whenever the difficulty changes:

```python
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
```

---

## Bug 7 — String coercion on even attempts broke comparisons
**File:** `app.py` — `if submit:` block, line 107

On every even attempt the secret was cast to a string before being passed to `check_guess`.
This caused lexicographic comparison instead of numeric (e.g. `"9" > "10"` is `True`),
so the outcome randomly flipped on every other guess.

```python
# Before (caused string comparison on even attempts):
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
else:
    secret = st.session_state.secret

# After (always integer):
secret = st.session_state.secret
```

The `try/except TypeError` block that previously existed inside `check_guess` was also removed
as part of this fix — it only existed to paper over the type mismatch caused by this coercion.
`check_guess` in `logic_utils.py` now uses a plain `if/else` (lines 38–41).

---

## Bug 8 — Wrong guess awarded points on even attempts
**File:** `logic_utils.py` — `update_score()`, lines 55–59

An inner `if attempt_number % 2 == 0` branch inside `update_score` gave `+5` points
for a "Too High" outcome on even-numbered attempts instead of deducting `-5`.

```python
# Before (even attempts rewarded wrong guesses):
if outcome == "Too High":
    if attempt_number % 2 == 0:
        return current_score + 5
    return current_score - 5

# After (all wrong guesses always cost 5):
if outcome == "Too High":
    return current_score - 5

if outcome == "Too Low":
    return current_score - 5
```

---

## Bug 9 — Win score double-penalized attempts
**File:** `logic_utils.py` — `update_score()`, line 50

`attempt_number` is already 1-indexed when passed in (incremented in `app.py` at line 97
before `update_score` is called). The original formula used `(attempt_number + 1)`,
adding a second +1 and over-penalizing every win by 10 extra points.

```python
# Before (attempt 1 → 80 pts, attempt 2 → 70 pts):
points = 100 - 10 * (attempt_number + 1)

# After (attempt 1 → 100 pts, attempt 2 → 90 pts):
points = 100 - 10 * (attempt_number - 1)
```

*This bug was discovered through the pytest suite in `tests/test_game_logic.py`
(`test_win_on_first_attempt_gives_100_points`), which caught that a perfect
first-guess win was yielding 90 points instead of 100.*
