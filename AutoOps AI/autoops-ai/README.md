# AutoOps AI - Autonomous Business Operations Agent

AutoOps AI is a multi-agent AI system that autonomously monitors invoice data, detects overdue unpaid invoices, decides the correct action, generates follow-up emails, simulates execution, verifies outcomes, and re-plans when needed.

## Problem

Small and medium businesses often lose revenue because invoice follow-ups are manual, delayed, or inconsistent.

## Solution

AutoOps AI acts like an AI Operations Manager.

Workflow:

Monitor → Detect → Decide → Act → Verify → Re-plan

## Why This Is Agentic AI

This is not a simple chatbot or fixed automation.

The system uses multiple agents:

1. Supervisor Agent - plans the workflow
2. Monitoring Agent - detects business issues
3. Decision Agent - chooses the best action
4. Action Agent - generates and executes action
5. Reflection Agent - verifies outcome and suggests next step

## Tech Stack

- Python
- OpenAI API
- GPT-4.1-mini
- Pandas
- Rich

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
