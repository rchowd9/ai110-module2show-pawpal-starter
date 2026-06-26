"""PawPal+ — a pet care scheduling system.

Class skeleton generated from the UML design:
    Owner, Pet, Task  -> dataclasses (data-holding objects)
    Scheduler         -> behavior-heavy planner
    Schedule          -> dataclass holding the generated plan
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from typing import Optional


@dataclass
class Task:
    """A single care activity for a pet (e.g. a walk, feeding, medication)."""

    name: str
    duration: int                      # minutes
    priority: int                      # higher value = more important
    recurrence: str                    # e.g. "daily", "weekly", "once"
    time_window: Optional[str] = None  # e.g. "morning", or a (start, end) range
    notes: str = ""

    def is_due_today(self) -> bool:
        """Return True if this task should be scheduled today."""
        raise NotImplementedError

    def fits_time_window(self, start: time, end: time) -> bool:
        """Return True if this task can run within the given time range."""
        raise NotImplementedError

    def describe(self) -> str:
        """Return a human-readable summary of the task."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet owned by an Owner, with its own list of care tasks."""

    name: str
    species: str
    breed: str
    energy_level: str                       # e.g. "low", "medium", "high"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a new task to this pet."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        raise NotImplementedError

    def get_daily_tasks(self) -> list[Task]:
        """Return the tasks that are due today for this pet."""
        raise NotImplementedError


@dataclass
class Owner:
    """The person responsible for one or more pets."""

    name: str
    available_time: int                     # minutes available today
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def update_availability(self, available_time: int) -> None:
        """Update how much time the owner has available."""
        raise NotImplementedError

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        raise NotImplementedError

    def get_constraints(self) -> dict:
        """Return the scheduling constraints derived from this owner."""
        raise NotImplementedError


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
        """Add a scheduled entry to the plan."""
        raise NotImplementedError

    def to_readable_format(self) -> str:
        """Return a human-readable rendering of the schedule."""
        raise NotImplementedError

    def summarize(self) -> str:
        """Return a short summary (time used, tasks done vs. skipped)."""
        raise NotImplementedError


class Scheduler:
    """Builds a Schedule from an owner's pets, tasks, and constraints."""

    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        tasks: list[Task],
        start_time: time,
        end_time: time,
    ) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks
        self.start_time = start_time
        self.end_time = end_time

    def sort_tasks(self) -> list[Task]:
        """Order tasks (e.g. by priority, then duration)."""
        raise NotImplementedError

    def filter_tasks_by_time(self) -> list[Task]:
        """Keep only tasks that fit within the scheduling window."""
        raise NotImplementedError

    def assign_time_slots(self) -> list[ScheduleEntry]:
        """Place tasks into concrete time slots."""
        raise NotImplementedError

    def generate_plan(self) -> Schedule:
        """Run the full pipeline and return a completed Schedule."""
        raise NotImplementedError

    def explain_choices(self) -> str:
        """Explain why tasks were scheduled, ordered, or skipped."""
        raise NotImplementedError
