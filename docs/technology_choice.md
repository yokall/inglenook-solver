# Technology Choice

---

## Context

A developer with a background in Perl and backend/API development wishes to build an interactive implementation of the Inglenook Shunting Puzzle. The application requires:

- A top-down visual representation of a headshunt and three sidings
- Interactive coupling and uncoupling of wagons
- A manual play mode and an automated solver that finds the shortest solution
- Simple but functional artwork — visual clarity is preferred over polish
- A learning-oriented project where exploring new technologies is welcomed

Three candidate technologies were evaluated: **Vanilla JavaScript + HTML5 Canvas**, **Python + Pygame**, and **Godot 4**. This record documents the rationale for selecting Python and Pygame.

---

## Decision

**Python 3 with Pygame** has been selected as the implementation technology for this project.

---

## Rationale

### 1. Language familiarity and cognitive fit

Python is the closest mainstream language to Perl in philosophy: expressive, readable, and oriented around getting things done quickly. A developer coming from Perl will find Python's syntax, string handling, and scripting idioms natural from the outset. This reduces the risk of getting stuck on language mechanics rather than puzzle logic — which is the primary learning goal.

JavaScript, by contrast, introduces a runtime model (asynchronous execution, the event loop, closures) that is genuinely unfamiliar to backend Perl developers and would add friction disproportionate to the project's scope. Godot's GDScript is also Python-like, but is only useful inside the Godot engine and teaches no transferable skills.

### 2. Solver algorithm fit

The most technically interesting component of this project is the automated solver — a state-space search (BFS or A\*) that finds the shortest sequence of moves to assemble the target train. Python is exceptionally well-suited to this:

- `collections.deque` provides an efficient queue for BFS out of the box
- `heapq` supports priority queues for A\* with no extra dependencies
- Python tuples are hashable and can be used directly as dictionary keys or in sets, making visited-state tracking trivial
- The standard library's data structures map cleanly onto the puzzle's state representation (wagon positions as tuples, move sequences as lists)

Critically, the solver can be written and tested as a **pure Python script with no UI dependency**, then integrated with Pygame once correct. This separation of concerns is a significant productivity advantage.

### 3. Minimal setup overhead

Getting started with Pygame requires nothing beyond:

```bash
pip install pygame
python puzzle.py
```

There is no editor to install, no project to configure, no build step, and no engine to learn. The edit-run cycle is as fast as any other Python script. This low friction is valuable for a learning project where iteration speed matters.

### 4. Appropriate rendering capability

Pygame's `pygame.draw` module provides everything needed for a clean top-down puzzle view: rectangles for wagons, lines for track, and text for labels. The visual requirements are modest — a functional representation, not a polished game — and Pygame delivers exactly this level of capability without overcomplicating the rendering layer.

A full game engine such as Godot would bring substantial additional concepts (scenes, nodes, signals, the Godot editor) that provide no benefit at this scope and would consume learning energy better spent on the puzzle logic itself.

### 5. Learning value and skill transferability

Python skills acquired during this project are directly applicable to the developer's existing backend and API work. Pygame knowledge, while niche, provides a foundation for understanding event-driven programming and game loops — concepts that transfer to other interactive application development. Neither Godot's GDScript nor a JavaScript/Canvas implementation offers comparable transferability given this developer's context.

---

## Alternatives Considered

| Technology | Reason not selected |
|---|---|
| Vanilla JS + HTML5 Canvas | JavaScript's runtime model is unfamiliar; algorithm code is more verbose; less natural fit for the solver component |
| Godot 4 | Significant engine learning curve (scenes, nodes, editor); overkill for a single-screen puzzle; solver logic harder to develop in isolation |

---

## Consequences

### Positive

- Fast development cycle with no build tooling
- Solver algorithm can be prototyped and tested independently of the UI
- Python's readability makes the codebase easy to revisit and extend
- Low risk of getting blocked on tooling or language issues

### Negative / Accepted trade-offs

- **Shareability:** Running the application requires Python 3 and Pygame to be installed on the target machine. There is no browser-based or standalone executable output without additional packaging (e.g. PyInstaller).
- **Animation:** Pygame has no built-in animation or tweening system. Smooth wagon movement must be implemented manually using delta time — this is straightforward but not automatic.
- **Future scope:** If the project later requires web deployment or significantly richer visuals, porting to JavaScript/Canvas or Godot would be the natural upgrade path. The pure-Python solver logic is portable and would survive such a migration intact.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| Python | ≥ 3.10 | Runtime |
| Pygame | ≥ 2.5 | Windowed display, event loop, 2D drawing |

No other third-party dependencies are required. The solver uses only the Python standard library.