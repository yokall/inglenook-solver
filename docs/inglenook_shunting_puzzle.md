# Inglenook Shunting Puzzle — Constraints Document

## 1. Overview

The **Inglenook Shunting Puzzle** is a classic model railway shunting puzzle invented by Alan Wright and named after his layout "Inglenook Sidings". The operator uses a locomotive to move wagons between a set of sidings until a specific five-wagon train is assembled in a required order.

There is no timetable, no destination, and no scenery objective. The sole goal is to sort wagons into a target sequence.

---

## 2. Terminology

| Term | Meaning |
|---|---|
| **Headshunt** | A short length of track at the entrance to a group of sidings. The locomotive uses it as a working space — it can sit here, run back and forth, and access each siding from it. |
| **Siding** | A dead-end track branching off the headshunt, closed at the far end by a buffer stop. |
| **Buffer stop** | The fixed barrier at the closed end of a siding. Wagons cannot pass it. |
| **Wagon** | An unpowered rail vehicle that is pushed or pulled by the locomotive. |
| **Locomotive (Loco)** | The powered vehicle that moves all wagons. It is always at the headshunt end of whatever track it is working. |
| **Train** | A group of wagons currently coupled together and being moved by the loco as a single unit. |
| **Shunting** | The process of moving individual wagons around the sidings to achieve a desired arrangement. |

---

## 3. The Physical Layout

### 3.1 Track Structure

The layout has **four tracks** numbered 1 to 4:

```
                    [  Track 2 — Siding  ·  ·  ·  ·  ·  ]
                   /
[ Track 1  ]------+--[  Track 3 — Siding  ·  ·  ·  ]
  Headshunt        \
                    [  Track 4 — Siding  ·  ·  ·  ]
```

- **Track 1 — Headshunt**: The working track. The loco lives here and uses it to access all three sidings. It also connects to the rest of the railway (the "outside world") at its far end away from the sidings.
- **Track 2 — Siding**: The largest siding. Holds up to **5 wagons**. This is where the completed target train will be assembled.
- **Track 3 — Siding**: Holds up to **3 wagons**.
- **Track 4 — Siding**: Holds up to **3 wagons**.

### 3.2 Capacities

| Track | Type | Max wagons |
|---|---|---|
| Track 1 | Headshunt | **3 wagons** (plus the loco, which does not occupy a wagon slot) |
| Track 2 | Siding | **5 wagons** |
| Track 3 | Siding | **3 wagons** |
| Track 4 | Siding | **3 wagons** |
| **Total** | | **14 wagon slots** |

> **Important**: The headshunt holds a maximum of **3 wagons** at any one time, in addition to the loco. This is a genuine operational constraint — the loco cannot park more than 3 wagons on the headshunt.

### 3.3 Access Rules

- All three sidings are **dead-ends**. Wagons can only enter or exit from the open end, which faces the headshunt.
- The loco **always approaches a siding from the headshunt end**. There is no other way in.
- The loco is permanently at the headshunt end of any wagons it pushes into a siding. It **cannot get to the other end of a group of wagons** without first moving them out of the way.

---

## 4. Wagons and Identifiers

- There are **8 wagons** in total, labelled **A, B, C, D, E, F, G, H**.
- The locomotive is labelled **L**.
- At the start of the full puzzle, all 8 wagons are distributed across Tracks 2, 3 and 4.
- To ease learning, the puzzle can be played with fewer wagons (e.g. 5 or 6) before progressing to the full 8-wagon version.

### 4.1 Starting Position

- The loco (L) starts on **Track 1 (the headshunt)**, with no wagons attached to it.
- The 8 wagons are distributed across Tracks 2, 3 and 4, within each track's capacity limits.
- The starting distribution is either set manually (for learning/setup) or generated at random (for normal play).

---

## 5. The Goal

The puzzle is solved when **5 specific wagons** are assembled on **Track 2**, arranged in a specific target order, with the correct wagon at the open (headshunt) end ready to be drawn out.

### 5.1 Why Track 2?

The headshunt (Track 1) holds only 3 wagons — it cannot accommodate the required 5-wagon train. Track 2, with its 5-wagon capacity, is the only track that can hold the complete target train. The solution train sits in Track 2, ready to be pulled out onto the main line by the loco.

### 5.2 Target Order

- A target sequence of 5 wagons is defined, for example: **C — F — A — H — D**
- The **first wagon** in the sequence must sit at the **open end** of Track 2 (nearest the headshunt), because that is the wagon the loco will couple to and lead out first.
- The **fifth wagon** will be at the **buffer stop end** of Track 2.

```
Track 2:  [ headshunt end / open end → · C · F · A · H · D · buffer stop ]

Loco couples at open end and pulls out:  L — C — F — A — H — D  ✓
```

---

## 6. Movement Rules

### 6.1 What the Loco Can Do

On each move, the loco performs one of two operations:

**Pull** — The loco reverses up to the open end of a siding, couples to the wagon(s) there, and draws them out onto the headshunt.

**Push** — The loco takes wagon(s) from the headshunt and propels them into a siding.

Those are the only two operations. The puzzle is solved entirely through combinations of pulls and pushes.

### 6.2 Coupling — Plain Language

Picture the wagons in a siding as objects stacked in a narrow corridor with only one doorway at one end. You can only interact with the item closest to the doorway. To reach an item further back, you must first remove everything in front of it.

More precisely:

- **Wagons in a siding form a fixed chain.** Every wagon is coupled to the one behind it, all the way back to the buffer stop. They cannot spread apart or reorder themselves while in the siding.
- **When the loco backs into a siding**, it couples to the wagon at the open end. It is now connected to that wagon, which is connected to the next, and so on — the loco is attached to all the wagons in the siding simultaneously.
- **The loco can pull out any number of wagons** from 1 up to however many are in the siding, but they must be taken from the open end and they must come out as a continuous, unbroken group. You cannot skip a wagon or choose one from the middle.
- **The loco can push any number of wagons into a siding**, up to the siding's remaining free capacity. They enter as a continuous group from the open end and push the existing wagons further towards the buffer stop.
- **You cannot insert a wagon between two wagons that are already in a siding.** New wagons always join at the open end.

### 6.3 "Splitting" — What It Means and Why It Is Impossible

**Splitting** would mean separating a group of wagons at a point in the middle — for example, removing wagon 1 from a siding while leaving wagons 2 and 3, even though wagon 1 is not at the open end.

This is **physically impossible** on a dead-end siding. All wagons are coupled in a chain, and the only accessible end is the open end. You cannot reach past the front wagons to grab one behind them.

**The only way to access a wagon that is not at the open end of a siding is to first remove all the wagons in front of it.** This is the core constraint that makes the puzzle challenging.

### 6.4 The Headshunt Capacity Constraint in Practice

The headshunt holds a maximum of **3 wagons** in addition to the loco. This has direct consequences during play:

- If the loco already has 3 wagons sitting on the headshunt, it **cannot pull any more out of a siding** until it has first pushed some of those wagons into a siding to free up space.
- When the loco pushes wagons into a siding, the wagon at the **far end from the loco** (the leading wagon of the train) enters the siding first and ends up deepest inside it.

---

## 7. Ordering and Reversal

Because the loco is always at the headshunt end, and all sidings are dead-ends, **the order of wagons reverses every time they pass through a siding**.

- Wagons **pulled out** of a siding emerge in the **reverse of the order they went in**. The last wagon pushed in is the first to come out.
- Wagons **pushed into** a siding enter so that the leading wagon (furthest from the loco) goes in deepest.

This reversal effect is the core mechanic that makes the puzzle non-trivial. Getting wagons into the precise order required in Track 2 demands careful planning of which sidings to use as intermediate staging areas and in what sequence.

---

## 8. Move Counting

> **One move = one continuous journey by the locomotive in one direction, stopping when it reaches a buffer stop or the operator chooses to stop.**

This means repositioning the loco counts as a move in its own right.

**Example** — The loco is on the headshunt with no wagons and wants to pull 2 wagons from Track 3:

| Step | What happens | Moves counted |
|---|---|---|
| 1 | Loco reverses into Track 3 and couples to 2 wagons | 1 |
| 2 | Loco pulls the 2 wagons forward out onto the headshunt | 1 |
| **Total** | | **2 moves** |

Every loco journey — including purely repositioning movements — counts as real work. A typical solution takes roughly **30–50 moves**.

---

## 9. Constraints Summary

| Rule | Detail |
|---|---|
| Track 1 (Headshunt) capacity | Max **3 wagons** (loco is additional and does not count) |
| Track 2 (Siding) capacity | Max **5 wagons** |
| Track 3 (Siding) capacity | Max **3 wagons** |
| Track 4 (Siding) capacity | Max **3 wagons** |
| Siding access | Open end only; dead-end; LIFO order |
| Loco position | Always at the headshunt/open end of any track being worked |
| Splitting wagons mid-siding | **Impossible** — physically cannot access non-front wagons |
| Wagon order within siding | Fixed chain; can only add or remove from the open end |
| Win condition | 5 target wagons in correct order in Track 2, first wagon at open end |
| Wagons | 8 total, labelled A–H |
| Locomotive | Labelled L; starts on Track 1 with no wagons |

---
