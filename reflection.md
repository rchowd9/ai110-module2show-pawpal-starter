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

* I used AI primarily as an architectural sounding board and a test-generation tool. It was incredibly helpful for quickly scaffolded `pytest` frameworks and for figuring out how to neatly pass state through methods without cluttering up class variables.

* The most helpful prompts were specific, isolated questions like: *"How can I design a conflict checking routine that flags matching times without crashing my generation loop?"* and *"What is the cleanest way to make anytime tasks drop to the bottom of a sorted list using Python's built-in sorting keys?"*

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

* There was a distinct moment during the conflict-checking design phase where the AI suggested implementing a heavy interval-tree lookup library to map task overlaps down to the millisecond. 

* I chose not to accept this suggestion because it felt like massive over-engineering for a standard pet-care app. Instead, I pushed back and opted for a straightforward sequential look-ahead loop. I verified this simpler logic by writing targeted edge-case tests with matching times, proving that a light sequential check was more than enough to give owners helpful warning banners in the UI.

---

## 4. Testing and Verification

**a. What you tested**

* **Chronological Sorting Accuracy:** I verified that the scheduler correctly arranges a jumbled mix of morning, afternoon, and evening tasks from earliest to latest based on 24-hour military strings.

* **Loose Boundary Management:** I tested that flexible tasks lacking a specified preferred time (`None`) naturally sink to the bottom of the itinerary instead of breaking the sorter or bumping rigid routines.

* **Automated Recurrence Re-indexing:** I confirmed that checking a daily task as complete toggles its state and successfully spawns a brand new instance advanced exactly `+1 day` into the future.

* **Conflict Flagging:** I tested that identical or overlapping task blocks reliably return human-readable alert strings to flag schedule bottlenecks.

* **Empty Profile Resilience:** I made sure the scheduler doesn't crash, throw index errors, or drop attribute faults when handed an entirely blank slate with zero active tasks.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

* I feel highly confident in the core scheduling engine. The edge cases are fully locked down by the automated test suite, and the logic handles mixed inputs, empty structures, and state changes cleanly.

* If I had more time, the next edge cases I would test involve extreme boundary conditions—like a task whose duration pushes it past midnight into the next day, or handling sudden changes to the owner's available time budget *after* a multi-pet plan has already been generated.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

* I am most satisfied with how naturally the backend logic binds to the Streamlit UI elements. Instead of just printing raw strings, the data streams into organized layout components like `st.table` for the master queue and clean, contextual `st.warning` blocks that pinpoint skipped tasks for the user.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

* In the next iteration, I would completely unify the concept of `Owner.available_time` (the minute budget) with the `Scheduler.start_time` and `end_time` (the physical window). Right now, they run as separate constraints, which can lead to confusing scenarios where an owner has plenty of minutes left in their budget, but can't schedule a task because it falls outside their active daytime window.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

* The biggest thing I learned is that spending an extra hour organizing class relationships and removing duplicate states *before* writing code saves you from massive refactoring headaches later. Keeping the system state driven purely by the `Owner` and `Pet` models made connecting everything to the frontend an absolute breeze.
