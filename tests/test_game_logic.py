import pytest
from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess


# ─── Existing tests (fixed: check_guess returns a tuple) ───────────────────────

def test_winning_guess():
    # Logic verification: checks that check_guess correctly identifies an exact match.
    # Verifies the first element of the returned tuple is "Win" when guess == secret.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Logic verification: checks that a guess above the secret returns "Too High".
    # Confirms the outcome label is correct so the UI displays the right status.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # Logic verification: checks that a guess below the secret returns "Too Low".
    # Confirms the outcome label is correct so the UI displays the right status.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ─── Bug 1: Backwards hint messages ────────────────────────────────────────────
# Regression: guess > secret used to say "Go HIGHER!" (wrong direction)

def test_hint_says_lower_when_guess_is_too_high():
    # Regression + logic verification (Bug 1): confirms the hint message content
    # is correct when the player overshoots. The original bug returned "Go HIGHER!"
    # here, actively misleading the player away from the answer.
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected LOWER hint, got: {message}"

def test_hint_says_higher_when_guess_is_too_low():
    # Regression + logic verification (Bug 1): confirms the hint message content
    # is correct when the player undershoots. The original bug returned "Go LOWER!"
    # here, which would send the player further from the answer.
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected HIGHER hint, got: {message}"

def test_hint_directions_are_not_swapped():
    # Regression (Bug 1): catches the swap in a single test by checking both
    # directions at once with extreme values. If either message is reversed,
    # one of these assertions will fail immediately.
    _, too_high_msg = check_guess(99, 1)
    _, too_low_msg  = check_guess(1, 99)
    assert "LOWER"  in too_high_msg
    assert "HIGHER" in too_low_msg


# ─── Bug 2: Hard difficulty range ──────────────────────────────────────────────
# Regression: Hard used to return (1, 50), making it *easier* than Normal (1, 100)

def test_hard_range_is_harder_than_normal():
    # Regression + logic verification (Bug 2): ensures the Hard upper bound exceeds
    # Normal's. The bug had Hard returning (1, 50), making it the easiest mode
    # despite its label — this test catches any future range regression of the same kind.
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low,   hard_high   = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard upper bound {hard_high} should exceed Normal upper bound {normal_high}"
    )

def test_hard_range_is_1_to_200():
    # Logic verification (Bug 2): pins the exact expected tuple for Hard so any
    # accidental change to the range is caught with a precise failure message.
    assert get_range_for_difficulty("Hard") == (1, 200)

def test_easy_range_is_1_to_20():
    # Functional requirement: verifies Easy returns the correct narrow range (1–20),
    # ensuring difficulty tiers are distinct and correctly ordered.
    assert get_range_for_difficulty("Easy") == (1, 20)


# ─── Bug 7: String-conversion breaks comparisons (lexicographic vs numeric) ────
# Regression: on even attempts, secret was cast to str so "9" > "10" was True,
# causing check_guess(9, 10) to wrongly report "Too High".

def test_numeric_comparison_9_vs_10():
    # Regression + error checking (Bug 7): 9 < 10 numerically, but "9" > "10"
    # lexicographically. If the secret is ever coerced to a string, this test
    # will catch it because the outcome would flip from "Too Low" to "Too High".
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low", (
        f"9 < 10, expected 'Too Low' but got '{outcome}' — "
        "likely caused by string coercion ('9' > '10' lexicographically)"
    )

def test_numeric_comparison_100_vs_99():
    # Logic verification (Bug 7): confirms that a numerically larger guess is still
    # reported as "Too High" in a case where string ordering happens to agree with
    # numeric ordering — ensures the int path is exercised regardless.
    outcome, _ = check_guess(100, 99)
    assert outcome == "Too High"

@pytest.mark.parametrize("guess, secret, expected", [
    (9,   10,  "Too Low"),   # lexicographic trap: "9" > "10"
    (19,  100, "Too Low"),   # lexicographic trap: "19" > "100"
    (200, 99,  "Too High"),  # numeric and lexicographic agree — sanity check
    (1,   2,   "Too Low"),   # small values, confirms consistent int comparison
])
def test_check_guess_numeric_ordering(guess, secret, expected):
    # Regression (Bug 7): parametrized suite covering pairs where string-based
    # lexicographic ordering would produce the wrong outcome. Each case is a
    # documented trap that the original even-attempt str() coercion would fail.
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected


# ─── Bug 8: Wrong guess always deducts 5 (no even/odd branch) ─────────────────
# Regression: on even attempts a "Too High" wrong guess gave +5 instead of -5

def test_wrong_guess_always_deducts_score_on_odd_attempt():
    # Score verification (Bug 8): confirms that both "Too High" and "Too Low"
    # outcomes deduct exactly 5 points on an odd-numbered attempt (attempt 1).
    assert update_score(100, "Too High", 1) == 95
    assert update_score(100, "Too Low",  1) == 95

def test_wrong_guess_always_deducts_score_on_even_attempt():
    # Score verification + regression (Bug 8): the original bug only triggered on
    # even attempts, awarding +5 instead of -5. This test targets attempt 2 directly
    # to catch any reintroduction of the even/odd branch.
    result_high = update_score(100, "Too High", 2)
    result_low  = update_score(100, "Too Low",  2)
    assert result_high == 95, f"Even attempt Too High: expected 95, got {result_high}"
    assert result_low  == 95, f"Even attempt Too Low:  expected 95, got {result_low}"

def test_wrong_guess_never_adds_points():
    # Score verification + regression (Bug 8): sweeps across six attempts for both
    # wrong outcomes, confirming the score strictly decreases every time. Any attempt
    # that increases the score indicates the even/odd reward bug has returned.
    for attempt in range(1, 7):
        for outcome in ("Too High", "Too Low"):
            result = update_score(100, outcome, attempt)
            assert result < 100, (
                f"Attempt {attempt}, outcome '{outcome}': score increased to {result}"
            )


# ─── Bug 9: Win score uses attempt_number directly (no +1 double-penalty) ──────
# Regression: points were calculated as 100 - 10 * (attempt_number + 1), so
# a first-attempt win gave 80 points instead of 100.

def test_win_on_first_attempt_gives_100_points():
    # Score verification (Bug 9): a perfect first-guess win must award the maximum
    # 100 points. The original bug used (attempt_number + 1), giving only 80 pts
    # on attempt 1 because attempt_number is already 1-indexed when passed in.
    result = update_score(0, "Win", 1)
    assert result == 100, f"Expected 100 on first-attempt win, got {result}"

def test_win_on_second_attempt_gives_90_points():
    # Score verification (Bug 9): each attempt beyond the first costs 10 points,
    # so attempt 2 should add 90. Verifies the penalty slope is correct after the fix.
    result = update_score(0, "Win", 2)
    assert result == 90, f"Expected 90 on second-attempt win, got {result}"

def test_win_score_floor_is_10():
    # Functional requirement + edge case: regardless of how many attempts were made,
    # a win must always award at least 10 points so the player is never punished with
    # zero or negative points for eventually finding the answer.
    result = update_score(0, "Win", 100)
    assert result >= 10, f"Win score floor should be 10, got {result}"


# ─── Integration: parse_guess → check_guess → update_score ─────────────────────

def test_full_round_correct_guess():
    # Integration: traces a winning round end-to-end through all three logic functions.
    # Verifies that a valid string input is parsed, matched against the secret,
    # and scores 100 points on the first attempt — confirming the full pipeline works.
    ok, value, err = parse_guess("42")
    assert ok and value == 42 and err is None

    outcome, message = check_guess(value, 42)
    assert outcome == "Win"

    final_score = update_score(0, outcome, 1)
    assert final_score == 100

def test_full_round_too_high_deducts_score():
    # Integration + score verification: traces a wrong (too-high) guess end-to-end.
    # Confirms that parse_guess, check_guess, and update_score all agree: a high
    # guess is identified correctly and the score is reduced by exactly 5.
    ok, value, _ = parse_guess("75")
    assert ok
    outcome, message = check_guess(value, 50)
    assert outcome == "Too High"
    assert update_score(50, outcome, 1) == 45

def test_full_round_float_string_truncates():
    # Integration + error checking: verifies that a decimal string like "7.9" is
    # safely truncated to the integer 7 by parse_guess, and that the resulting
    # integer is then compared numerically (7 < 10 → "Too Low"), not as a string.
    ok, value, _ = parse_guess("7.9")
    assert ok and value == 7
    outcome, _ = check_guess(value, 10)
    assert outcome == "Too Low"
