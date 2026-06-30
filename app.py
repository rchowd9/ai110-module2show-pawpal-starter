import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler, Schedule, ScheduleEntry

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# ---------------------------------------------------------
# SESSION STATE SETUP
# ---------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

if "pets" not in st.session_state:
    st.session_state.pets = []

owner = st.session_state.owner

# ---------------------------------------------------------
# OWNER INPUTS
# ---------------------------------------------------------

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, breed="Unknown", energy_level="medium")
    st.session_state.pets.append(new_pet)
    owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name}")

if st.session_state.pets:
    st.write("Current pets:")
    for pet in st.session_state.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet.")



st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if st.session_state.pets:
    selected_pet = st.selectbox(
        "Assign task to which pet?",
        st.session_state.pets,
        format_func=lambda p: p.name
    )

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_map = {"low": 1, "medium": 3, "high": 5}
    task = Task(
        name=task_title,
        duration=int(duration),
        priority=priority_map[priority],
        recurrence="daily",
        time_window=None
    )
    selected_pet.add_task(task)
    st.success(f"Added task '{task_title}' to {selected_pet.name}")


if st.session_state.pets:
    if selected_pet.tasks:
        st.write("Current tasks for this pet:")
        for t in selected_pet.tasks:
            st.write(f"- {t.describe()}")
    else:
        st.info("This pet has no tasks yet.")

st.divider()


st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
