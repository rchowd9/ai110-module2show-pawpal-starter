"""PawPal+ — a pet care scheduling system.

Class roles:
    Task      -> a single activity (description, time, frequency, completion)
    Pet       -> pet details + its list of tasks
    Owner     -> manages multiple pets, exposes all their tasks
    Scheduler -> the "brain": retrieves, organizes, and plans tasks across pets
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Optional

# Named parts of the day mapped to (start_hour, end_hour) ranges.
# Used to turn a loose time_window string ("morning") into real times.
TIME_WINDOWS: dict[str, tuple[int, int]] = {
    "morning": (6, 12),
    "afternoon": (12, 17),
    "evening": (17, 21),
    "night": (21, 24),
}


def _add_minutes(t: time, minutes: int) -> time:
    """Return the time that is `minutes` after `t` (clamped within one day)."""
    base = datetime.combine(datetime.min, t) + timedelta(minutes=minutes)
    return base.time()


@dataclass
class Task:
    """A single care activity for a pet (e.g. a walk, feeding, medication)."""

    name: str
    duration: int                      # minutes
    priority: int                      # higher value = more important
    recurrence: str                    # "daily", "weekly", "once"
    time_window: Optional[str] = None  # e.g. "morning"; None = any time
    notes: str = ""
    completed: bool = False            # completion status
    pet_name: str = ""                 # set when attached to a Pet (back-ref)

    def is_due_today(self) -> bool:
        """Return True if this task should be scheduled today.

        - "daily": always due.
        - "weekly": treated as due (simplified — no calendar tracking yet).
        - "once": due only until it has been completed.
        """
        if self.recurrence == "once":
            return not self.completed
        return self.recurrence in ("daily", "weekly")

    def fits_time_window(self, start: time, end: time) -> bool:
        """Return True if this task's preferred window overlaps [start, end].

        A task with no time_window fits any range.
        """
        if not self.time_window:
            return True
        window = TIME_WINDOWS.get(self.time_window.lower())
        if window is None:
            return True  # unknown label -> don't over-constrain
        win_start = time(hour=window[0] % 24)
        win_end = time(hour=window[1] % 24) if window[1] < 24 else time(23, 59)
        # Overlap if the task's window starts before the range ends and vice versa.
        return win_start <= end and win_end >= start

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def describe(self) -> str:
        """Return a human-readable summary of the task."""
        owner = f"{self.pet_name}'s " if self.pet_name else ""
        window = f" [{self.time_window}]" if self.time_window else ""
        status = "✓" if self.completed else "•"
        return (
            f"{status} {owner}{self.name} "
            f"({self.duration} min, priority {self.priority}, {self.recurrence}){window}"
        )


@dataclass
class Pet:
    """A pet owned by an Owner, with its own list of care tasks."""

    name: str
    species: str
    breed: str
    energy_level: str                       # "low", "medium", "high"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a new task to this pet and stamp it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet (by identity, not value)."""
        self.tasks = [t for t in self.tasks if t is not task]

    def get_daily_tasks(self) -> list[Task]:
        """Return the tasks that are due today for this pet."""
        return [t for t in self.tasks if t.is_due_today()]


@dataclass
class Owner:
    """The person responsible for one or more pets."""

    name: str
    available_time: int                     # minutes available today
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def update_availability(self, available_time: int) -> None:
        """Update how much time the owner has available."""
        self.available_time = available_time

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Flat list of every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_daily_tasks(self) -> list[Task]:
        """Flat list of today's due tasks across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.get_daily_tasks()]

    def get_constraints(self) -> dict:
        """Return the scheduling constraints derived from this owner."""
        return {
            "available_time": self.available_time,
            "preferences": dict(self.preferences),
        }


@dataclass
class ScheduleEntry:
    """One scheduled task occupying a concrete time slot."""

    task: Task
    start_time: time
    end_time: time


@dataclass
class Schedule:
    """The generated plan: scheduled entries plus what got skipped."""

    entries: list[ScheduleEntry] = field(default_factory=list)
    total_time_used: int = 0                 # minutes
    skipped_tasks: list[Task] = field(default_factory=list)

    def add_entry(self, entry: ScheduleEntry) -> None:
        """Add a scheduled entry to the plan and track time used."""
        self.entries.append(entry)
        self.total_time_used += entry.task.duration

    def to_readable_format(self) -> str:
        """Return a human-readable rendering of the schedule."""
        if not self.entries and not self.skipped_tasks:
            return "No tasks to schedule today."
        lines = ["Today's plan:"]
        for entry in self.entries:
            start = entry.start_time.strftime("%H:%M")
            end = entry.end_time.strftime("%H:%M")
            lines.append(f"  {start}-{end}  {entry.task.describe()}")
        if self.skipped_tasks:
            lines.append("Skipped:")
            for task in self.skipped_tasks:
                lines.append(f"  {task.describe()}")
        return "\n".join(lines)

    def summarize(self) -> str:
        """Return a short summary (time used, tasks done vs. skipped)."""
        return (
            f"{len(self.entries)} task(s) scheduled using "
            f"{self.total_time_used} min; {len(self.skipped_tasks)} skipped."
        )


class Scheduler:
    """The brain: retrieves, organizes, and plans tasks across all pets."""

    def __init__(
        self,
        owner: Owner,
        start_time: time,
        end_time: time,
    ) -> None:
        """Create a scheduler for an owner within a start/end time window."""
        self.owner = owner
        self.start_time = start_time
        self.end_time = end_time

    def retrieve_tasks(self) -> list[Task]:
        """Pull today's due tasks from every pet the owner has."""
        return self.owner.get_daily_tasks()

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (high first), then shortest duration."""
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def filter_tasks_by_time(self, tasks: list[Task]) -> list[Task]:
        """Keep only tasks whose window overlaps the scheduling range."""
        return [
            t for t in tasks
            if t.fits_time_window(self.start_time, self.end_time)
        ]

    def assign_time_slots(self, tasks: list[Task]) -> Schedule:
        """Pack tasks sequentially within the window and time budget.

        A task is skipped if it would overrun the end time or exceed the
        owner's available minutes.
        """
        schedule = Schedule()
        cursor = self.start_time
        budget = self.owner.available_time

        for task in tasks:
            finish = _add_minutes(cursor, task.duration)
            overruns_window = finish > self.end_time
            over_budget = schedule.total_time_used + task.duration > budget
            if overruns_window or over_budget:
                schedule.skipped_tasks.append(task)
                continue
            schedule.add_entry(ScheduleEntry(task, cursor, finish))
            cursor = finish

        return schedule

    def generate_plan(self) -> Schedule:
        """Run the full pipeline and return a completed Schedule."""
        tasks = self.retrieve_tasks()
        tasks = self.filter_tasks_by_time(tasks)
        tasks = self.sort_tasks(tasks)
        return self.assign_time_slots(tasks)

    def explain_choices(self) -> str:
        """Explain how tasks were ordered and what drove the plan."""
        return (
            "Tasks are pulled from all pets, kept only if their preferred "
            "time window overlaps the day, then ordered by priority (highest "
            "first) and shortest duration. They are packed in order until the "
            f"{self.start_time.strftime('%H:%M')}-"
            f"{self.end_time.strftime('%H:%M')} window or the owner's "
            f"{self.owner.available_time}-minute budget runs out; the rest "
            "are skipped."
        )
