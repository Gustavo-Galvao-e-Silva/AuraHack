from google.adk.agents import LlmAgent
from schemas import *
from prompts import load_prompt, Prompt

CHECKER_POOL_SIZE = 4

doctor = LlmAgent(
    name="doctor",
    model="gemini-2.5-flash",
    instruction=load_prompt(Prompt.Doctor),
)

summarizer = LlmAgent(
    name="summarizer",
    model="gemini-2.5-flash",
    instruction=load_prompt(Prompt.Summarizer),
    output_schema=PatientSummary,
)

checker_agent = LlmAgent(
    name="checker",
    model="gemini-2.5-flash",
    instruction=load_prompt(Prompt.Checker),
    output_schema=GoalCheck,
)

# Pool of checker agents for parallel goal checking
checker_pool: list[LlmAgent] = [checker_agent] + [
    LlmAgent(
        name=f"checker_{i}",
        model="gemini-2.5-flash",
        instruction=load_prompt(Prompt.Checker),
        output_schema=GoalCheck,
    )
    for i in range(1, CHECKER_POOL_SIZE)
]

task_factory = LlmAgent(
    name="factory",
    model="gemini-2.5-flash",
    instruction=load_prompt(Prompt.Factory),
    output_schema=NewTasks,
)

report_agent = LlmAgent(
    name="report_agent",
    model="gemini-2.5-flash",
    instruction=load_prompt(Prompt.Report),
    output_schema=MedicalReport,
)

pdf_report_agent = LlmAgent(
    name="pdf_report_agent",
    model="gemini-2.5-flash",
    instruction=load_prompt(Prompt.PdfReport),
    output_schema=MedicalReport,
)
