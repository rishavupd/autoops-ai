"""from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)"""


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Mock LLM (no API required)
    """

    # Supervisor Agent
    if "Supervisor" in system_prompt:
        return "Plan: Monitor invoices → detect overdue → decide action → send reminder → verify → repeat."

    # Monitoring Agent
    if "Monitoring" in system_prompt:
        return "Detected multiple overdue invoices. High priority customers need immediate action."

    # Decision Agent
    if "Decision" in system_prompt:
        if "overdue_days': 60" in user_prompt or "overdue_days': 70" in user_prompt:
            return "Decision: Escalate to finance manager\nReason: Highly overdue\nUrgency: High"
        return "Decision: Send reminder email\nReason: Overdue payment\nUrgency: Medium"

    # Action Agent
    if "Action Agent" in system_prompt:
        return """Subject: Payment Reminder

Body:
Dear Customer,
Your invoice is overdue. Kindly make the payment at the earliest.
Thank you."""

    # Reflection Agent
    if "Reflection" in system_prompt:
        return "Action completed successfully. No further action required."

    return "Default response"
class SupervisorAgent:
    def plan(self, goal: str) -> str:
        system_prompt = """
You are the Supervisor Agent of an autonomous business operations system.
Your job is to create a clear workflow plan.
You must think like an operations manager.
Keep output practical and short.
"""

        user_prompt = f"""
Goal:
{goal}

Create a step-by-step plan for autonomous invoice operations.
"""

        return call_llm(system_prompt, user_prompt)


class MonitoringAgent:
    def summarize_issues(self, issues: list[dict]) -> str:
        system_prompt = """
You are the Monitoring Agent.
You inspect invoice issues and summarize what needs attention.
Do not make final decisions. Only report observations.
"""

        user_prompt = f"""
Detected overdue unpaid invoices:

{issues}

Summarize the operational issues.
"""

        return call_llm(system_prompt, user_prompt)


class DecisionAgent:
    def decide_action(self, issue: dict) -> str:
        system_prompt = """
You are the Decision Agent.
You decide the best business action for an overdue invoice.

Decision options:
1. Send polite reminder
2. Send urgent reminder
3. Escalate to finance manager
4. No action

Return:
- decision
- reason
- urgency level
"""

        user_prompt = f"""
Invoice issue:

{issue}

Decide the best next action.
"""

        return call_llm(system_prompt, user_prompt)


class ActionAgent:
    def generate_email(self, issue: dict, decision: str) -> dict:
        system_prompt = """
You are the Action Agent.
Generate a professional payment follow-up email.

Return only this format:

Subject: <subject>

Body:
<body>
"""

        user_prompt = f"""
Invoice issue:
{issue}

Decision:
{decision}

Generate the email.
"""

        email_text = call_llm(system_prompt, user_prompt)

        subject = "Payment Reminder"
        body = email_text

        if "Subject:" in email_text and "Body:" in email_text:
            subject_part = email_text.split("Body:")[0]
            body_part = email_text.split("Body:")[1]

            subject = subject_part.replace("Subject:", "").strip()
            body = body_part.strip()

        return {
            "subject": subject,
            "body": body,
        }


class ReflectionAgent:
    def review(self, issue: dict, decision: str, action_result: dict, verification: dict) -> str:
        system_prompt = """
You are the Reflection Agent.
You check if the autonomous workflow succeeded.
If not, suggest the next autonomous step.
Be honest and practical.
"""

        user_prompt = f"""
Invoice issue:
{issue}

Decision:
{decision}

Action result:
{action_result}

Verification:
{verification}

Review the outcome and suggest if re-planning is needed.
"""

        return call_llm(system_prompt, user_prompt)