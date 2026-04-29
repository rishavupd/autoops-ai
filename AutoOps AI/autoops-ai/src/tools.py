import os
import json
from datetime import datetime
import pandas as pd


def calculate_overdue_days(due_date, today: str) -> int:
    """
    Handles both string and Timestamp safely
    """

    current = datetime.strptime(today, "%Y-%m-%d")

    if isinstance(due_date, pd.Timestamp):
        due = due_date.to_pydatetime()
    else:
        due = datetime.strptime(str(due_date), "%Y-%m-%d")

    return max((current - due).days, 0)

def detect_unpaid_invoices(df: pd.DataFrame, today: str) -> list[dict]:
    """
    Tool used by Monitoring Agent.
    Detects unpaid overdue invoices.
    """
    issues = []

    for _, row in df.iterrows():
        if str(row["status"]).lower() == "unpaid":
            overdue_days = calculate_overdue_days(row["due_date"], today)

            if overdue_days > 0:
                issues.append(
                    {
                        "invoice_id": row["invoice_id"],
                        "customer_name": row["customer_name"],
                        "customer_email": row["customer_email"],
                        "amount": float(row["amount"]),
                        "due_date": str(row["due_date"].date()),
                        "overdue_days": overdue_days,
                        "last_reminder_sent": (
                            None
                            if pd.isna(row["last_reminder_sent"])
                            else str(row["last_reminder_sent"].date())
                        ),
                        "priority": row["priority"],
                    }
                )

    return issues


def save_json(data: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def simulate_email_send(customer_email: str, subject: str, body: str) -> dict:
    """
    Demo-safe action tool.
    It does not actually send email.
    It simulates action execution.
    """
    return {
        "sent": True,
        "to": customer_email,
        "subject": subject,
        "body": body,
        "message": "Email simulated successfully.",
    }


def verify_action(issue: dict, action_result: dict) -> dict:
    """
    Reflection / verification tool.
    Checks whether action was executed.
    """
    if not action_result.get("sent"):
        return {
            "resolved": False,
            "reason": "Email action failed.",
            "next_step": "Retry or escalate to finance manager.",
        }

    if issue["overdue_days"] > 45:
        return {
            "resolved": False,
            "reason": "Invoice is highly overdue. Reminder alone may not be enough.",
            "next_step": "Escalate to finance manager.",
        }

    return {
        "resolved": True,
        "reason": "Reminder action completed.",
        "next_step": "Wait for customer response.",
    }