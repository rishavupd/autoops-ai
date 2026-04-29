from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import DATA_PATH, OUTPUT_DIR, TODAY
from data_loader import load_invoice_data
from tools import (
    detect_unpaid_invoices,
    simulate_email_send,
    verify_action,
    save_json,
)
from agents import (
    SupervisorAgent,
    MonitoringAgent,
    DecisionAgent,
    ActionAgent,
    ReflectionAgent,
)


console = Console()


def display_issues(issues: list[dict]) -> None:
    table = Table(title="Detected Unpaid Overdue Invoices")

    table.add_column("Invoice ID")
    table.add_column("Customer")
    table.add_column("Amount")
    table.add_column("Overdue Days")
    table.add_column("Priority")

    for issue in issues:
        table.add_row(
            issue["invoice_id"],
            issue["customer_name"],
            str(issue["amount"]),
            str(issue["overdue_days"]),
            issue["priority"],
        )

    console.print(table)


def run_autoops_agent() -> None:
    console.print(Panel.fit("AutoOps AI - Autonomous Invoice Operations Agent"))

    goal = """
Autonomously monitor unpaid invoices, detect overdue cases,
decide the correct follow-up action, execute the action,
verify the result, and re-plan if needed.
"""

    supervisor = SupervisorAgent()
    monitoring_agent = MonitoringAgent()
    decision_agent = DecisionAgent()
    action_agent = ActionAgent()
    reflection_agent = ReflectionAgent()

    console.print("\n[bold cyan]Step 1: Supervisor Agent planning workflow...[/bold cyan]")
    plan = supervisor.plan(goal)
    console.print(Panel(plan, title="Supervisor Plan"))

    console.print("\n[bold cyan]Step 2: Loading invoice data...[/bold cyan]")
    df = load_invoice_data(DATA_PATH)

    console.print("\n[bold cyan]Step 3: Monitoring Agent detecting issues...[/bold cyan]")
    issues = detect_unpaid_invoices(df, TODAY)

    if not issues:
        console.print("[green]No overdue unpaid invoices found.[/green]")
        return

    display_issues(issues)

    issue_summary = monitoring_agent.summarize_issues(issues)
    console.print(Panel(issue_summary, title="Monitoring Agent Summary"))

    final_results = []

    console.print("\n[bold cyan]Step 4: Autonomous decision-action-verification loop...[/bold cyan]")

    for issue in issues:
        console.print(Panel.fit(f"Processing {issue['invoice_id']} - {issue['customer_name']}"))

        decision = decision_agent.decide_action(issue)
        console.print(Panel(decision, title="Decision Agent"))

        email = action_agent.generate_email(issue, decision)
        console.print(Panel(email["body"], title=email["subject"]))

        action_result = simulate_email_send(
            customer_email=issue["customer_email"],
            subject=email["subject"],
            body=email["body"],
        )

        verification = verify_action(issue, action_result)

        reflection = reflection_agent.review(
            issue=issue,
            decision=decision,
            action_result=action_result,
            verification=verification,
        )

        console.print(Panel(str(verification), title="Verification Result"))
        console.print(Panel(reflection, title="Reflection Agent"))

        final_results.append(
            {
                "issue": issue,
                "decision": decision,
                "email": email,
                "action_result": action_result,
                "verification": verification,
                "reflection": reflection,
            }
        )

    output = {
        "project": "AutoOps AI",
        "date": TODAY,
        "goal": goal,
        "supervisor_plan": plan,
        "monitoring_summary": issue_summary,
        "results": final_results,
    }

    save_json(output, f"{OUTPUT_DIR}/autoops_run_result.json")

    console.print(
        Panel.fit(
            "Autonomous run completed. Output saved to outputs/autoops_run_result.json",
            title="Done",
        )
    )


if __name__ == "__main__":
    run_autoops_agent()