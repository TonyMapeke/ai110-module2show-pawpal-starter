"""Demo script: simulates Alex's pets and prints a daily care plan (60-minute window)."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # --- Owner & pets ---
    alex = Owner()
    buddy = Pet(name="Buddy", species="Golden Retriever")
    misty = Pet(name="Misty", species="Tabby")

    # Buddy's tasks
    buddy.add_task(
        Task(
            description="Morning walk",
            duration_mins=30,
            priority=9,
            frequency="daily",
        )
    )
    buddy.add_task(
        Task(
            description="Training session",
            duration_mins=20,
            priority=6,
            frequency="weekdays",
        )
    )
    buddy.add_task(
        Task(
            description="Monthly flea treatment",
            duration_mins=10,
            priority=10,
            frequency="monthly",
            is_completed=True,
        )
    )

    # Misty's tasks
    misty.add_task(
        Task(
            description="Breakfast feeding",
            duration_mins=15,
            priority=10,
            frequency="daily",
        )
    )
    misty.add_task(
        Task(
            description="Full grooming",
            duration_mins=45,
            priority=7,
            frequency="weekly",
        )
    )

    alex.add_pet(buddy)
    alex.add_pet(misty)

    # --- Schedule ---
    scheduler = Scheduler()
    plan = scheduler.generate_plan(alex, available_time=60)

    # --- Output ---
    divider = "*" * 52
    section = "-" * 52

    print(divider)
    print("  DAILY CARE PLAN - Alex's pets (60 min available)")
    print(divider)
    print()

    if not plan.selected_tasks:
        print("  No tasks scheduled for this window.")
    else:
        for i, task in enumerate(plan.selected_tasks, start=1):
            print(f"  {i}. {task.description}")
            print(f"     Duration: {task.duration_mins} min  |  Priority: {task.priority}")
            print(f"     Frequency: {task.frequency}")
            print(section)

    print()
    print("  EXPLANATION")
    print(section)
    print(f"  {plan.explanation}")
    print()
    print("  TOTAL TIME USED")
    print(section)
    print(f"  {plan.total_duration} minutes")
    print()
    print(divider)


if __name__ == "__main__":
    main()
