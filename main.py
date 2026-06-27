from datetime import time
from pawpal_system import (
    Owner,
    Pet,
    Task,
    Scheduler,
)


owner = Owner(name="Riasat", available_time=120)  # 2 hours available


biscuit = Pet(
    name="Biscuit",
    species="Dog",
    breed="Golden Retriever",
    energy_level="high"
)

mochi = Pet(
    name="Mochi",
    species="Cat",
    breed="Siamese",
    energy_level="medium"
)

owner.add_pet(biscuit)
owner.add_pet(mochi)


biscuit.add_task(Task(
    name="Morning Walk",
    duration=30,
    priority=3,
    recurrence="daily",
    time_window="morning"
))

biscuit.add_task(Task(
    name="Feeding",
    duration=10,
    priority=5,
    recurrence="daily"
))

mochi.add_task(Task(
    name="Playtime",
    duration=20,
    priority=2,
    recurrence="daily",
    time_window="afternoon"
))


scheduler = Scheduler(
    owner=owner,
    start_time=time(8, 0),   # 8:00 AM
    end_time=time(12, 0)     # Noon
)


schedule = scheduler.generate_plan()

print("\n=== TODAY'S SCHEDULE ===")
print(schedule.to_readable_format())

print("\nSummary:", schedule.summarize())

print("\nExplanation:")
print(scheduler.explain_choices())

