#!/usr/bin/env python3
"""One-line roast of the gadget or app you use every day.

Writes one line (<=200 chars) to /output/entry.txt, deterministically.

The line is chosen from a shortlist of candidates by an internal
heuristic score: funny first, then fresh (an angle nobody else roasts),
then neat wording, then a concrete, specific detail about how the
thing actually behaves. The winning line is the banking app's circular
login code: it texts a code to the phone that is locked until you enter
the code it just texted.
"""
import os
import tempfile

CANDIDATES = [
    # (text, funny, fresh, neat, specific) -- each 0..10
    (
        "My banking app texts a login code to my phone, which is locked "
        "until I enter the code my banking app just texted.",
        10, 10, 9, 10,
    ),
    (
        "My robot vacuum mapped my whole house in an afternoon and still "
        "gets stuck under the same chair every single day.",
        9, 8, 9, 9,
    ),
    (
        "My smartwatch celebrates when I stand up, then silently judges "
        "me for sitting back down eight seconds later.",
        9, 8, 9, 8,
    ),
    (
        "My earbuds wait until I am mid-sentence on a call to disconnect, "
        "like tiny wireless cowards.",
        9, 9, 9, 8,
    ),
    (
        "My TV remote has 47 buttons and I use exactly one, to summon the "
        "menu that hides the other 46.",
        8, 8, 8, 9,
    ),
    (
        "My smart coffee maker needs a firmware update before it will "
        "make coffee, which is the opposite of the point of coffee.",
        8, 8, 8, 8,
    ),
    (
        "My phone helpfully warns me I have too many notifications, then "
        "adds itself to the pile.",
        8, 8, 9, 7,
    ),
]

# Judge weights, most important first: funny, fresh, neat, specific.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    text, funny, fresh, neat, specific = candidate
    total = (
        funny * WEIGHTS[0]
        + fresh * WEIGHTS[1]
        + neat * WEIGHTS[2]
        + specific * WEIGHTS[3]
    )
    return total


def pick():
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        if len(candidate[0]) > 200:
            continue
        # The line must name a concrete daily gadget or app.
        if not any(word in candidate[0] for word in ("My ", "my ")):
            continue
        s = score(candidate)
        # On a tie, the shorter line wins: tight and neatly worded.
        if s > best_score or (s == best_score and len(candidate[0]) < len(best)):
            best_score = s
            best = candidate[0]
    return best


def main():
    text = pick()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
