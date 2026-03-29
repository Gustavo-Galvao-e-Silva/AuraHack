import json
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types
from agents import doctor, summarizer, checker_agent, task_factory
from schemas import GoalCheck, NewTasks, PatientSummary
import time


class AnamnesisAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="anamnesis",
            sub_agents=[doctor, summarizer, checker_agent, task_factory],
            **kwargs,
        )

    async def _run_async_impl(self, ctx: InvocationContext):
        if "current_goals" not in ctx.session.state:
            ctx.session.state["current_goals"] = ["Identify primary symptom"]

        # If patient just answered, process it first
        if ctx.session.state.get("awaiting_patient"):

            # --- Step 2: Summarizer ---
            t = time.time()
            async for event in summarizer.run_async(ctx):
                yield event
                if hasattr(event, "data") and isinstance(event.data, PatientSummary):
                    ctx.session.state["patient_summary"] = event.data
                elif event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            try:
                                ctx.session.state["patient_summary"] = PatientSummary(
                                    **json.loads(part.text.strip())
                                )
                            except Exception:
                                pass
            print(f"[DEBUG] Summary: {ctx.session.state.get('patient_summary')}")

            # --- Step 3: Checker ---
            remove = []
            for goal in ctx.session.state["current_goals"]:
                ctx.session.state["goal"] = goal
                message = [
                        event async for events in checker_agent.run_async(ctx)
                    ][-1]
                remove.append(
                    GoalCheck(**json.loads(message.content.parts[0].text)).satisfied                    
                )

            items_removed = 0
            for i, complete in enumerate(remove):
                if complete == True:
                    ctx.session.state["current_goals"].pop(i - items_removed)
                    items_removed += 1

            # --- Step 4: Factory ---
            if len(ctx.session.state["current_goals"]):
                events = [event async for event in task_factory.run_async(ctx)]
                new_tasks = NewTasks(**json.loads(events[-1].content.parts[0].text))
                existing = set(ctx.session.state["current_goals"])
                for task in new_tasks.added_tasks:
                    if task not in existing:
                        ctx.session.state["current_goals"].append(task)

        # --- Step 1: Doctor asks next question ---
        if ctx.session.state.get("current_goals"):
            t = time.time()
            last_doctor_text = ""
            async for event in doctor.run_async(ctx):
                yield event
                if event.author == "doctor" and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            last_doctor_text = part.text
            ctx.session.state["last_doctor_message"] = last_doctor_text
            ctx.session.state["awaiting_patient"] = True
        else:
            yield types.Content(
                role="model",
                parts=[types.Part(text="Anamnesis complete. All goals have been addressed.")],
            )
