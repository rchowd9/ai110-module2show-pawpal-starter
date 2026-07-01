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

Features
1. Chronological Time Sorting
Scheduler.sort_by_time() — pawpal_system.py:253
Orders tasks by their concrete preferred_time ("HH:MM") using a composite sort key. Tasks with no set time are pushed to the end via a (preferred_time is None, ...) tuple trick, and ties are broken by priority (highest first). Demonstrated in main.py where out-of-order tasks resolve into 08:00 → 08:00 → 14:00 → 18:30 → Anytime.

2. Priority-Based Sorting
Scheduler.sort_tasks() — pawpal_system.py:227
A separate ranking algorithm using the composite key (-priority, duration): most important tasks first, and among equal priorities the shortest task wins (a greedy "quick wins first" tiebreak). This is what drives the Master Care Queue table in the app.

3. Multi-Criteria Filtering
Scheduler.filter_tasks() — pawpal_system.py:238
Filters a task list by completion status and/or pet name, each optional and independent. None means "don't filter on this axis," so one call powers all the sidebar combinations ("Mochi's pending tasks", "all completed", etc.). Pet matching is case-insensitive. A second filter, filter_tasks_by_time(), keeps only tasks whose named window ("morning", etc.) overlaps the scheduling range.

4. Recurring Task Automation
Task.mark_complete() — pawpal_system.py:73
Completing a recurring task returns a freshly spawned Task for the next occurrence, advancing due_date by +1 day (daily) or +1 week (weekly). once tasks return None. This lets the queue regenerate itself instead of tracking a static list. Task.is_due_today() decides eligibility per recurrence type.

5. Conflict Detection
Scheduler.check_conflicts() — pawpal_system.py:260
Sorts tasks chronologically, then does a single linear pass over adjacent pairs, flagging an overlap whenever the next task's start time falls before the current task's end (start + duration). Returns human-readable warnings — e.g. it catches Biscuit's feeding and Mochi's insulin both booked at 08:00 in main.py.

6. Constraint-Based Day Planning
Scheduler.generate_plan() / assign_time_slots() — pawpal_system.py:305
The full pipeline: retrieve today's tasks → filter by time window → sort by priority → greedily pack into slots. It walks a time cursor from the start of the day, placing each task back-to-back and skipping any that would overrun the day's end time or exceed the owner's available-minutes budget. Skipped tasks are surfaced (not silently dropped) so the owner sees what didn't fit. explain_choices() narrates the logic in plain language.



## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. **Chronological Sorting:** Checks that if you add a bunch of tasks completely out of order, the scheduler correctly sequences them from earliest to latest based on their 24-hour clock times.

2. **Handling Anytime Tasks:** Makes sure that tasks without a specific time attached automatically drop to the bottom of the schedule, so they never accidentally bump a time-sensitive routine.

3. **Dynamic Recurrence:** Verifies that when you mark a daily or weekly task as done, the system toggles its status correctly and immediately spawns a fresh copy advanced to the next due date.

4. **Conflict Alerts:** Ensures that if two tasks overlap or share the exact same time slot, the app flags it with a clear warning instead of crashing.

5. **Empty States:** Tests how the scheduler handles a clean slate. If a pet profile has zero tasks, the engine handles the empty list gracefully instead of throwing a generic index error.



**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

python main.py
=== PAWPAL COMPONENT AND LOGIC VERIFICATION ===

--- 1. Raw Ingestion Order ---
  [Biscuit] 18:30 - Evening Walk (Completed: False)
  [Biscuit] 08:00 - Morning Feeding (Completed: False)
  [Biscuit] Anytime - Brush Fur (Completed: False)
  [Mochi] 08:00 - Insulin Injection (Completed: False)
  [Mochi] 14:00 - Afternoon Playtime (Completed: False)

--- 2. Chronological Sorting Results ---
  [Biscuit] 08:00 - Morning Feeding
  [Mochi] 08:00 - Insulin Injection
  [Mochi] 14:00 - Afternoon Playtime
  [Biscuit] 18:30 - Evening Walk
  [Biscuit] Anytime - Brush Fur

--- 3. Filtered Isolation: Mochi's Routine Only ---
  [Mochi] Insulin Injection
  [Mochi] Afternoon Playtime

--- 4. Active Conflict Analysis ---
⚠️ Conflict Detected: [Biscuit] 'Morning Feeding' (starts 08:00, runs 15m) overlaps with [Mochi] 'Insulin Injection' starting at 08:00.

--- 5. Automated Recurrence Automation ---
  Current Occurrence -> Date: 2026-07-01 | Done: False
  Current Occurrence After -> Done: True
  🚀 Next Instance Spawned -> Date: 2026-07-02 (Tomorrow) | Done:False