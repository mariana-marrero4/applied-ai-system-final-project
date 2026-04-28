"""
RAG (Retrieval-Augmented Generation) module for PawPal+ summaries.
Uses Google Gemini API to generate intelligent pet care summaries.
"""

import os
import re
from pathlib import Path

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ google-generativeai not installed. Install via: pip install google-generativeai")

# Load .env from project root
try:
    from dotenv import load_dotenv
    
    # Find project root by searching up the directory tree for .env
    def _find_project_root():
        """Search up the directory tree for .env file"""
        current = Path(__file__).parent
        for _ in range(5):  # Search up to 5 levels
            if (current / ".env").exists():
                return current
            current = current.parent
        return Path(__file__).parent  # Fallback to script's parent directory
    
    project_root = _find_project_root()
    env_path = project_root / ".env"
    load_dotenv(env_path)
except ImportError:
    print("⚠️ python-dotenv not installed")

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def _get_model():
    """Initialize and return Gemini model, with error handling"""
    if not GENAI_AVAILABLE:
        raise RuntimeError("google-generativeai library not installed")
    
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "tu_api_key_aqui_reemplaza_esto":
        raise ValueError(
            "❌ GOOGLE_API_KEY not configured or still has placeholder value.\n"
            "Please:\n"
            "1. Get your API key from: https://ai.google.dev/\n"
            "2. Replace the placeholder in .env file with your actual key\n"
            "3. Restart the app"
        )
    
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-2.5-flash')


def _format_response(text: str) -> str:
    """
    Post-process LLM response for clean rendering in Streamlit.
    Removes problematic bullet formatting and ensures proper spacing.
    """
    # Simply clean up the text and return as-is (no bullet formatting)
    return text.strip()


def _validate_summary(summary: str, actual_tasks: list) -> str:
    """
    Validate LLM-generated summary against actual task data to catch hallucinations.
    Only removes lines with explicit frequency contradictions (e.g., "twice-daily feeding" when task is "daily").
    
    Args:
        summary: Raw Gemini-generated summary
        actual_tasks: List of actual Task objects from pet/owner
        
    Returns:
        str: Validated summary with flagged hallucinations removed
    """
    if not actual_tasks:
        return summary  # No tasks to validate against
    
    # Extract actual task names and frequencies
    task_frequencies = {task.task_name: task.frequency for task in actual_tasks}
    
    lines = summary.split('\n')
    validated_lines = []
    
    for line in lines:
        # Keep section headers and empty lines
        if line.startswith('####') or line.strip() == '':
            validated_lines.append(line)
            continue
        
        # Only flag hallucinations if line explicitly contradicts task frequency
        # (e.g., "twice-daily feeding" when task is "daily")
        should_remove = False
        for task_name, actual_freq in task_frequencies.items():
            if task_name.lower() in line.lower():
                # Only remove if there's an explicit frequency contradiction
                frequency_patterns = {
                    'daily': r'\btwice.?daily\b|\btwice.?day\b',
                    'weekly': r'\bdaily\b|\btwice.?daily\b',
                    'monthly': r'\bdaily\b|\bweekly\b'
                }
                
                if actual_freq in frequency_patterns:
                    if re.search(frequency_patterns[actual_freq], line, re.IGNORECASE):
                        should_remove = True
                        break
        
        if not should_remove:
            validated_lines.append(line)
    
    return '\n'.join(validated_lines)


def get_individual_pet_summary(pet) -> str:
    """
    Generate a detailed summary for an individual pet using Gemini RAG.
    Focus: Veterinary care and health as primary concerns.
    Format: Structured with bullet points and clear sections.
    
    Args:
        pet: Pet object with name, pet_type, age, and tasks
        
    Returns:
        str: Structured summary with vet care focus
    """
    try:
        model = _get_model()
    except (RuntimeError, ValueError) as e:
        return f"⚠️ Error: {str(e)}"
    
    # Build tasks text
    if pet.tasks:
        tasks_text = "\n".join([
            f"• {task.task_name}: {task.duration} min ({task.frequency}) - Priority: {task.priority}/3"
            for task in pet.tasks
        ])
    else:
        tasks_text = "• No tasks assigned yet"
    
    prompt = f"""
You are a veterinary expert and pet care specialist. Analyze this pet and provide a structured health & care summary.

**PET PROFILE:**
- Name: {pet.name}
- Type/Species: {pet.pet_type}
- Age: {pet.age} years old

**CURRENT CARE TASKS:**
{tasks_text}

RESPOND WITH THIS STRUCTURE (use simple text, no bullets or special formatting):

#### 🚨 VETERINARY PRIORITIES
Briefly list top 3 concerns based on pet type and age

#### 🏥 VET CARE CHECKLIST
Essential checkups, vaccinations, and preventive care for this pet

#### ⚕️ HEALTH CONSIDERATIONS
Key health risks and nutrition considerations for {pet.pet_type} at {pet.age} years old

#### 📋 CURRENT CARE ASSESSMENT
Is the current care plan adequate? Any gaps or well-covered areas?

#### 💡 RECOMMENDED IMPROVEMENTS
Top 2-3 recommendations to improve pet health and care
"""
    
    response = model.generate_content(prompt)
    formatted_response = _format_response(response.text)
    validated_response = _validate_summary(formatted_response, pet.tasks)
    return validated_response


def get_global_pets_summary(owner) -> str:
    """
    Generate a cross-pet summary for all pets of an owner using Gemini RAG.
    Analyzes workload distribution, patterns, and recommendations.
    
    Args:
        owner: Owner object with name, available_time, and list of pets
        
    Returns:
        str: Natural language summary of multi-pet care strategy
    """
    try:
        model = _get_model()
    except (RuntimeError, ValueError) as e:
        return f"⚠️ Error: {str(e)}"
    
    # Build pets summary
    if owner.pets:
        pets_data = []
        total_tasks = 0
        for pet in owner.pets:
            total_duration = pet.get_total_duration()
            task_count = len(pet.tasks)
            total_tasks += task_count
            pets_data.append(
                f"• {pet.name} ({pet.pet_type}, {pet.age} years old): "
                f"{task_count} tasks, {total_duration} min total"
            )
        pets_text = "\n".join(pets_data)
    else:
        pets_text = "• No pets added yet"
        total_tasks = 0
    
    prompt = f"""
You are a veterinary and pet care optimization expert. Analyze this multi-pet household and provide a structured assessment.

**OWNER PROFILE:**
- Owner Name: {owner.name}
- Total Available Time: {owner.available_time} minutes/day
- Morning Availability: {owner.available_time_morning} min
- Afternoon Availability: {owner.available_time_afternoon} min

**PETS OVERVIEW:**
{pets_text}

**Total Tasks in System:** {total_tasks}

RESPOND WITH THIS STRUCTURE IN ORDER (use simple text, no bullets):

#### 📊 WORKLOAD ANALYSIS
Analyze total daily time needed vs available. Determine if under/at/over capacity. Include morning/afternoon utilization.

#### 🐾 PER-PET HEALTH ASSESSMENT
One-line health status for each pet

#### ✅ WELL-COVERED AREAS
What care aspects are being done well across the household

#### 🏥 VETERINARY PRIORITIES
Top veterinary concerns and preventive care needs across all pets

#### 🚨 CRITICAL GAPS
What care is missing or insufficient

#### 💡 RECOMMENDATIONS
Top 2-3 optimization recommendations for better household pet care management
"""
    
    # Collect all tasks from all pets for validation
    all_tasks = []
    for pet in owner.pets:
        all_tasks.extend(pet.tasks)
    
    response = model.generate_content(prompt)
    formatted_response = _format_response(response.text)
    validated_response = _validate_summary(formatted_response, all_tasks)
    return validated_response


def test_api_connection() -> bool:
    """
    Test if the Google Gemini API connection is working.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        model = _get_model()
        test_response = model.generate_content("Responde con 'OK' solamente.")
        return "OK" in test_response.text
    except Exception as e:
        print(f"❌ API Connection Test Failed: {str(e)}")
        return False
