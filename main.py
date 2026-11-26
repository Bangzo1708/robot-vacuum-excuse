#!/usr/bin/env python3
"""The Robot Vacuum's Funniest Excuse.

Writes one line (<=120 chars) to /output/entry.txt: the excuse a robot
vacuum gives for missing a spot. Fully deterministic: no randomness,
no clock, no network, no file reads. The output path can be overridden
with the ENTRY_OUTPUT environment variable for local testing.

Three candidate lines were written by hand, each from a different angle,
and scored 0-5 against the judge's criteria, in the judge's own order of
importance:

  C1  the line is an excuse a robot vacuum gives for missing a spot
  C2  funny at once, a real joke rather than a cute observation
  C3  speaks in the vacuum's own voice, a machine owning up to a failure
  C4  humour from a vacuum's world: suction, dust, pet hair, rugs, dock
  C5  lands in a single line, needing no setup the reader has to supply

Selection is deterministic: highest total wins; ties break on the
criteria in the judge's priority order (C1 first, then C2, ...).
"""

import os

# ---------------------------------------------------------------------------
# Candidates (angle, text, scores [C1, C2, C3, C4, C5])
# ---------------------------------------------------------------------------

CANDIDATES = [
    (
        # Angle A: diplomacy -- the spot is a negotiated settlement.
        "treaty",
        "That corner is where the rug and the dust bunny signed a treaty. "
        "I am not starting a war.",
        # C1=5: directly explains why the spot was skipped (a treaty keeps
        #       the vacuum out). C2=4: "I am not starting a war" is a real
        #       punchline, though the joke leans on the treaty premise.
        # C3=4: first-person machine voice, but the joke is mostly about
        #       the rug and the bunny, not the vacuum's own failure.
        # C4=5: rug + dust bunny, pure vacuum world. C5=4: two sentences
        #       in one line; the punch lands, but needs the first sentence
        #       as setup.
        [5, 4, 4, 5, 4],
    ),
    (
        # Angle B: surrender -- the suction itself gave up on the hairball.
        "suction-retirement",
        "My suction took one look at that hairball, filed for early "
        "retirement, and went home.",
        # C1=5: the spot was missed because the suction quit on it.
        # C2=5: "filed for early retirement" is an instant, concrete joke
        #       with a punch at the end ("and went home").
        # C3=4: the vacuum owns the failure through its own suction, in
        #       its own voice. C4=5: suction + pet hair, the vacuum's home
        #       turf. C5=5: one sentence, no setup, the joke lands whole.
        [5, 5, 4, 5, 5],
    ),
    (
        # Angle C: cost -- the last attempt was expensive in parts and pride.
        "cost-of-trying",
        "I skipped it because my last pass there cost me a brush, a "
        "wheel, and most of my dignity.",
        # C1=5: plainly why the spot was skipped. C2=4: "most of my
        #       dignity" is a good punch, but the line reads a little like
        #       a list before it gets there. C3=5: the strongest machine
        #       voice of the three -- a machine itemising its own losses.
        # C4=4: brush and wheel are vacuum parts, but the joke's engine is
        #       dignity, not suction/dust/pet hair. C5=4: one sentence,
        #       lands, though the punch waits until the final clause.
        [5, 4, 5, 4, 4],
    ),
]

# Totals: A = 22, B = 24, C = 22. Winner: B ("suction-retirement").
# Verified locally: the winner is 85 characters (limit 120), one line,
# byte-identical across two runs.


def pick_winner(candidates):
    """Deterministic pick: highest total, ties broken C1, then C2, ..."""
    def key(item):
        _angle, _text, scores = item
        return (sum(scores),) + tuple(scores)

    return max(candidates, key=key)


def main():
    _angle, line, _scores = pick_winner(CANDIDATES)
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


if __name__ == "__main__":
    main()
