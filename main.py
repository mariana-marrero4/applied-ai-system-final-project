"""
PawPal+ Demo Script
Demonstrates the pet scheduling system with Owner, Pet, Task, and Scheduler classes
"""

from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    print("=" * 60)
    print("🐾 PawPal+ - Pet Care Scheduling System")
    print("=" * 60)
    print()
    
    # Create an Owner
    owner = Owner(
        name="Jordan",
        available_time=120,  # 120 minutes available
        preferences={"feeding_time": "morning", "exercise_preference": "evening"}
    )
    print(f"✅ Owner created: {owner.name}")
    print(f"   Available time: {owner.available_time} minutes")
    print()
    
    # Create Pet 1: Mochi (Dog)
    mochi = Pet(
        name="Mochi",
        pet_type="dog",
        age=3
    )
    print(f"✅ Pet 1 created: {mochi.name} ({mochi.pet_type}, age {mochi.age})")
    
    # Create Pet 2: Luna (Cat)
    luna = Pet(
        name="Luna",
        pet_type="cat",
        age=2
    )
    print(f"✅ Pet 2 created: {luna.name} ({luna.pet_type}, age {luna.age})")
    print()
    
    # Add pets to owner
    owner.add_pet(mochi)
    owner.add_pet(luna)
    print(f"✅ Pets added to owner. Total pets: {len(owner.get_pets())}")
    print()
    
    # ===== TASKS FOR MOCHI =====
    print("📋 Adding tasks for Mochi...")
    
    # Task 1: Morning Walk
    task1 = Task(
        task_name="Morning Walk",
        duration=30,
        priority=1,
        prefered_time="morning",
        frequency="daily"
    )
    mochi.add_task(task1)
    print(f"   ✅ {task1.task_name} - {task1.duration} min (Priority: {task1.priority})")
    
    # Task 2: Feeding
    task2 = Task(
        task_name="Feeding",
        duration=15,
        priority=1,
        prefered_time="morning",
        frequency="daily"
    )
    mochi.add_task(task2)
    print(f"   ✅ {task2.task_name} - {task2.duration} min (Priority: {task2.priority})")
    
    # Task 3: Playtime
    task3 = Task(
        task_name="Playtime",
        duration=45,
        priority=2,
        prefered_time="afternoon",
        frequency="daily"
    )
    mochi.add_task(task3)
    print(f"   ✅ {task3.task_name} - {task3.duration} min (Priority: {task3.priority})")
    
    # Task 4: Grooming
    task4 = Task(
        task_name="Grooming",
        duration=60,
        priority=3,
        frequency="weekly"
    )
    mochi.add_task(task4)
    print(f"   ✅ {task4.task_name} - {task4.duration} min (Priority: {task4.priority})")
    print()
    
    # ===== TASKS FOR LUNA =====
    print("📋 Adding tasks for Luna...")
    
    # Task 5: Feeding
    task5 = Task(
        task_name="Feeding",
        duration=10,
        priority=1,
        prefered_time="morning",
        frequency="daily"
    )
    luna.add_task(task5)
    print(f"   ✅ {task5.task_name} - {task5.duration} min (Priority: {task5.priority})")
    
    # Task 6: Litter Box Cleaning
    task6 = Task(
        task_name="Litter Box Cleaning",
        duration=20,
        priority=2,
        frequency="daily"
    )
    luna.add_task(task6)
    print(f"   ✅ {task6.task_name} - {task6.duration} min (Priority: {task6.priority})")
    
    # Task 7: Playtime with toys
    task7 = Task(
        task_name="Interactive Play",
        duration=25,
        priority=2,
        prefered_time="afternoon",
        frequency="daily"
    )
    luna.add_task(task7)
    print(f"   ✅ {task7.task_name} - {task7.duration} min (Priority: {task7.priority})")
    print()
    
    # ===== GENERATE SCHEDULES =====
    print("=" * 60)
    print("📅 TODAY'S SCHEDULE")
    print("=" * 60)
    print()
    
    # Schedule for Mochi
    print(f"🐕 Schedule for {mochi.name}:")
    print("-" * 60)
    scheduler_mochi = Scheduler(owner, mochi, owner.available_time)
    scheduler_mochi.generate_plan()
    print(scheduler_mochi.explain_plan())
    print()
    
    # Schedule for Luna
    print(f"🐈 Schedule for {luna.name}:")
    print("-" * 60)
    scheduler_luna = Scheduler(owner, luna, owner.available_time)
    scheduler_luna.generate_plan()
    print(scheduler_luna.explain_plan())
    print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Total pets: {len(owner.get_pets())}")
    print(f"Mochi - Total tasks: {len(mochi.get_tasks())}, Total duration: {mochi.get_total_duration()} min")
    print(f"Luna - Total tasks: {len(luna.get_tasks())}, Total duration: {luna.get_total_duration()} min")
    print(f"Available time: {owner.available_time} minutes")
    print()
    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
