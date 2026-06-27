# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- add a pet
- schedule a walk
- see today's tasks

Owner
Attributes: name, available_time, preferences, pets
Methods: update_availability(), add_pet(), get_constraints()

Pet
Attributes: name, species, breed, energy_level, tasks
Methods: add_task(), remove_task(), get_daily_tasks()

Task
Attributes: name, duration, priority, recurrence, time_window, notes
Methods: is_due_today(), fits_time_window(), describe()

Scheduler
Attributes: owner, pet, tasks, start_time, end_time
Methods: sort_tasks(), filter_tasks_by_time(), assign_time_slots(), generate_plan(), explain_choices()

Schedule
Attributes: entries, total_time_used, skipped_tasks
Methods: add_entry(), to_readable_format(), summarize()

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Here are the key changes I made and why they mattered.

1. I removed duplicated task state from the Scheduler
Originally, the Scheduler accepted a pet and a separate tasks list. My assistant pointed out that this created two sources of truth — tasks lived both on the Pet and inside the Scheduler. That duplication would eventually cause inconsistencies.

What I changed:  
I removed the extra tasks parameter and now derive tasks directly from the pet (or pets) the scheduler is working with.

Why:  
It keeps the system consistent and prevents subtle bugs where one list updates and the other doesn’t.

2. I added a ScheduleEntry class to make time‑slotting explicit
My initial UML didn’t include a dedicated object for a scheduled block of time. The assistant recommended adding one so that each scheduled item could cleanly pair a Task with a start and end time.

What I changed:  
I introduced ScheduleEntry as a dataclass.

Why:  
It makes the schedule easier to build, reason about, and test. It also keeps the Schedule class clean and focused.

3. I strengthened the relationship between tasks and pets
The assistant noted that once tasks are flattened into a schedule, I’d lose track of which pet a task belonged to. That would make readable output confusing (“Walk at 8:00” — for who?).

What I changed:  
I updated ScheduleEntry so it can carry the Task object directly, and I ensured tasks remain tied to their pet through the pet’s task list.

Why:  
It preserves context and makes the final schedule human‑readable.

4. I clarified how time windows will work
My initial design used time_window: Optional[str], but the assistant pointed out that this would force me to hardcode vague strings like "morning" into real time ranges. That would get messy fast.

What I changed:  
I kept the attribute for now, but I documented that I’ll eventually replace it with a structured type (e.g., (start_time, end_time)).

Why:  
It sets me up for cleaner logic when I implement fits_time_window().

5. I acknowledged the need to unify “available time” vs. “time window”
The assistant highlighted a conceptual conflict:

Owner.available_time is a budget in minutes

Scheduler.start_time/end_time is a fixed window

I didn’t fully resolve this yet, but I documented it as a design decision I’ll finalize when implementing the scheduler.

Why:  
It prevents me from writing logic that accidentally contradicts itself.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
