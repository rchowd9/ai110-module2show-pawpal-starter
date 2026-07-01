import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler, Schedule, ScheduleEntry

st.set_page_config(page_title="PawPal+ Care Portal", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Care Assistant")

# ---------------------------------------------------------
# SESSION STATE SETUP
# ---------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

if "pets" not in st.session_state:
    st.session_state.pets = []

owner = st.session_state.owner

# ---------------------------------------------------------
# SIDEBAR CONTROLS & LIVE FILTERS
# ---------------------------------------------------------
st.sidebar.header("🎯 Settings & Filters")

# Edit Owner parameters
owner_name = st.sidebar.text_input("Owner Name", value=owner.name)
owner.name = owner_name

available_mins = st.sidebar.slider("Available Care Minutes Today", min_value=15, max_value=480, value=owner.available_time, step=15)
owner.update_availability(available_mins)

st.sidebar.divider()
st.sidebar.subheader("Filter Live Lists")

# Filter tasks by a specific pet
pet_options = ["All Pets"] + [pet.name for pet in st.session_state.pets]
selected_filter_pet = st.sidebar.selectbox("Show Tasks For:", pet_options)

# Filter tasks by completion status
status_option = st.sidebar.radio("Task Status:", ["All Tasks", "Pending Tasks Only", "Completed Tasks Only"])

# ---------------------------------------------------------
# HOUSEHOLD DATA INGESTION
# ---------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🐕 Household Pets")
    with st.form("pet_form", clear_on_submit=True):
        new_pet_name = st.text_input("Pet Name", value="Mochi")
        species = st.selectbox("Species", ["dog", "cat", "other"])
        submit_pet = st.form_submit_button("Add Pet")
        
        if submit_pet and new_pet_name:
            new_pet = Pet(name=new_pet_name, species=species, breed="Unknown", energy_level="medium")
            st.session_state.pets.append(new_pet)
            owner.add_pet(new_pet)
            st.success(f"Successfully added {new_pet_name} to the family!")
            st.rerun()

    if st.session_state.pets:
        for pet in st.session_state.pets:
            st.markdown(f"- **{pet.name}** ({pet.species.title()})")
    else:
        st.info("No pets added yet.")

with col_right:
    st.subheader("➕ Add Care Activity")
    if st.session_state.pets:
        with st.form("task_form", clear_on_submit=True):
            chosen_pet = st.selectbox("Assign task to:", st.session_state.pets, format_func=lambda p: p.name)
            task_title = st.text_input("Activity Name", value="Evening Walk")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
            with c2:
                priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
            with c3:
                time_window = st.selectbox("Time Window", ["None", "morning", "afternoon", "evening", "night"])

            # Optional concrete start time — enables chronological sorting & conflict detection
            set_time = st.checkbox("Set a specific start time (enables conflict detection)")
            preferred_clock = st.time_input("Preferred start time", time(8, 0), disabled=not set_time)

            submit_task = st.form_submit_button("Save Task")

            if submit_task and task_title:
                priority_map = {"low": 1, "medium": 3, "high": 5}
                window_val = None if time_window == "None" else time_window
                preferred_val = preferred_clock.strftime("%H:%M") if set_time else None

                task = Task(
                    name=task_title,
                    duration=int(duration),
                    priority=priority_map[priority],
                    recurrence="daily",
                    time_window=window_val,
                    preferred_time=preferred_val
                )
                chosen_pet.add_task(task)
                st.success(f"Added '{task_title}' to {chosen_pet.name}'s daily routine!")
                st.rerun()
    else:
        st.info("Please register a pet before adding tasks.")

st.divider()

# ---------------------------------------------------------
# INTERACTIVE QUEUE REVEAL (SORTING & FILTERING METHODS)
# ---------------------------------------------------------
st.subheader("📋 Master Care Queue")

all_tasks = owner.get_all_tasks()

# Instantiate a temporary baseline scheduler to process sorting and filters
base_scheduler = Scheduler(owner=owner, start_time=time(0, 0), end_time=time(23, 59))

# Apply complete/pending parameters based on sidebar choices
filter_done = None
if status_option == "Pending Tasks Only":
    filter_done = False
elif status_option == "Completed Tasks Only":
    filter_done = True

filter_pet_name = None if selected_filter_pet == "All Pets" else selected_filter_pet

# Use your Scheduler's built-in filter method
processed_tasks = base_scheduler.filter_tasks(all_tasks, completed=filter_done, pet_name=filter_pet_name)

if not processed_tasks:
    st.info("No care activities match your current sidebar filters.")
else:
    # Use your Scheduler's built-in sorting method (Priority high-to-low, then shortest duration)
    sorted_tasks = base_scheduler.sort_tasks(processed_tasks)
    
    # Present data cleanly using st.table
    table_rows = []
    for idx, t in enumerate(sorted_tasks):
        table_rows.append({
            "Order Key": idx + 1,
            "Pet Name": t.pet_name,
            "Activity": t.name,
            "Duration": f"{t.duration} mins",
            "Priority Score": f"Level {t.priority}",
            "Target Window": t.time_window if t.time_window else "Flexible / Anytime",
            "Status": "✅ Complete" if t.completed else "⏳ Pending"
        })
    st.table(table_rows)

    # Simple interactive button panel to toggle task completion states
    st.markdown("**Quick Completion Simulator:**")
    button_cols = st.columns(min(len(sorted_tasks), 5))
    for idx, t in enumerate(sorted_tasks):
        btn_col = button_cols[idx % 5]
        if not t.completed:
            if btn_col.button(f"Mark #{idx+1} Done", key=f"complete_btn_{idx}_{t.name}"):
                t.mark_complete()
                st.rerun()

st.divider()

# ---------------------------------------------------------
# DYNAMIC DAY PLAN OPTIMIZATION ENGINE
# ---------------------------------------------------------
st.subheader("📅 Optimized Day-Plan Roadmap")

time_start_col, time_end_col = st.columns(2)
with time_start_col:
    day_start = st.time_input("Start Day At:", time(8, 0))
with time_end_col:
    day_end = st.time_input("End Day At:", time(21, 0))

if st.button("Generate Today's Action Schedule", type="primary"):
    if not st.session_state.pets:
        st.error("You need to register at least one pet to generate a schedule roadmap.")
    else:
        # Build the operational scheduler using owner constraints
        engine = Scheduler(owner=owner, start_time=day_start, end_time=day_end)
        computed_plan = engine.generate_plan()
        
        # Display the summary string
        st.success(computed_plan.summarize())

        # Time-Conflict Detection: flag tasks whose fixed start times overlap
        conflicts = engine.check_conflicts(engine.retrieve_tasks())
        if conflicts:
            st.markdown("#### ⚠️ Time Conflicts Detected")
            for warning in conflicts:
                st.warning(warning)

        # Surfacing Conflict Warnings: Display skipped tasks transparently to the pet owner
        if computed_plan.skipped_tasks:
            st.markdown("#### 🚨 Schedule Bottleneck Warning")
            for skipped in computed_plan.skipped_tasks:
                st.warning(
                    f"⏰ **Could not schedule:** [{skipped.pet_name}] **{skipped.name}** "
                    f"({skipped.duration} mins, Priority {skipped.priority}). "
                    f"This task was skipped because it exceeds your available time budget "
                    f"or falls outside your operational hours.",
                    icon="⏳"
                )
        
        # Display Planned Entries
        st.markdown("### 🗺️ Timeline View")
        if not computed_plan.entries:
            st.info("No tasks could be safely scheduled within your specified hours and time budget.")
        else:
            for entry in computed_plan.entries:
                start_str = entry.start_time.strftime("%H:%M")
                end_str = entry.end_time.strftime("%H:%M")
                st.info(
                    f"🟢 **{start_str} - {end_str}** | "
                    f"**[{entry.task.pet_name}]** {entry.task.name} ({entry.task.duration} mins) "
                    f"— *Priority Rank: {entry.task.priority}*"
                )
        
        # Output Engine Explanatory Analytics
        st.markdown("### 🧠 Logic Explanation")
        st.caption(engine.explain_choices())