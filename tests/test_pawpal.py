"""Basic tests for the PawPal+ system."""

import os
import sys

# Make the project root importable
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from pawpal_system import Pet, Task

def test_mark_complete_changes_status():
    # Changed 'recurring=True' to 'recurrence="daily"' (or whatever type your system expects)
    task = Task(name="Feed", duration=10, priority=5, recurrence="daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True

def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", species="dog", breed="Lab", energy_level="high")
    assert len(pet.tasks) == 0

    # Added the missing 'recurrence' argument here as well
    pet.add_task(Task(name="Walk", duration=30, priority=3, recurrence="none"))

    assert len(pet.tasks) == 1