"""Unit tests for core PawPal+ domain models in pawpal_system."""

import pytest

from pawpal_system import Pet, Task


@pytest.fixture
def sample_task() -> Task:
    """A typical pending care task used across tests."""
    return Task(
        description="Evening walk",
        duration_mins=25,
        priority=8,
        frequency="daily",
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
