# state.py
#
# Defines the canonical state representation for the Inglenook Shunting Puzzle.
#
# State shape: tuple of four tuples, one per track.
#
#   (track1, track2, track3, track4)
#
# Each inner tuple contains wagon labels (strings) ordered from the open
# (headshunt-facing) end inward, i.e. index 0 is always the end the
# locomotive accesses first.
#
# The locomotive is not stored in the state — it always resides in the
# headshunt (track1) at the open end (index 0), implicitly, at every
# state boundary between moves.
#
# See solver-design-decisions.md for full rationale.

# ---------------------------------------------------------------------------
# Track indices
# ---------------------------------------------------------------------------

HEADSHUNT = 0
TRACK2    = 1
TRACK3    = 2
TRACK4    = 3

# ---------------------------------------------------------------------------
# Track capacities (wagon slots; loco is not counted)
# ---------------------------------------------------------------------------

CAPACITY = (3, 5, 3, 3)

# ---------------------------------------------------------------------------
# Convenience collections
# ---------------------------------------------------------------------------

SIDINGS = (TRACK2, TRACK3, TRACK4)  # tracks where the loco may decouple

# ---------------------------------------------------------------------------
# Type alias (documentation only — Python does not enforce it)
# ---------------------------------------------------------------------------

# State = tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...]]

# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------

def make_initial_state(track2, track3, track4):
    """Return the canonical starting state for a puzzle.

    Args:
        track2: Sequence of wagon labels for Track 2, ordered from the open
                end inward (index 0 = mouth of siding).
        track3: Same for Track 3.
        track4: Same for Track 4.

    Returns:
        A hashable state tuple with an empty headshunt and the three sidings
        populated as specified.

    Raises:
        ValueError: If any siding exceeds its capacity, contains duplicates,
                    or uses the reserved label 'L'.
    """
    tracks = {
        TRACK2: (tuple(track2), CAPACITY[TRACK2]),
        TRACK3: (tuple(track3), CAPACITY[TRACK3]),
        TRACK4: (tuple(track4), CAPACITY[TRACK4]),
    }

    all_wagons = []
    for idx, (wagons, cap) in tracks.items():
        if len(wagons) > cap:
            raise ValueError(
                f"Track {idx + 1} has capacity {cap} but received {len(wagons)} wagons."
            )
        for label in wagons:
            if label == 'L':
                raise ValueError("'L' is reserved for the locomotive and cannot be a wagon label.")
        all_wagons.extend(wagons)

    if len(all_wagons) != len(set(all_wagons)):
        raise ValueError("Wagon labels must be unique across all tracks.")

    return (
        (),                  # headshunt starts empty
        tracks[TRACK2][0],
        tracks[TRACK3][0],
        tracks[TRACK4][0],
    )
