from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Task:
    """Dataclass representing a pet task"""
    task_id: str
    task_name: str
    duration: int  # in minutes
    priority: int  # 1-3, where 3 is highest
    prefered_time: Optional[str] = None
    
    def update(self):
        """Update task details"""
        pass
    
    def is_feasible(self) -> bool:
        """Check if task is feasible given constraints"""
        pass


@dataclass
class Pet:
    """Dataclass representing a pet"""
    name: str
    pet_type: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet"""
        pass
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks for the pet"""
        pass
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task by task_id"""
        pass
    
    def get_total_duration(self) -> int:
        """Calculate total duration of all tasks"""
        pass


@dataclass
class Owner:
    """Dataclass representing a pet owner"""
    name: str
    available_time: int
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner"""
        pass
    
    def get_pets(self) -> List[Pet]:
        """Get all pets owned"""
        pass
    
    def set_availability(self, time: int) -> None:
        """Set available time for pet care"""
        pass


class Scheduler:
    """Class for scheduling pet tasks"""
    
    def __init__(self, owner: Owner, pet: Pet, available_time: int):
        self.owner = owner
        self.pet = pet
        self.available_time = owner.available_time
        self.plan: List[Task] = []
    
    def generate_plan(self) -> List[Task]:
        """Generate a schedule plan for tasks"""
        pass
    
    def explain_plan(self) -> str:
        """Provide explanation of the generated plan"""
        pass
    
    def filter_by_constraints(self) -> List[Task]:
        """Filter tasks based on constraints"""
        pass
    
    def sort_by_priority(self) -> List[Task]:
        """Sort tasks by priority"""
        pass
