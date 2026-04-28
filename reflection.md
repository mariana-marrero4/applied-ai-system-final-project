# PawPal+ Project Reflection

## 1. What are the limitations or biases in your system?

- **Fixed scheduling:** Morning/afternoon slots don't adapt to real user schedules or pet emergencies at night
- **Simple recurrence:** Doesn't account for seasonal changes or varying month lengths (28-31 days)
- **AI hallucinations (mitigated):** Gemini infers details sometimes (e.g., "twice-daily" when we said "daily"). To address this, a validation layer was implemented that cross-checks AI claims against actual task data and removes contradictions
- **Cost bias:** Gemini may recommend expensive products; no guardrails for financial accessibility
- **Species-agnostic:** Treats all pets the same; no consideration for species-specific needs or bonding time
- **User expertise assumed:** Task prioritization assumes owners can accurately rate importance; novices may struggle

---

## 2. Could your AI be misused, and how would you prevent that?

**Potential Misuses:**
1. **False confidence:** Users might follow recommendations blindly and miss actual health emergencies
2. **Misinformation spread:** Summaries could be shared as veterinary advice when they're just scheduling suggestions
3. **Data privacy:** API calls send pet data to Google's servers; sensitive information could be logged
4. **Financial exploitation:** AI could recommend expensive products without guardrails

**Prevention Strategies:**
- **Explicit disclaimers:** PawPal+ is a scheduling tool, not a veterinary advisor; medical concerns require professional help
- **API security:** Filter user prompts to prevent injection attacks; validate all inputs before sending to Gemini
- **Rate limits:** Cap API calls per user to prevent abuse and unexpected costs
- **Offline fallback:** Ensure core scheduling works without AI so users aren't dependent on the API
- **Consent & transparency:** Ask users to opt-in to data sharing with clear disclosure on what's sent

---

## 3. What surprised you while testing your AI's reliability?

**What Worked Well:**
- The Scheduler's core logic (filtering, sorting, conflict detection) was robust—never crashed even with extreme inputs
- 51/51 tests passed on first run, validating the upfront design
- Deterministic code (Task/Owner/Scheduler) proved trustworthy and predictable

**Key Discovery: AI Hallucinations:**
Gemini's summaries sometimes invent task details (e.g., claiming "twice-daily feeding" when we only said "daily"). This surprised me because the AI wasn't just missing information—it was actively creating false claims. To address this, a `_validate_summary()` function was implemented that cross-checks each claim against actual task data and removes contradictions. Testing showed this successfully catches and removes hallucinated frequencies while preserving legitimate recommendations.

**Lessons:**
- Non-deterministic AI (Gemini) requires validation layers; deterministic code does not
- Real reliability comes from integrating safeguards, not just unit tests
- Backend robustness doesn't guarantee frontend safety when AI is involved

---

## 4. Describe your collaboration with AI during this project. 

**a. Identify one instance when the AI gave a helpful suggestion.**

When implementing the RAG summarizer, the AI assistant suggested adding explicit constraints to the Gemini prompts to prevent the model from inferring or inventing details. This led to refining the system prompts to say "Only summarize EXACTLY what the user told you" and "Do NOT infer or extrapolate." While this doesn't eliminate hallucinations entirely, it significantly reduces false claims and makes the AI output more grounded in the actual task data provided. The change improved reliability with minimal effort.

**b. Identify one instance when the AI gave a suggestion that was flawed or incorrect.**

When designing the RAG summaries, the AI suggested having Gemini generate very detailed explanations for every section to "provide thorough guidance." The problem was that Gemini creates verbose, rambling summaries even with minimal input. With just a pet's name, age, and a few tasks, it fills pages with generic filler instead of staying concise. The solution was limiting output length in the prompts and filtering unnecessary text afterward. The key lesson is that more detail doesn't always mean better—sometimes less is more.


