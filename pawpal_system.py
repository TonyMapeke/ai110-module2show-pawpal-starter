from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents one pet care activity and its scheduling metadata."""

    description: str
    duration_mins: int
    priority: int
    frequency: str
    is_completed: bool = False


@dataclass
class Pet:
    """Models a pet and the care tasks assigned to that pet."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a new Task object to the pet's internal task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Holds every pet belonging to one owner for household-level planning."""

    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Registers a Pet in this owner's managed list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns every task from every pet in a single combined list."""
        combined: List[Task] = []
        for pet in self.pets:
            combined.extend(pet.tasks)
        return combined


class Scheduler:
    """Builds a feasible daily plan from an owner's pending tasks and time budget."""

    @staticmethod
    def _sort_tasks_for_scheduling(tasks: List[Task]) -> List[Task]:
        """Orders tasks by descending priority, then ascending duration."""
        return sorted(tasks, key=lambda t: (-t.priority, t.duration_mins))

    @classmethod
    def generate_plan(cls, owner: Owner, available_time: int) -> DailyPlan:
        """Produces a DailyPlan of tasks that fit within the given minute budget."""
        all_tasks = owner.get_all_tasks()
        pending = [t for t in all_tasks if not t.is_completed]
        ordered = cls._sort_tasks_for_scheduling(pending)

        selected: List[Task] = []
        used = 0
        for task in ordered:
            if used + task.duration_mins <= available_time:
                selected.append(task)
                used += task.duration_mins

        selected_ids = {id(t) for t in selected}
        not_fitted = [t for t in ordered if id(t) not in selected_ids]
        explanation = cls._build_explanation(
            owner=owner,
            available_time=available_time,
            total_tasks_considered=len(all_tasks),
            pending_count=len(pending),
            selected=selected,
            not_fitted=not_fitted,
        )

        return DailyPlan(
            selected_tasks=selected,
            total_duration=used,
            explanation=explanation,
        )

    @staticmethod
    def _build_explanation(
        owner: Owner,
        available_time: int,
        total_tasks_considered: int,
        pending_count: int,
        selected: List[Task],
        not_fitted: List[Task],
    ) -> str:
        """Composes a short human-readable summary of scheduling decisions."""
        parts: List[str] = []
        pet_count = len(owner.pets)
        parts.append(
            f"Looked at {total_tasks_considered} task(s) across {pet_count} pet(s); "
            f"{pending_count} still pending (completed tasks ignored)."
        )
        parts.append(
            "Scheduled in order of highest priority first, then shorter tasks first "
            "so more items fit in the time window."
        )
        if not selected:
            parts.append(
                "No tasks fit the available time—raise the time budget or shorten or "
                "complete tasks."
            )
        elif not_fitted:
            skipped = len(not_fitted)
            highest_left = max(not_fitted, key=lambda t: t.priority)
            parts.append(
                f"Dropped {skipped} task(s) that did not fit in {available_time} minutes; "
                f"highest-priority among those left out is {highest_left.priority} "
                f"({highest_left.description})."
            )
        else:
            parts.append("All pending tasks fit within the available time.")
        return " ".join(parts)


@dataclass
class DailyPlan:
    """Captures the chosen tasks, their total time, and why the plan looks this way."""

    selected_tasks: List[Task]
    total_duration: int
    explanation: str

    def display_plan(self) -> str:
        """Returns a multi-line string suitable for logging or terminal display."""
        lines: List[str] = [self.explanation, "", "Selected tasks:"]
        if not self.selected_tasks:
            lines.append("  (none)")
        else:
            for t in self.selected_tasks:
                lines.append(
                    f"  - {t.description} | {t.duration_mins} min | "
                    f"priority {t.priority} | {t.frequency}"
                )
        lines.append(f"\nTotal scheduled: {self.total_duration} minutes")
        return "\n".join(lines)
