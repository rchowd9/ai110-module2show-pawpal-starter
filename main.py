from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    print("=== PAWPAL COMPONENT AND LOGIC VERIFICATION ===\n")

    owner = Owner(name="Riasat", available_time=120)

    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", energy_level="high")
    mochi = Pet(name="Mochi", species="Cat", breed="Siamese", energy_level="medium")

    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # 1. Add tasks out of chronological order to verify sort_by_time
    biscuit.add_task(Task("Evening Walk", duration=30, priority=3, recurrence="daily", time_window="evening", preferred_time="18:30"))
    biscuit.add_task(Task("Morning Feeding", duration=15, priority=5, recurrence="daily", time_window="morning", preferred_time="08:00"))
    biscuit.add_task(Task("Brush Fur", duration=10, priority=2, recurrence="once", time_window=None, preferred_time=None))
    
    # 2. Add an overlapping task at 08:00 AM to trigger the conflict detector explicitly
    mochi.add_task(Task("Insulin Injection", duration=10, priority=5, recurrence="daily", time_window="morning", preferred_time="08:00"))
    mochi.add_task(Task("Afternoon Playtime", duration=20, priority=2, recurrence="daily", time_window="afternoon", preferred_time="14:00"))

    all_tasks = owner.get_all_tasks()
    scheduler = Scheduler(owner=owner, start_time=time(8, 0), end_time=time(20, 0))

    # --- VERIFICATION 1: Raw Ingestion Order ---
    print("--- 1. Raw Ingestion Order ---")
    for t in all_tasks:
        print(f"  [{t.pet_name}] {t.preferred_time if t.preferred_time else 'Anytime'} - {t.name} (Completed: {t.completed})")

    # --- VERIFICATION 2: Chronological Sort ---
    print("\n--- 2. Chronological Sorting Results ---")
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    for t in sorted_tasks:
        print(f"  [{t.pet_name}] {t.preferred_time if t.preferred_time else 'Anytime'} - {t.name}")

    # --- VERIFICATION 3: Dynamic Filters ---
    print("\n--- 3. Filtered Isolation: Mochi's Routine Only ---")
    mochi_only = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
    for t in mochi_only:
        print(f"  [{t.pet_name}] {t.name}")

    # --- VERIFICATION 4: Conflict Warning Engine ---
    print("\n--- 4. Active Conflict Analysis ---")
    conflicts = scheduler.check_conflicts(all_tasks)
    for warning in conflicts:
        print(warning)

    # --- VERIFICATION 5: Automated Recurrence Generation ---
    print("\n--- 5. Automated Recurrence Automation ---")
    feeding_task = all_tasks[1] # Biscuit's Morning Feeding
    print(f"  Current Occurrence -> Date: {feeding_task.due_date} | Done: {feeding_task.completed}")
    
    # Complete task and extract follow-up
    next_occurrence = feeding_task.mark_complete()
    print(f"  Current Occurrence After -> Done: {feeding_task.completed}")
    if next_occurrence:
        print(f"  🚀 Next Instance Spawned -> Date: {next_occurrence.due_date} (Tomorrow) | Done: {next_occurrence.completed}")

if __name__ == "__main__":
    main()