# app.py Bug Fix Instructions

Fix all bugs in `app.py`. Here is the full list with exact locations:

## Bug 1 — Backwards hints (lines 38-40 and 46-47)
In `check_guess`, the messages are swapped. When guess is too high it says "Go HIGHER!" and when too low it says "Go LOWER!" — both are backwards.

Fix lines 38-40:
- Change: `return "Too High", "📈 Go HIGHER!"`
- To:     `return "Too High", "📉 Go LOWER!"`
- Change: `return "Too Low", "📉 Go LOWER!"`
- To:     `return "Too Low", "📈 Go HIGHER!"`

Also fix lines 46-47 (the except TypeError block) the same way.

## Bug 2 — Hard difficulty range is wrong (line 10)
Hard returns `1, 50` which is easier than Normal (`1, 100`). Hard should be harder.
- Change: `return 1, 50`
- To:     `return 1, 200`

## Bug 3 — Attempts initialized to 1 instead of 0 (line 96)
This causes the "Attempts left" display to show one less than it should on load.
- Change: `st.session_state.attempts = 1`
- To:     `st.session_state.attempts = 0`

## Bug 4 — New Game ignores difficulty (line 136)
When clicking New Game, the secret is always generated from 1-100 regardless of difficulty.
- Change: `st.session_state.secret = random.randint(1, 100)`
- To:     `st.session_state.secret = random.randint(low, high)`

## Bug 5 — Info text hardcoded to 1-100 (line 110)
The info banner always says "between 1 and 100" even on Easy (1-20) or Hard.
- Change: `f"Guess a number between 1 and 100. "`
- To:     `f"Guess a number between {low} and {high}. "`

## Bug 6 — Changing difficulty doesn't reset the secret (before line 92)
The secret is only generated once on first load. Switching difficulty mid-game keeps the old secret.

Add this block BEFORE the existing `if "secret" not in st.session_state:` check:

```python
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
```
# Bug 7 — String conversion on even attempts breaks comparisons (lines 158-161)
Every even attempt converts the secret to a string, causing lexicographic comparison bugs
(e.g. "9" > "10" because "9" > "1"). This randomly breaks the game every other guess.

Remove the entire if/else block:

```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
else:
    secret = st.session_state.secret
Replace with just:


secret = st.session_state.secret
```
Also remove the now-unnecessary try/except TypeError block in check_guess (lines 36-47)
and replace the whole thing with a simple if/else:

```python
if guess > secret:
    return "Too High", "📉 Go LOWER!"
else:
    return "Too Low", "📈 Go HIGHER!"
```
# Bug 8 — Wrong guess rewards points (lines 57-60)
On even attempts, a "Too High" wrong guess gives +5 points instead of -5.

Remove the inner if attempt_number % 2 == 0 check entirely.
Replace the whole block with: return current_score - 5
# Bug 9 — Win score double-penalizes attempts (line 52)
attempt_number is already incremented before this function is called, so adding +1 again over-penalizes.

Change: points = 100 - 10 * (attempt_number + 1)
To: points = 100 - 10 * attempt_number