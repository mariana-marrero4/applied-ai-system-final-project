# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

    I want a class Owner that is directly related to a class Pet, because an Owner can have one or more pets but a pet can only have one owner. Then I added a class task that handles all the tasks of each pet based on the owner. Lastly, I added a class Scheduler that creates a plan based on the owner, the pet, tasks assigned, priorities and then it explains the plan. In the UML Scheduler depends on  Owner and Pet to generate the plan. The class Owner has a composition relationship with the class Pet, that also has a composition relationship with the class Task.

- What classes did you include, and what responsibilities did you assign to each?

    Owner class -> holds owner's name, available time, and preferences. This class is responsible of managing the pets.

    Pet class -> holds pet's name, type of pet, breed of pet, and their age. This class is responsible of holding and managing the list of tasks.

    Task class -> reprsents a single care activity that holds name, duration in minutes, priority (1-3), and preffered time of day.

    Scheduler class -> takes an Owner and a Pet and filters tasks based on time constraints and preferences, sorts them by priority, generates a daily plan, and explains the reasoning behind it.


**b. Design changes**

- Did your design change during implementation? 

    Yes, it changed a bit.

- If yes, describe at least one change and why you made it.

    Most of the changes that were made were for convenience. For example, I changed the attribute preferences in the owner class from list to dictionary because it is more convenient to do a key-value search than search in a list for a specific string and risk an error. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
