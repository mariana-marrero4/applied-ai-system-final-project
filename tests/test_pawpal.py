"""
Unit tests for PawPal+ System
Tests for Task, Pet, Owner, and Scheduler classes
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Tests for Task completion functionality"""
    
    def test_task_completion_status_changes(self):
        """Verify that calling mark_complete() actually changes the task's status"""
        # Arrange
        task = Task(
            task_name="Morning Walk",
            duration=30,
            priority=1,
            frequency="daily"
        )
        
        # Assert initial state
        assert task.completed is False, "Task should not be completed initially"
        
        # Act - mark task as complete
        task.mark_complete()
        
        # Assert final state
        assert task.completed is True, "Task should be completed after calling mark_complete()"
    
    def test_task_completion_persists(self):
        """Verify that completion status persists after being set"""
        # Arrange
        task = Task(
            task_name="Feeding",
            duration=15,
            priority=1
        )
        
        # Act
        task.mark_complete()
        
        # Assert - check multiple times to ensure it persists
        assert task.completed is True
        assert task.completed is True  # Should still be True


class TestTaskAddition:
    """Tests for Task addition to Pet functionality"""
    
    def test_adding_task_to_pet_increases_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count"""
        # Arrange
        pet = Pet(
            name="Mochi",
            pet_type="dog",
            age=3
        )
        
        task1 = Task(
            task_name="Walk",
            duration=30,
            priority=1,
            frequency="daily"
        )
        
        task2 = Task(
            task_name="Feeding",
            duration=15,
            priority=1,
            frequency="daily"
        )
        
        # Assert initial state
        initial_count = len(pet.get_tasks())
        assert initial_count == 0, "Pet should have no tasks initially"
        
        # Act - add first task
        pet.add_task(task1)
        
        # Assert after first addition
        assert len(pet.get_tasks()) == 1, "Pet should have 1 task after adding one task"
        
        # Act - add second task
        pet.add_task(task2)
        
        # Assert after second addition
        assert len(pet.get_tasks()) == 2, "Pet should have 2 tasks after adding two tasks"
    
    def test_adding_multiple_tasks_maintains_order(self):
        """Verify that tasks are maintained in the order they were added"""
        # Arrange
        pet = Pet(
            name="Luna",
            pet_type="cat",
            age=2
        )
        
        task1 = Task(task_name="Task 1", duration=10, priority=1)
        task2 = Task(task_name="Task 2", duration=20, priority=2)
        task3 = Task(task_name="Task 3", duration=30, priority=3)
        
        # Act
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Assert
        tasks = pet.get_tasks()
        assert len(tasks) == 3
        assert tasks[0].task_name == "Task 1", "First task should be Task 1"
        assert tasks[1].task_name == "Task 2", "Second task should be Task 2"
        assert tasks[2].task_name == "Task 3", "Third task should be Task 3"


class TestTaskValidation:
    """Tests for Task validation during creation"""
    
    def test_task_creation_with_valid_data(self):
        """Verify that Task can be created with valid data"""
        # Act & Assert
        task = Task(
            task_name="Valid Task",
            duration=30,
            priority=1,
            frequency="daily"
        )
        
        assert task.task_name == "Valid Task"
        assert task.duration == 30
        assert task.priority == 1
    
    def test_task_creation_with_invalid_empty_name(self):
        """Verify that Task creation fails with empty name"""
        with pytest.raises(ValueError, match="Task name cannot be empty"):
            Task(
                task_name="",
                duration=30,
                priority=1
            )
    
    def test_task_creation_with_invalid_priority(self):
        """Verify that Task creation fails with invalid priority"""
        with pytest.raises(ValueError, match="Priority must be an integer between 1 and 3"):
            Task(
                task_name="Task",
                duration=30,
                priority=5  # Invalid priority
            )
    
    def test_task_creation_with_invalid_duration(self):
        """Verify that Task creation fails with invalid duration"""
        with pytest.raises(ValueError, match="Duration must be an integer between 1 and 480 minutes"):
            Task(
                task_name="Task",
                duration=0,  # Invalid duration
                priority=1
            )


class TestPetNoDuplicates:
    """Tests for preventing duplicate pets in Owner"""
    
    def test_owner_cannot_add_duplicate_pet(self):
        """Verify that Owner cannot add a pet with same name, type, and age"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        
        pet1 = Pet(
            name="Mochi",
            pet_type="dog",
            age=3
        )
        
        pet2 = Pet(
            name="Mochi",
            pet_type="dog",
            age=3
        )
        
        # Act - add first pet
        owner.add_pet(pet1)
        
        # Assert - trying to add duplicate should raise error
        with pytest.raises(ValueError, match="already exists"):
            owner.add_pet(pet2)
    
    def test_owner_can_add_pets_with_different_names(self):
        """Verify that Owner can add multiple pets with different names"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        
        pet1 = Pet(name="Mochi", pet_type="dog", age=3)
        pet2 = Pet(name="Luna", pet_type="cat", age=2)
        
        # Act
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Assert
        assert len(owner.get_pets()) == 2
        assert owner.get_pets()[0].name == "Mochi"
        assert owner.get_pets()[1].name == "Luna"


class TestTaskIsFeasible:
    """Tests for Task feasibility checking"""
    
    def test_task_is_feasible_with_sufficient_time(self):
        """Verify that task is feasible when duration fits in available time"""
        # Arrange
        task = Task(
            task_name="Quick Task",
            duration=30,
            priority=1
        )
        available_time = 60
        
        # Act & Assert
        assert task.is_feasible(available_time) is True
    
    def test_task_is_not_feasible_with_insufficient_time(self):
        """Verify that task is not feasible when duration exceeds available time"""
        # Arrange
        task = Task(
            task_name="Long Task",
            duration=60,
            priority=1
        )
        available_time = 30
        
        # Act & Assert
        assert task.is_feasible(available_time) is False
    
    def test_task_is_feasible_with_exact_time(self):
        """Verify that task is feasible when duration equals available time"""
        # Arrange
        task = Task(
            task_name="Exact Task",
            duration=45,
            priority=1
        )
        available_time = 45
        
        # Act & Assert
        assert task.is_feasible(available_time) is True
    
    def test_task_feasible_with_negative_time_raises_error(self):
        """Verify that checking feasibility with negative time raises ValueError"""
        # Arrange
        task = Task(
            task_name="Task",
            duration=30,
            priority=1
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Available time must be a non-negative integer"):
            task.is_feasible(-10)


class TestOwnerTimeSlots:
    """Tests for Owner time slot functionality"""
    
    def test_owner_auto_assigns_time_slots_50_50(self):
        """Verify that Owner auto-assigns time slots 50/50 if not provided"""
        # Arrange & Act
        owner = Owner(name="Jordan", available_time=120)
        
        # Assert - should auto-assign 50/50
        assert owner.available_time_morning == 60, "Morning should be 50% of total (60 min)"
        assert owner.available_time_afternoon == 60, "Afternoon should be 50% of total (60 min)"
    
    def test_owner_validates_time_slot_sum(self):
        """Verify that Owner validates morning + afternoon = total"""
        # This should raise ValueError because 50 + 40 != 120
        with pytest.raises(ValueError, match="Time slot mismatch"):
            Owner(
                name="Jordan",
                available_time=120,
                available_time_morning=50,
                available_time_afternoon=40
            )
    
    def test_owner_accepts_valid_time_slots(self):
        """Verify that Owner accepts valid time slot assignment"""
        # Arrange & Act
        owner = Owner(
            name="Jordan",
            available_time=120,
            available_time_morning=80,
            available_time_afternoon=40
        )
        
        # Assert
        assert owner.available_time_morning == 80
        assert owner.available_time_afternoon == 40
        assert owner.available_time == 120
    
    def test_owner_rejects_negative_morning_time(self):
        """Verify that Owner rejects negative morning time"""
        with pytest.raises(ValueError, match="Invalid available_time_morning"):
            Owner(
                name="Jordan",
                available_time=120,
                available_time_morning=-10,
                available_time_afternoon=130
            )
    
    def test_owner_rejects_negative_afternoon_time(self):
        """Verify that Owner rejects negative afternoon time"""
        with pytest.raises(ValueError, match="Invalid available_time_afternoon"):
            Owner(
                name="Jordan",
                available_time=120,
                available_time_morning=100,
                available_time_afternoon=-20
            )


class TestSchedulerConflictDetection:
    """Tests for improved Scheduler conflict detection"""
    
    def test_detect_conflicts_morning_slot_exceeded(self):
        """Verify that conflicts are detected when morning slot is exceeded"""
        # Arrange
        owner = Owner(
            name="Jordan",
            available_time=120,
            available_time_morning=30,
            available_time_afternoon=90
        )
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        # Create tasks that exceed morning slot
        task1 = Task(
            task_name="Morning Walk",
            duration=20,
            priority=1,
            prefered_time="morning"
        )
        task2 = Task(
            task_name="Morning Feeding",
            duration=20,
            priority=1,
            prefered_time="morning"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner, pet)
        scheduler.generate_plan()
        conflicts = scheduler.detect_conflicts()
        
        # Assert - should detect morning slot conflict
        assert len(conflicts) > 0, "Should detect morning slot conflict"
        assert any("morning" in c.lower() for c in conflicts), "Conflict should mention morning"
    
    def test_detect_conflicts_afternoon_slot_exceeded(self):
        """Verify that conflicts are detected when afternoon slot is exceeded"""
        # Arrange
        owner = Owner(
            name="Jordan",
            available_time=120,
            available_time_morning=90,
            available_time_afternoon=30
        )
        pet = Pet(name="Luna", pet_type="cat", age=2)
        owner.add_pet(pet)
        
        # Create tasks that exceed afternoon slot
        task1 = Task(
            task_name="Afternoon Play",
            duration=20,
            priority=2,
            prefered_time="afternoon"
        )
        task2 = Task(
            task_name="Afternoon Grooming",
            duration=20,
            priority=2,
            prefered_time="afternoon"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner, pet)
        scheduler.generate_plan()
        conflicts = scheduler.detect_conflicts()
        
        # Assert - should detect afternoon slot conflict
        assert len(conflicts) > 0, "Should detect afternoon slot conflict"
        assert any("afternoon" in c.lower() for c in conflicts), "Conflict should mention afternoon"
    
    def test_detect_conflicts_no_conflicts(self):
        """Verify that no conflicts are detected when tasks fit properly"""
        # Arrange
        owner = Owner(
            name="Jordan",
            available_time=120,
            available_time_morning=60,
            available_time_afternoon=60
        )
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        # Create tasks that fit perfectly
        task1 = Task(
            task_name="Morning Walk",
            duration=30,
            priority=1,
            prefered_time="morning"
        )
        task2 = Task(
            task_name="Afternoon Play",
            duration=40,
            priority=2,
            prefered_time="afternoon"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner, pet)
        scheduler.generate_plan()
        conflicts = scheduler.detect_conflicts()
        
        # Assert - should have no conflicts
        assert len(conflicts) == 0, "Should have no conflicts when tasks fit"


class TestSchedulerPrioritySorting:
    """Tests for Scheduler priority sorting"""
    
    def test_scheduler_sorts_by_priority_ascending(self):
        """Verify that Scheduler sorts tasks with priority 1 first (highest priority)"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Priority 2", duration=20, priority=2)
        task2 = Task(task_name="Priority 1", duration=30, priority=1)
        task3 = Task(task_name="Priority 3", duration=40, priority=3)
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Act
        scheduler = Scheduler(owner, pet)
        sorted_tasks = scheduler.sort_by_priority()
        
        # Assert
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].priority == 1, "Priority 1 task should be first"
        assert sorted_tasks[1].priority == 2, "Priority 2 task should be second"
        assert sorted_tasks[2].priority == 3, "Priority 3 task should be third"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
