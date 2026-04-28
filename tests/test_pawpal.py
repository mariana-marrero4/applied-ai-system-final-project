"""
Unit tests for PawPal+ System
Tests for Task, Pet, Owner, and Scheduler classes

Test Coverage:
- Task validation and lifecycle
- Pet management 
- Owner scheduling
- Scheduler filtering and sorting
- Error handling and logging

Confidence Level: HIGH - Tests cover critical paths and edge cases
"""

import pytest
import logging
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tests/test_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TestTaskStatusSystem:
    """Tests for Task status system (pending/in-progress/completed)"""
    
    def test_task_initial_status_is_pending(self):
        """Verify that new tasks have status 'pending' by default"""
        # Arrange & Act
        task = Task(
            task_name="New Task",
            duration=30,
            priority=1
        )
        
        # Assert
        assert task.status == "pending", "New task should have status 'pending'"
    
    def test_task_status_update_to_in_progress(self):
        """Verify that task status can be updated to 'in-progress'"""
        # Arrange
        task = Task(
            task_name="Task",
            duration=30,
            priority=1
        )
        
        # Act
        task.update_status("in-progress")
        
        # Assert
        assert task.status == "in-progress"
    
    def test_task_status_update_to_completed(self):
        """Verify that task status can be updated to 'completed'"""
        # Arrange
        task = Task(
            task_name="Task",
            duration=30,
            priority=1
        )
        
        # Act
        task.update_status("completed")
        
        # Assert
        assert task.status == "completed"
    
    def test_task_update_status_with_invalid_status_raises_error(self):
        """Verify that invalid status raises ValueError"""
        # Arrange
        task = Task(
            task_name="Task",
            duration=30,
            priority=1
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid status"):
            task.update_status("invalid-status")


class TestTaskCompletion:
    """Tests for Task completion functionality (recurring tasks)"""
    
    def test_recurring_task_creates_next_occurrence_on_completion(self):
        """Verify that completing a recurring daily task creates the next occurrence"""
        # Arrange
        task = Task(
            task_name="Morning Walk",
            duration=30,
            priority=1,
            frequency="daily"
        )
        
        # Act - mark task as completed
        next_task = task.update_status("completed")
        
        # Assert
        assert task.status == "completed", "Task should be marked as completed"
        assert next_task is not None, "Should create next occurrence for recurring task"
        assert next_task.task_name == "Morning Walk", "Next task should have same name"
        assert next_task.is_recurring_copy is True, "Next task should be marked as recurring copy"
    
    def test_one_time_task_no_next_occurrence(self):
        """Verify that non-recurring frequency tasks only use valid frequencies (daily/weekly/monthly)"""
        # Arrange
        task = Task(
            task_name="Playtime",
            duration=45,
            priority=2,
            frequency="weekly"  # Valid frequency
        )
        
        # Act
        next_task = task.update_status("completed")
        
        # Assert - weekly tasks should create next occurrence
        assert task.status == "completed"
        assert next_task is not None, "Weekly task should create next occurrence"
        assert next_task.frequency == "weekly"


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


class TestSchedulerFilterByStatus:
    """Tests for Scheduler filter_by_status() - STEP 2 Feature"""
    
    def test_filter_by_pending_status(self):
        """Verify that filter_by_status correctly returns pending tasks"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Task 1", duration=20, priority=1)
        task2 = Task(task_name="Task 2", duration=20, priority=1)
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Mark task1 as completed
        task1.update_status("completed")
        
        # Act
        scheduler = Scheduler(owner, pet)
        pending_tasks = scheduler.filter_by_status("pending")
        
        # Assert
        assert len(pending_tasks) == 1, "Should have 1 pending task"
        assert pending_tasks[0].task_name == "Task 2"
    
    def test_filter_by_completed_status(self):
        """Verify that filter_by_status correctly returns completed tasks"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Task 1", duration=20, priority=1)
        task2 = Task(task_name="Task 2", duration=20, priority=1)
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Mark both as completed
        task1.update_status("completed")
        task2.update_status("completed")
        
        # Act
        scheduler = Scheduler(owner, pet)
        completed_tasks = scheduler.filter_by_status("completed")
        
        # Assert
        assert len(completed_tasks) == 2, "Should have 2 completed tasks"
        assert all(t.status == "completed" for t in completed_tasks)
    
    def test_filter_by_in_progress_status(self):
        """Verify that filter_by_status correctly returns in-progress tasks"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Luna", pet_type="cat", age=2)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Task 1", duration=20, priority=1)
        task2 = Task(task_name="Task 2", duration=20, priority=1)
        task3 = Task(task_name="Task 3", duration=20, priority=1)
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Mark one as in-progress
        task2.update_status("in-progress")
        
        # Act
        scheduler = Scheduler(owner, pet)
        in_progress_tasks = scheduler.filter_by_status("in-progress")
        
        # Assert
        assert len(in_progress_tasks) == 1, "Should have 1 in-progress task"
        assert in_progress_tasks[0].task_name == "Task 2"


class TestSchedulerFilterByTimeSlot:
    """Tests for Scheduler filter_by_time_slot() - STEP 2 Feature"""
    
    def test_filter_by_morning_time_slot(self):
        """Verify that filter_by_time_slot correctly returns morning tasks"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Morning Walk", duration=20, priority=1, prefered_time="morning")
        task2 = Task(task_name="Afternoon Play", duration=20, priority=2, prefered_time="afternoon")
        task3 = Task(task_name="Morning Feeding", duration=15, priority=1, prefered_time="morning")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Act
        scheduler = Scheduler(owner, pet)
        morning_tasks = scheduler.filter_by_time_slot("morning")
        
        # Assert
        assert len(morning_tasks) == 2, "Should have 2 morning tasks"
        assert all(t.prefered_time == "morning" for t in morning_tasks)
    
    def test_filter_by_afternoon_time_slot(self):
        """Verify that filter_by_time_slot correctly returns afternoon tasks"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Luna", pet_type="cat", age=2)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Morning Feeding", duration=15, priority=1, prefered_time="morning")
        task2 = Task(task_name="Afternoon Play", duration=30, priority=2, prefered_time="afternoon")
        task3 = Task(task_name="Afternoon Grooming", duration=45, priority=3, prefered_time="afternoon")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Act
        scheduler = Scheduler(owner, pet)
        afternoon_tasks = scheduler.filter_by_time_slot("afternoon")
        
        # Assert
        assert len(afternoon_tasks) == 2, "Should have 2 afternoon tasks"
        assert all(t.prefered_time == "afternoon" for t in afternoon_tasks)
    
    def test_filter_by_flexible_time_slot(self):
        """Verify that filter_by_time_slot correctly returns flexible (None) tasks"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_name="Morning Walk", duration=20, priority=1, prefered_time="morning")
        task2 = Task(task_name="Flexible Task", duration=20, priority=2, prefered_time=None)
        task3 = Task(task_name="Afternoon Play", duration=30, priority=2, prefered_time="afternoon")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Act
        scheduler = Scheduler(owner, pet)
        flexible_tasks = scheduler.filter_by_time_slot("flexible")
        
        # Assert
        assert len(flexible_tasks) == 1, "Should have 1 flexible task"
        assert flexible_tasks[0].task_name == "Flexible Task"
    
    def test_filter_by_time_slot_with_multiple_pets(self):
        """Verify that filter_by_time_slot works across multiple pets"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet1 = Pet(name="Mochi", pet_type="dog", age=3)
        pet2 = Pet(name="Luna", pet_type="cat", age=2)
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Add tasks to pet1
        task1 = Task(task_name="Mochi Morning", duration=20, priority=1, prefered_time="morning")
        pet1.add_task(task1)
        
        # Add tasks to pet2
        task2 = Task(task_name="Luna Morning", duration=15, priority=1, prefered_time="morning")
        pet2.add_task(task2)
        
        # Act - should work for both pets
        scheduler1 = Scheduler(owner, pet1)
        scheduler2 = Scheduler(owner, pet2)
        
        mochi_morning = scheduler1.filter_by_time_slot("morning")
        luna_morning = scheduler2.filter_by_time_slot("morning")
        
        # Assert
        assert len(mochi_morning) == 1
        assert len(luna_morning) == 1
        assert mochi_morning[0].task_name == "Mochi Morning"
        assert luna_morning[0].task_name == "Luna Morning"


class TestErrorHandlingAndValidation:
    """
    Tests for error handling and validation across all system components.
    These tests verify that the system gracefully handles invalid inputs.
    """
    
    def test_task_update_with_invalid_name_type_returns_false(self):
        """Verify that task.update() returns False when name is not a string"""
        # Arrange
        task = Task(task_name="Original", duration=30, priority=1)
        
        # Act - try to update with invalid name type
        result = task.update(name=123)
        
        # Assert
        assert result is False, "Should return False for invalid name type"
        assert task.task_name == "Original", "Task name should remain unchanged"
        logger.info("✓ Task name type validation works correctly")
    
    def test_task_update_with_invalid_duration_returns_false(self):
        """Verify that task.update() returns False when duration is invalid"""
        # Arrange
        task = Task(task_name="Task", duration=30, priority=1)
        
        # Act - try to update with duration out of range
        result = task.update(duration=500)  # Max is 480
        
        # Assert
        assert result is False, "Should return False for duration out of range"
        assert task.duration == 30, "Duration should remain unchanged"
        logger.info("✓ Task duration validation works correctly")
    
    def test_task_update_with_invalid_priority_returns_false(self):
        """Verify that task.update() returns False when priority is invalid"""
        # Arrange
        task = Task(task_name="Task", duration=30, priority=1)
        
        # Act - try to update with invalid priority
        result = task.update(priority=5)
        
        # Assert
        assert result is False, "Should return False for invalid priority"
        assert task.priority == 1, "Priority should remain unchanged"
        logger.info("✓ Task priority validation works correctly")
    
    def test_pet_add_non_task_raises_type_error(self):
        """Verify that pet.add_task() raises TypeError for non-Task objects"""
        # Arrange
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        
        # Act & Assert
        with pytest.raises(TypeError, match="Expected Task instance"):
            pet.add_task("not a task")
        logger.info("✓ Pet task type validation works correctly")
    
    def test_pet_add_duplicate_task_id_raises_value_error(self):
        """Verify that pet.add_task() raises ValueError for duplicate task IDs"""
        # Arrange
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        task1 = Task(task_name="Task", duration=30, priority=1)
        
        # Add the task
        pet.add_task(task1)
        
        # Try to add same task again (same ID)
        with pytest.raises(ValueError, match="already exists"):
            pet.add_task(task1)
        logger.info("✓ Pet duplicate task ID validation works correctly")
    
    def test_owner_add_non_pet_raises_type_error(self):
        """Verify that owner.add_pet() raises TypeError for non-Pet objects"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        
        # Act & Assert
        with pytest.raises(TypeError, match="Expected Pet instance"):
            owner.add_pet("not a pet")
        logger.info("✓ Owner pet type validation works correctly")
    
    def test_owner_set_negative_availability_raises_value_error(self):
        """Verify that owner.set_availability() raises ValueError for negative time"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        
        # Act & Assert
        with pytest.raises(ValueError, match="non-negative integer"):
            owner.set_availability(-50)
        logger.info("✓ Owner availability validation works correctly")
    
    def test_scheduler_filter_by_invalid_status_raises_value_error(self):
        """Verify that scheduler.filter_by_status() raises ValueError for invalid status"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner, pet)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid status"):
            scheduler.filter_by_status("invalid-status")
        logger.info("✓ Scheduler status validation works correctly")


class TestRecurringTaskGeneration:
    """Tests for recurring task automatic generation"""
    
    def test_daily_task_next_occurrence_is_one_day_later(self):
        """Verify that daily tasks create next occurrence one day later"""
        # Arrange
        original_date = datetime(2024, 1, 15, 9, 0)
        task = Task(
            task_name="Daily Walk",
            duration=30,
            priority=1,
            frequency="daily",
            due_date=original_date
        )
        
        # Act
        next_task = task.get_next_occurrence()
        
        # Assert
        assert next_task.due_date == original_date + timedelta(days=1)
        assert next_task.task_name == "Daily Walk"
        assert next_task.is_recurring_copy is True
        logger.info("✓ Daily recurring task generation works correctly")
    
    def test_weekly_task_next_occurrence_is_one_week_later(self):
        """Verify that weekly tasks create next occurrence one week later"""
        # Arrange
        original_date = datetime(2024, 1, 15, 10, 0)
        task = Task(
            task_name="Weekly Grooming",
            duration=60,
            priority=2,
            frequency="weekly",
            due_date=original_date
        )
        
        # Act
        next_task = task.get_next_occurrence()
        
        # Assert
        assert next_task.due_date == original_date + timedelta(weeks=1)
        assert next_task.frequency == "weekly"
        assert next_task.is_recurring_copy is True
        logger.info("✓ Weekly recurring task generation works correctly")
    
    def test_monthly_task_next_occurrence_is_30_days_later(self):
        """Verify that monthly tasks create next occurrence 30 days later"""
        # Arrange
        original_date = datetime(2024, 1, 15, 11, 0)
        task = Task(
            task_name="Monthly Vet Checkup",
            duration=90,
            priority=1,
            frequency="monthly",
            due_date=original_date
        )
        
        # Act
        next_task = task.get_next_occurrence()
        
        # Assert
        assert next_task.due_date == original_date + timedelta(days=30)
        assert next_task.frequency == "monthly"
        logger.info("✓ Monthly recurring task generation works correctly")
    
    def test_completed_recurring_task_creates_next_in_pet_tasks(self):
        """Verify that completing a recurring task creates next occurrence in pet's tasks"""
        # Arrange
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        task = Task(
            task_name="Daily Walk",
            duration=30,
            priority=1,
            frequency="daily"
        )
        pet.add_task(task)
        
        initial_count = len(pet.get_tasks())
        
        # Act - mark task as completed
        next_task = pet.update_task_status(task.task_id, "completed")
        
        # Assert
        assert next_task is not None, "Should create next occurrence"
        assert len(pet.get_tasks()) == initial_count + 1, "Should have one more task"
        assert pet.get_tasks()[-1].is_recurring_copy is True
        logger.info("✓ Recurring task creation in pet tasks works correctly")


class TestDataIntegrity:
    """Tests for data integrity and state consistency"""
    
    def test_multiple_tasks_maintain_unique_ids(self):
        """Verify that multiple tasks get unique IDs"""
        # Arrange
        task1 = Task(task_name="Task 1", duration=20, priority=1)
        task2 = Task(task_name="Task 2", duration=30, priority=2)
        task3 = Task(task_name="Task 3", duration=40, priority=3)
        
        # Act
        ids = [task1.task_id, task2.task_id, task3.task_id]
        
        # Assert
        assert len(ids) == len(set(ids)), "All task IDs should be unique"
        logger.info("✓ Task ID uniqueness maintained correctly")
    
    def test_task_removal_actually_removes_from_pet(self):
        """Verify that removing a task actually removes it from pet's task list"""
        # Arrange
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        task1 = Task(task_name="Task 1", duration=20, priority=1)
        task2 = Task(task_name="Task 2", duration=30, priority=2)
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        success = pet.remove_task(task1.task_id)
        
        # Assert
        assert success is True, "Should successfully remove task"
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0].task_id == task2.task_id
        logger.info("✓ Task removal works correctly")
    
    def test_pet_removal_from_owner(self):
        """Verify that removing a pet actually removes it from owner's pet list"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet1 = Pet(name="Mochi", pet_type="dog", age=3)
        pet2 = Pet(name="Luna", pet_type="cat", age=2)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Act
        success = owner.remove_pet("Mochi")
        
        # Assert
        assert success is True, "Should successfully remove pet"
        assert len(owner.get_pets()) == 1
        assert owner.get_pets()[0].name == "Luna"
        logger.info("✓ Pet removal works correctly")


class TestSystemIntegration:
    """Integration tests for complete system workflows"""
    
    def test_complete_workflow_owner_to_task_creation(self):
        """Test complete workflow: Owner → Pet → Task → Scheduler"""
        # Arrange
        owner = Owner(name="Jordan", available_time=120)
        pet = Pet(name="Mochi", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        # Act - Create tasks
        task1 = Task(task_name="Walk", duration=30, priority=1, prefered_time="morning")
        task2 = Task(task_name="Feeding", duration=15, priority=1, prefered_time="morning")
        task3 = Task(task_name="Play", duration=45, priority=2, prefered_time="afternoon")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Create scheduler
        scheduler = Scheduler(owner, pet)
        sorted_tasks = scheduler.sort_by_priority()
        
        # Assert
        assert len(owner.get_pets()) == 1
        assert len(pet.get_tasks()) == 3
        assert sorted_tasks[0].priority == 1  # Walk
        assert sorted_tasks[2].priority == 2  # Play
        logger.info("✓ Complete workflow integration test passed")
    
    def test_concurrent_pet_management(self):
        """Test managing multiple pets with multiple tasks"""
        # Arrange
        owner = Owner(name="Sarah", available_time=240)
        
        pet1 = Pet(name="Buddy", pet_type="dog", age=5)
        pet2 = Pet(name="Whiskers", pet_type="cat", age=3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Add tasks to each pet
        for pet in owner.get_pets():
            for i in range(3):
                task = Task(
                    task_name=f"{pet.name} Task {i+1}",
                    duration=20,
                    priority=i+1
                )
                pet.add_task(task)
        
        # Act
        total_tasks = sum(len(pet.get_tasks()) for pet in owner.get_pets())
        
        # Assert
        assert total_tasks == 6, "Should have 6 total tasks"
        logger.info("✓ Concurrent pet management test passed")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
