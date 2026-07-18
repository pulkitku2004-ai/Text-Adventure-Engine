# Text Adventure Engine

A tiny playable text adventure powered by a generic, reusable `StateMachine`.

The game is a wrapper — the finite-state machine underneath is the actual deliverable, designed to be lifted out and reused for any state/transition/guard problem (workflow engines, graph state, etc.).

## Table of Contents

- [Overview](#overview)
- [World Map](#world-map)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [How to Play](#how-to-play)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
- [Roadmap](#roadmap)

## Overview

A state machine boils down to four ideas, mapped here onto a small adventure game:

| Concept | In this game |
|---|---|
| States | Rooms |
| Events | Player commands (`go south`, etc.) |
| Transition table | `(state, event) → next_state` |
| Guards | Conditions that must hold for a transition to fire |

The core design principle: **the world is data, the machine is logic, and the two never bleed into each other.** `StateMachine` has no hardcoded knowledge of rooms, doors, or keys — it only reads the transition table and world data it's given.

## World Map

```
[Hall] --South--> [Study] --East (key required)--> [Vault]
         <--North--
```

## Project Structure

```
.
├── state_machine.py   # The deliverable: generic StateMachine + InvalidTransition
├── player_state.py    # Game loop: holds world + player state, drives the machine
├── world.json         # World definition (rooms, items, exits)
├── test_machine.py     # Unit tests for the machine
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone <repository-url>
cd Text_Adventure_Engine
```

No external dependencies — the project only uses the Python standard library.

## How to Play

```bash
python player_state.py
```

| Command | Description |
|---|---|
| `go <direction>` | Move between rooms, e.g. `go South` |
| `take key` | Pick up the key from the current room |
| `check` | Show your inventory and current room |

**Win condition:** reach the Vault. The `East` exit from the Study is guarded — you need the key in your inventory first.

## How It Works

**World** — static data, loaded once from `world.json`:

```json
{
  "Hall":  { "desc": "...", "list": ["key"], "exits": { "South": "Study" } },
  "Study": { "desc": "...", "list": [],      "exits": { "North": "Hall", "East": "Vault" } },
  "Vault": { "desc": "...", "list": [],      "exits": {} }
}
```

**Player state** — mutable, held by the game loop: `current_room` (string) and `inventory` (list).

**The machine** — pure transition logic: `(current_state, event) → new_state`, checking guards along the way. `transition()` has no side effects; it never mutates player state directly. That purity is what would make event replay or time-travel debugging possible on top of this engine later.

## API Reference

`StateMachine` is fully generic — it has zero knowledge of adventures, rooms, or keys.

```python
class InvalidTransition(Exception):
    pass

class StateMachine:
    def __init__(self, transitions, states, guards=None):
        # transitions: {(state, event): target_state}
        # states:      dict of state data (rooms, loaded from world.json)
        # guards:      {(state, event): callable(context) -> bool}

    def available_events(self, state) -> dict:
        # Returns the legal exits from this state

    def transition(self, state, event, context):
        # 1. Is (state, event) in the transition table? If not -> InvalidTransition
        # 2. Is there a guard for (state, event)? If so, call it with context
        # 3. Guard returns False -> InvalidTransition
        # 4. Otherwise return the target state (pure: no side effects, no mutation)
```

## Roadmap

- [ ] Fill in `test_machine.py`: cover valid transitions, invalid events, and guard failures
- [ ] Support multi-item guards and combinable conditions
- [ ] Add a save/load mechanism for player state
