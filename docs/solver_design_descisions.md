# Inglenook Shunting Puzzle — Solver Design Decisions

This document records the key design decisions made before implementing the Python BFS solver. Each entry defines the question, the decision taken, and the rationale.

---

## Decision 1: Locomotive position encoding

**Question:** How should the locomotive's position be represented in the state?

**Options considered:**
- **Option A:** Store the loco as an explicit token `'L'` inside the track tuple, e.g. `('L', 'A', 'B')`. Position is implicit in tuple order.
- **Option B:** Store only wagon labels in each track tuple, with a separate `loco_track` field indicating which track the loco is on.

**Decision:** Option B — wagon tuples contain only wagon labels; loco position is a separate field.

**Rationale:** Keeps wagon tuples homogeneous. No special-casing of `'L'` tokens in capacity checks or move generation. The loco's track is always unambiguous.

---

## Decision 2: Loco position is always the headshunt after every move

**Question:** Does `loco_track` need to be stored as part of the state?

**Context:** The puzzle uses Convention B move counting, where a move is either a Pull or a Push. Every move — both Pull and Push — ends with the loco in the headshunt (Track 1). There is no state between moves where the loco is mid-journey or parked in a siding.

**Decision:** `loco_track` is not stored. It is always Track 1 (the headshunt) at every state boundary.

**Rationale:** Since every move terminates with the loco in the headshunt, the loco's track carries no information at state boundaries. Dropping it simplifies the state shape and hashing.

---

## Decision 3: State representation

**Question:** What is the canonical state shape?

**Decision:** The state is a tuple of four tuples, one per track:

```
(track1_wagons, track2_wagons, track3_wagons, track4_wagons)
```

Where:
- `track1_wagons` — headshunt wagon contents (0–3 wagons; loco is implicit at index 0 but not stored)
- `track2_wagons` — siding 2 contents (0–5 wagons)
- `track3_wagons` — siding 3 contents (0–3 wagons)
- `track4_wagons` — siding 4 contents (0–3 wagons)

Each inner tuple contains wagon labels as strings (e.g. `'A'`, `'B'`). The outer tuple is hashable and suitable for use in the BFS visited set.

---

## Decision 4: Track tuple orientation — index 0 is the open (headshunt-facing) end

**Question:** Which end of a track tuple represents the end accessible to the locomotive?

**Decision:** Index 0 is always the **open end** — the end closest to the headshunt, where wagons are coupled and uncoupled.

**Rationale:** Consistent across all four tracks. For sidings, index 0 is the mouth of the siding. For the headshunt, index 0 is the loco end (though the loco itself is not stored). The "working end" for pull/push operations on the headshunt is index -1, since that is where the headshunt meets the siding being accessed.

---

## Decision 5: The headshunt is a transit buffer, not a deposit location

**Question:** Can the loco decouple wagons in the headshunt?

**Decision:** No. The loco can never decouple wagons in the headshunt. Wagons may only be deposited (decoupled) in sidings (Tracks 2–4).

**Constraints that follow:**
- At the start of the puzzle, only the loco is in the headshunt. Track 1 wagons = `()`.
- The loco may pull wagons into the headshunt and hold them there between moves, but must push them into a siding before they can be considered deposited.
- Wagons in the headshunt are "in transit" and form part of the live state.

---

## Decision 6: Move definitions — Pull and Push

**Question:** What constitutes a legal move, and what state transformation does each perform?

**Decision:** There are exactly two move types:

### Pull(siding, n)
The loco reverses into a siding, couples to `n` wagons at the open end, and draws them out onto the headshunt.

- **Legality:** `n >= 1`, siding has `>= n` wagons, headshunt currently has `<= (3 - n)` wagons.
- **State transformation:** Remove `n` wagons from index 0 of the siding tuple; append them (in order) to the end (index -1) of the headshunt tuple.

**Example:**
```
Headshunt: ('A', 'B'),  Track 3: ('C', 'D', 'E')
Pull(3, 1)
Headshunt: ('A', 'B', 'C'),  Track 3: ('D', 'E')
```

### Push(siding, n)
The loco propels `n` wagons from the headshunt into a siding.

- **Legality:** `n >= 1`, headshunt has `>= n` wagons, siding has `<= (capacity - n)` free slots.
- **State transformation:** Remove `n` wagons from the end (index -1) of the headshunt tuple; prepend them (in order) to index 0 of the siding tuple.

**Example:**
```
Headshunt: ('A', 'B', 'C'),  Track 2: ()
Push(2, 2)
Headshunt: ('A',),  Track 2: ('B', 'C')
```

---

## Decision 7: Headshunt and siding interaction — partial pulls and pushes are independent moves

**Question:** Must all wagons in the headshunt be pushed into a siding before further pulls are performed?

**Decision:** No. Pulls and pushes may be freely interleaved. Each Pull or Push is an independent move regardless of the current headshunt contents, subject only to capacity constraints.

**Constraints that follow:**
- A Pull is legal as long as `len(headshunt) + n <= 3`.
- A Push is legal as long as `len(headshunt) >= n` and the target siding has sufficient free capacity.
- The order of wagons in the headshunt is never altered — pulls append to the end, pushes remove from the end.

**Example sequence:**
```
Headshunt: ('A',),  Track 3: ('B', 'C', 'D')
Pull(3, 2)  →  Headshunt: ('A', 'B', 'C'),  Track 3: ('D',)   [legal: 1 + 2 = 3]
Push(2, 1)  →  Headshunt: ('A', 'B'),        Track 2: ('C',)
Pull(4, 1)  →  Headshunt: ('A', 'B', 'E'),   Track 4: ()       [legal: 2 + 1 = 3]
```

---

## Track capacities (reference)

| Track | Role       | Wagon capacity | Notes                        |
|-------|------------|----------------|------------------------------|
| 1     | Headshunt  | 3              | Loco always present but not counted |
| 2     | Siding     | 5              | Target assembly track        |
| 3     | Siding     | 3              |                              |
| 4     | Siding     | 3              |                              |

---

## Decision 8: Goal state definition

**Question:** What constitutes a solved puzzle state?

**Decision:** The puzzle is solved when all of the following hold:

- `track2_wagons == target` — Track 2 contains exactly the 5 target wagons in the correct order (exact tuple match)
- `track1_wagons == ()` — the headshunt is empty (loco has no wagons coupled)
- `track3_wagons` and `track4_wagons` are unconstrained

**Target tuple convention:** The target is specified from the open end inward, i.e. index 0 is the wagon at the mouth of Track 2 — the first one the loco would pull out. This is consistent with the index 0 = open end convention used throughout.

**Example:**
```python
target = ('C', 'A', 'E', 'B', 'D')

def is_goal(state, target):
    track1, track2, track3, track4 = state
    return track1 == () and track2 == target
```

**Rationale:** Requiring an empty headshunt gives a clean, unambiguous terminal condition — the loco is parked with nothing coupled, the train is fully assembled in Track 2. Tracks 3 and 4 are unconstrained because the puzzle only specifies the assembled train, not the disposition of remaining wagons.
