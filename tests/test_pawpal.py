"""Unit tests for core PawPal+ domain models in pawpal_system."""

from datetime import date, timedelta

import pytest

from pawpal_system import Pet, Task


@pytest.fixture
def sample_task() -> Task:
    """A typical pending care task used across tests."""
    return Task(
        description="Evening walk",
        duration_mins=25,
        priority=8,
        frequency="None",
        category="exercise",
    )


@pytest.fixture
def sample_pet() -> Pet:
    """A pet with no tasks yet."""
    return Pet(name="Mochi", species="Shiba Inu")


def test_task_is_completed_defaults_to_false(sample_task: Task) -> None:
    """New tasks should start as not completed so they appear in scheduling."""
    assert sample_task.is_completed is False


def test_task_can_be_marked_complete_via_attribute(sample_task: Task) -> None:
    """After marking complete, the flag should be True (simulates finishing a chore)."""
    assert sample_task.is_completed is False
    sample_task.is_completed = True
    assert sample_task.is_completed is True


def test_pet_task_list_starts_empty(sample_pet: Pet) -> None:
    """A new pet should have no tasks until the owner adds them."""
    assert sample_pet.tasks == []
    assert len(sample_pet.tasks) == 0


def test_pet_add_task_appends_one_task(
    sample_pet: Pet,
    sample_task: Task,
) -> None:
    """add_task() should grow the pet's task list by exactly one item."""
    assert len(sample_pet.tasks) == 0
    sample_pet.add_task(sample_task)
    assert len(sample_pet.tasks) == 1
    assert sample_pet.tasks[0] is sample_task


def test_mark_complete_daily_returns_next_with_incremented_due_date() -> None:
    base = date(2026, 3, 1)
    t = Task(
        description="Walk",
        duration_mins=15,
        priority=5,
        frequency="Daily",
        due_date=base,
    )
    nxt = t.mark_complete()
    assert t.is_completed is True
    assert nxt is not None
    assert nxt.is_completed is False
    assert nxt.frequency == "Daily"
    assert nxt.due_date == base + timedelta(days=1)


def test_mark_complete_weekly_uses_seven_day_delta() -> None:
    base = date(2026, 3, 1)
    t = Task(
        description="Groom",
        duration_mins=40,
        priority=7,
        frequency="Weekly",
        due_date=base,
    )
    nxt = t.mark_complete()
    assert nxt is not None
    assert nxt.due_date == base + timedelta(days=7)


def test_mark_complete_none_frequency_returns_none() -> None:
    t = Task(description="Vet", duration_mins=30, priority=10, frequency="None")
    nxt = t.mark_complete()
    assert nxt is None
    assert t.is_completed is True


def test_pet_complete_task_appends_next_occurrence() -> None:
    pet = Pet(name="Rex", species="dog")
    base = date(2026, 6, 10)
    walk = Task(
        description="Morning walk",
        duration_mins=20,
        priority=9,
        frequency="Daily",
        due_date=base,
    )
    pet.add_task(walk)
    nxt = pet.complete_task(walk)
    assert len(pet.tasks) == 2
    assert pet.tasks[0] is walk and walk.is_completed
    assert nxt is pet.tasks[1]
    assert nxt.due_date == base + timedelta(days=1)


def test_complete_task_rejects_foreign_task(sample_pet: Pet, sample_task: Task) -> None:
    other = Pet(name="Other", species="cat")
    other.add_task(sample_task)
    with pytest.raises(ValueError, match="not on this pet"):
        sample_pet.complete_task(sample_task)
