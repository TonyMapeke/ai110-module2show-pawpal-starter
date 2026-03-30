import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Streamlit reruns this entire script on every widget change; without session_state,
# a new Owner would be created each time and you would lose pets/tasks. Only
# initialize when the key is missing so the same object survives across reruns.
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner()
    st.session_state["owner_name"] = "Guest"

if "last_plan" not in st.session_state:
    st.session_state.last_plan = None

st.title("🐾 PawPal+")

st.markdown(
    """
Plan pet care tasks, attach them to pets, and generate a schedule that fits your available time.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks based on time, priority, and preferences.
Add pets, add tasks to each pet, then generate a daily plan.
"""
    )

st.divider()

owner = st.session_state.owner
st.session_state.owner_name = st.text_input(
    "Owner display name",
    value=st.session_state.get("owner_name", "Guest"),
)

st.subheader("Pets")
col_pet_a, col_pet_b = st.columns(2)
with col_pet_a:
    new_pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
with col_pet_b:
    new_pet_species = st.text_input("Species", value="dog", key="new_pet_species")

if st.button("Add Pet"):
    name = new_pet_name.strip()
    species = new_pet_species.strip() or "unknown"
    if not name:
        st.warning("Please enter a pet name.")
    else:
        owner.add_pet(Pet(name=name, species=species))
        st.success(f"Added {name} ({species}).")
        st.rerun()

if owner.pets:
    st.caption("Your pets:")
    for p in owner.pets:
        st.write(f"- **{p.name}** ({p.species}) — {len(p.tasks)} task(s)")
else:
    st.info("No pets yet. Add at least one pet to unlock tasks and scheduling.")

st.divider()

has_pets = len(owner.pets) > 0

if has_pets:
    st.subheader("Tasks")
    st.caption(
        "Pick a pet, then add a task. Category is Task.category; "
        "recurrence is Task.frequency (None / Daily / Weekly)."
    )

    pet_labels = [f"{p.name} ({p.species})" for p in owner.pets]
    chosen_label = st.selectbox("Pet for this task", options=pet_labels, key="task_pet_select")
    pet_index = pet_labels.index(chosen_label)
    selected_pet = owner.pets[pet_index]

    t1, t2 = st.columns(2)
    with t1:
        task_description = st.text_input("Description", value="Morning walk", key="task_desc")
    with t2:
        task_category = st.text_input("Category", value="exercise", key="task_cat")

    t3, t4 = st.columns(2)
    with t3:
        task_duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=480,
            value=20,
            key="task_dur",
        )
    with t4:
        priority_label = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=2,
            key="task_pri",
        )

    priority_value = {"low": 3, "medium": 6, "high": 9}[priority_label]
    task_recurrence = st.selectbox(
        "Recurrence (frequency)",
        ["None", "Daily", "Weekly"],
        index=0,
        key="task_recurrence",
    )
    task_recurring = st.checkbox(
        "Also include in every plan while done (is_recurring flag)",
        value=False,
        key="task_recurring",
    )

    if st.button("Add Task"):
        desc = task_description.strip()
        if not desc:
            st.warning("Please enter a task description.")
        else:
            selected_pet.add_task(
                Task(
                    description=desc,
                    duration_mins=int(task_duration),
                    priority=priority_value,
                    frequency=task_recurrence,
                    category=task_category.strip() or "general",
                    is_recurring=task_recurring,
                )
            )
            st.success(f"Task added for **{selected_pet.name}**.")
            st.rerun()

    st.divider()

    st.subheader("Build schedule")
    available_time = st.number_input(
        "Available time (minutes)",
        min_value=1,
        max_value=1440,
        value=60,
        key="avail_time",
    )

    if st.button("Generate Schedule"):
        scheduler = Scheduler()
        st.session_state.last_plan = scheduler.generate_plan(
            owner,
            available_time=int(available_time),
        )
        st.rerun()

else:
    st.session_state.last_plan = None

if st.session_state.last_plan is not None and has_pets:
    plan = st.session_state.last_plan
    st.divider()
    st.subheader("Latest plan")
    st.write(plan.explanation)
    if plan.conflict_warnings:
        for msg in plan.conflict_warnings:
            st.warning(msg)
    if plan.selected_tasks:
        rows = [
            {
                "Description": t.description,
                "Minutes": t.duration_mins,
                "Priority": t.priority,
                "Category": t.category,
                "Recurrence": t.frequency,
            }
            for t in plan.selected_tasks
        ]
        st.table(rows)
    else:
        st.info("No tasks fit this time window.")
    st.caption(f"Total scheduled time: **{plan.total_duration}** minutes.")
