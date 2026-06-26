# Text Adventure Engine

Build a playable text adventure where the engine underneath is a general-purpose state machine you could lift out and reuse for anything — including graph state later.

**The game is the disguise. The `StateMachine` class is the deliverable.**

---

## Core Mental Model

A state machine is four things:

| Concept | In this game |
|---|---|
| States | Rooms |
| Events | Player commands (`go south`, etc.) |
| Transition table | `(state, event) → next_state` |
| Guards | Conditions that must be true for a transition to fire |

That's it. Everything else is decoration.

### World Map

```
[Hall] --South--> [Study] --East (key required)--> [Vault]
         <--North--
```

---

## Data Model

Three things in memory. Don't over-design:

**World** (static, loaded once from `world.json`)
```json
{
  "Hall":  { "desc": "...", "list": ["key"], "exits": {"South": "Study"} },
  "Study": { "desc": "...", "list": [],      "exits": {"North": "Hall", "East": "Vault"} },
  "Vault": { "desc": "...", "list": [],      "exits": {} }
}
```

**Player state** (mutable): `current_room` (string) + `inventory` (list). Two fields.

**The machine**: transition logic that takes `(current_state, event) → new_state` and checks guards along the way.

**The discipline that matters**: world is data, machine is logic — they never bleed into each other. The machine has no `if room == "study"` hardcoded anywhere. It reads the transition table. This separation is the thing being practiced here — it's the same separation that makes graph state and hexagonal architecture work later.

---

## API

`StateMachine` knows nothing about adventures. It is fully generic:

```python
class InvalidTransition(Exception):
    pass

class StateMachine:
    def __init__(self, transitions, states, guards=None):
        # transitions: {(state, event): target_state}
        # states:      dict of state data (rooms, loaded from world.json)
        # guards:      {(state, event): callable(context) -> bool}

    def available_events(self, state) -> dict:
        # Returns legal exits from this state (queries the transition table)

    def transition(self, state, event, context):
        # 1. Is (state, event) in the table? If not -> InvalidTransition
        # 2. Is there a guard? If so, call it with context
        # 3. Guard returns False -> InvalidTransition
        # 4. Return the target state (pure: no side effects, no mutation)
```

`transition()` is **pure**: state in, state out, no side effects. The game loop handles all mutation (updating `current_room`, modifying inventory). A pure transition function is what makes time-travel and event replay possible later.

---

## Project Structure

```
Text_Adventure_Engine/
├── state_machine.py   # The deliverable — generic StateMachine + InvalidTransition
├── player_state.py    # Thin game loop: holds world + player state, calls the machine
├── world.json         # World definition (rooms, items, exits)
├── test_machine.py    # Unit tests for the machine (independent of the game)
└── README.md
```

---

## Playing the Game

```bash
python player_state.py
```

| Command | Description |
|---|---|
| `go <Direction>` | Move between rooms (e.g. `go South`) |
| `take key` | Pick up the key from the current room |
| `check` | Show inventory and current room |

**Win condition**: reach the Vault. The East door from Study is guarded — you need the key.

---

## Build Milestones

**Day 1 AM — The machine alone**
Write `StateMachine` and `InvalidTransition`. No game yet. Write `test_machine.py` asserting: valid transitions return the right state, illegal events raise, guard failures raise. Get this green before touching the game. This is the part not to skip — it's the actual learning.

**Day 1 PM — The dumb game**
Hardcode three rooms. Write the input loop. Wire `go <direction>` to the machine. No items or guards yet — just walk between rooms.

**Day 2 AM — Items and the guard**
Add `take <item>` and `inventory`. Add the guarded transition (vault door needs the key). Play it: try the door without the key (blocked), grab the key, try again (works).

**Day 2 PM — Load world from file**
Move hardcoded rooms into `world.json` and load them. If the machine still works after the world moves to a file, data and logic were properly separate. If something breaks, there was hidden coupling — find it. That's a real lesson, not busywork.

---

## Moments to Pay Attention To

**When the guard blocks a door you expected to open** — debug it by hand. Is the key actually in the inventory? Did `take key` mutate the right object? That debugging loop is exactly what you'll do inside LangGraph when a conditional edge doesn't route as expected. Feel it now in 30 lines instead of 300.

**When moving the world to JSON breaks something** — that break shows where the machine secretly knew about adventures. Fix it so the machine is pure. This is the hexagonal instinct forming early.

**When listing `available_events(state)`** — notice you're querying the transition table, not asking the rooms. The machine is the single source of truth about what's legal.

---

## Done Criteria

- [ ] `StateMachine` has zero references to rooms, doors, or keys — fully generic
- [ ] Tests pass and cover valid moves, invalid moves, and guard failures
- [ ] The game loads its world from `world.json`
- [ ] You can explain out loud: *why does `transition()` return a new state instead of mutating one?*

The answer to that last one: **it returns instead of mutates, so you could replay a list of events and reconstruct any past state**. That's the property that makes time-travel and graph state debugging possible later.
