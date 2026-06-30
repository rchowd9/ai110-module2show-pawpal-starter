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

python -m pytest
====================== test session starts =======================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Home\Downloads\pawpal\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 5 items                                                 

tests\test_pawpal.py ::test_sorting_correctness_happy_path PASSED           [ 20%]
tests\test_pawpal.py ::test_sorting_anytime_tasks_sink_to_bottom PASSED     [ 40%]
tests\test_pawpal.py ::test_recurrence_logic_generation PASSED              [ 60%]
tests\test_pawpal.py ::test_conflict_detection_flags_duplicate_slots PASSED [ 80%]
tests\test_pawpal.py ::test_scheduler_robustness_empty_states PASSED        [100%]

======================= 5 passed in 0.14s ========================

### 🧪 Automated Test Suite

We use `pytest` to make sure our scheduling logic behaves exactly how it should and to prevent any breaking changes as the system evolves. 

#### How to Run the Tests

To run the full suite from your project root directory, open your terminal and type:

```powershell
python -m pytest

#### What These Tests Cover

The suite focuses on verifying real-world scenarios along with tricky edge cases to ensure the scheduling engine stays reliable:

* **Chronological Sorting:** Confirms that when you pass in multiple tasks scattered completely out of order, the scheduler correctly organizes them from earliest to latest based on their 24-hour clock times.

* **Handling Anytime Tasks:** Validates that tasks without a specific preferred time anchor drop safely to the bottom of the schedule so they never accidentally bump a time-sensitive task.

* **Dynamic Recurrence:** Checks that when a daily or weekly routine item is completed, the system toggles its status correctly and immediately spawns an identical task pushed forward by the right amount of time.

* **Conflict Alerts:** Ensures that if two tasks share the exact same time slot or overlap, a human-readable warning is generated without crashing the app.

* **Empty States:** Tests the engine's resilience when a household profile has zero active tasks to verify that the code handles empty lists gracefully instead of throwing index or attribute errors.

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
