from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    duration_mins: int
    priority: int
    category: str

    def update_priority(self, new_priority: int) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_total_task_time(self) -> int:
        pass


class Scheduler:
    def __init__(self, available_time: int) -> None:
        self.available_time = available_time

    def generate_plan(self, pet: Pet) -> "DailyPlan":
        pass

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        pass


class DailyPlan:
    def __init__(
        self,
        selected_tasks: List[Task],
        total_duration: int,
        explanation: str,
    ) -> None:
        self.selected_tasks = selected_tasks
        self.total_duration = total_duration
        self.explanation = explanation

    def display_plan(self) -> None:
        pass
