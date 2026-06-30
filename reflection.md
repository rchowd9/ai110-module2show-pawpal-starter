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

* **What constraints does your scheduler consider?**
    Our enhanced scheduler evaluates a multi-layered set of explicit constraints:
    1.  **Total Time Budget:** The absolute physical limit on care hours available, defined by `Owner.available_time`.
    2.  **Hard Clock-Time Anchors:** Exact timing requirements via `Task.preferred_time` (e.g., critical medications or rigid appointments).
    3.  **Loose Time Windows:** Coarser operational blocks defined by `TIME_WINDOWS` (e.g., "morning", "afternoon") ensuring tasks fit broad daily routines.
    4.  **Task Priority Metrics:** Relative task importance scaled 1 (lowest) through 5 (highest).

* **How did you decide which constraints mattered most?**
    We established a strict operational hierarchy: **Hard Chronological Availability > Task Urgency/Priority**. 
    Physical availability is an unyielding constraint—an owner cannot physically execute a task if their time budget or the operational window has passed. Once a timeline window is validated, the engine relies on the task's `priority` metric (e.g., medical or feeding needs scoring a 5) to sort and secure slots before allocating remaining capacity to flexible tasks like "Brush Fur" (priority 2).



**b. Tradeoffs**

* **Describe one tradeoff your scheduler makes.**
    Our lightweight conflict detection system (`Scheduler.check_conflicts()`) prioritizes performance efficiency over exhaustive timeline scanning. It handles conflict auditing by sorting tasks chronologically and performing an $O(N)$ sequential interval pass to check if a subsequent task begins before an immediately preceding task concludes (`start_2 < end_1`). 
    
    The tradeoff is that it only catches overlaps between **immediately adjacent sequential entries** in the sorted queue. If a very long-running task (e.g., a 60-minute "Vet Visit" at 08:00) spans across multiple shorter, back-to-back tasks (e.g., a 5-minute "Meds" dose at 08:15 and a "Feeding" at 08:30), the adjacent comparison strategy will flag the first collision but may not map trailing multi-layered overlaps.

* **Why is that tradeoff reasonable for this scenario?**
    This tradeoff is highly reasonable for a day-to-day pet routine planner for several reasons:
    1.  **Algorithmic Performance:** It avoids complex, resource-heavy nested look-ahead sweeps ($O(N^2)$ loops) or interval trees, keeping the codebase clean, highly readable, and performant.
    2.  **User UI Feedback:** For a standard pet owner profile, alerting them to the *initial* structural breakdown or overlap in their schedule block is sufficient to prompt a calendar adjustment.
    3.  **Domain Specifics:** Most pet-care micro-tasks (feeding, quick breaks, giving medication) are short-duration events. Long, sprawling tasks that engulf multiple blocks are exceptions rather than the rule, making sequential checking incredibly reliable for standard use cases.

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
