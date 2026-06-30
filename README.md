# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

=== TODAY'S SCHEDULE ===
Today's plan:
  08:00-08:10  • Biscuit's Feeding (10 min, priority 5, daily)
  08:10-08:40  • Biscuit's Morning Walk (30 min, priority 3, daily) [morning]
  08:40-09:00  • Mochi's Playtime (20 min, priority 2, daily) [afternoon]

Summary: 3 task(s) scheduled using 60 min; 0 skipped.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Task sorting** | `Scheduler.sort_by_time()` | Orders tasks chronologically using an alphabetical lambda key comparison on 24-hour clock strings (`"HH:MM"`). Pushes loose, flexible `"Anytime"` assignments safely to the bottom of the list. |

| **Filtering** | `Scheduler.filter_tasks()` | Employs fast list-comprehensions to dynamically isolate tasks by completion status (pending vs. complete) or a specific pet profile target with case-insensitive boundary matches. |

| **Conflict handling** | `Scheduler.check_conflicts()` | Translates timestamp strings into aggregate minute counters from midnight to evaluate task windows, executing a sequential interval pass to flag overlaps without interrupting the application flow. |

| **Recurring tasks** | `Task.mark_complete()` | Integrates native Python `datetime.timedelta` logic to automatically advance dates by `+1 day` (Daily) or `+1 week` (Weekly) and spawn the next due instance upon task completion. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
