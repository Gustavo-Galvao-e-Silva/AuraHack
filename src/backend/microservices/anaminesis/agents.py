from google.adk.agents import LlmAgent
from schemas import *
from prompts import load_prompt, Prompt

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
