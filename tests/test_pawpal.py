import pytest
from datetime import time, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

# ---------------------------------------------------------
# FIXTURES SETUP
# ---------------------------------------------------------
@pytest.fixture
def empty_scheduler_env():
    """Provides a sterile, initialized environment containing an owner and scheduler."""
    owner = Owner(name="Riasat", available_time=120)
    scheduler = Scheduler(owner=owner, start_time=time(8, 0), end_time=time(20, 0))
    return owner, scheduler


@pytest.fixture
def populated_pet_household(empty_scheduler_env):
    """Provides an environment populated with a multi-pet portfolio."""
    owner, scheduler = empty_scheduler_env
    biscuit = Pet(name="Biscuit", species="Dog", breed="Lab", energy_level="high")
    mochi = Pet(name="Mochi", species="Cat", breed="Siamese", energy_level="medium")
    
    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner, scheduler, biscuit, mochi


# ---------------------------------------------------------
# AUTOMATED TESTING CORE SUITE
# ---------------------------------------------------------

def test_sorting_correctness_happy_path(populated_pet_household):
    """Verify that sorting returns explicit clock tasks in strict chronological order."""
    owner, scheduler, biscuit, _ = populated_pet_household
    
    # Ingest tasks completely out of order
    biscuit.add_task(Task("Evening Walk", duration=30, priority=3, recurrence="daily", preferred_time="18:30"))
    biscuit.add_task(Task("Morning Feeding", duration=15, priority=5, recurrence="daily", preferred_time="08:00"))
    biscuit.add_task(Task("Afternoon Play", duration=20, priority=2, recurrence="daily", preferred_time="14:00"))
    
    all_tasks = owner.get_all_tasks()
    sorted_results = scheduler.sort_by_time(all_tasks)
    
    # Assert correct sequential timeline mapping
    assert len(sorted_results) == 3
    assert sorted_results[0].preferred_time == "08:00"
    assert sorted_results[1].preferred_time == "14:00"
    assert sorted_results[2].preferred_time == "18:30"


def test_sorting_anytime_tasks_sink_to_bottom(populated_pet_household):
    """Verify that tasks lacking precise preferred_times drop to the bottom of the array."""
    owner, scheduler, biscuit, _ = populated_pet_household
    
    biscuit.add_task(Task("Flexible Brush Fur", duration=10, priority=2, recurrence="once", preferred_time=None))
    biscuit.add_task(Task("Rigid Morning Meds", duration=5, priority=5, recurrence="daily", preferred_time="07:45"))
    
    all_tasks = owner.get_all_tasks()
    sorted_results = scheduler.sort_by_time(all_tasks)
    
    assert sorted_results[0].preferred_time == "07:45"
    assert sorted_results[1].preferred_time is None  # Anytime item drops securely to last index


def test_recurrence_logic_generation(populated_pet_household):
    """Confirm that marking a daily item complete spawns a new instance for the next calendar day."""
    _, _, biscuit, _ = populated_pet_household
    
    target_task = Task("Daily Feeding", duration=15, priority=5, recurrence="daily", preferred_time="08:00")
    biscuit.add_task(target_task)
    
    initial_date = target_task.due_date
    
    # Execute state change transition
    follow_up_task = target_task.mark_complete()
    
    assert target_task.completed is True
    assert follow_up_task is not None
    assert follow_up_task.name == "Daily Feeding"
    assert follow_up_task.completed is False
    # Validate datetime calculation delta boundary
    assert follow_up_task.due_date == initial_date + timedelta(days=1)


def test_conflict_detection_flags_duplicate_slots(populated_pet_household):
    """Verify that the engine generates human-readable warnings for overlapping assignments."""
    owner, scheduler, biscuit, mochi = populated_pet_household
    
    # Introduce an explicit timing collision at 08:00 AM
    biscuit.add_task(Task("Morning Walk", duration=30, priority=4, recurrence="daily", preferred_time="08:00"))
    mochi.add_task(Task("Insulin Injection", duration=10, priority=5, recurrence="daily", preferred_time="08:00"))
    
    all_tasks = owner.get_all_tasks()
    warnings = scheduler.check_conflicts(all_tasks)
    
    assert len(warnings) == 1
    assert "⚠️ Conflict Detected" in warnings[0]
    assert "Morning Walk" in warnings[0]
    assert "Insulin Injection" in warnings[0]


def test_scheduler_robustness_empty_states(empty_scheduler_env):
    """Edge Case: Ensure the scheduling module executes flawlessly when handling zero active tasks."""
    _, scheduler = empty_scheduler_env
    
    empty_list = []
    
    # Execute pipelines against empty structures
    sorted_res = scheduler.sort_by_time(empty_list)
    conflicts_res = scheduler.check_conflicts(empty_list)
    
    assert sorted_res == []
    assert conflicts_res == []