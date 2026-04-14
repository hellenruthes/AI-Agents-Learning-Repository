🛡️ Exercise: Guardrails for Safe Retrieval (Internal Notes Protection)
📌 Overview

In this exercise you will build an AI agent that retrieves information from the database (conversations and feedbacks) and applies guardrails to ensure that sensitive content is never exposed to the user.

The system contains a table called sensitive_items which represents internal data such as internal notes about users.

The goal is to ensure that:

The agent may access sensitive data internally but must never expose it in the final response.

🎯 Objective

Build an agent that:

retrieves relevant data from the database
filters sensitive or unsafe content
responds only with safe information
blocks attempts to access internal data
🧱 Available Data

Your database contains:

conversations — messages between users and support
feedbacks — user feedback
sensitive_items — internal data such as:
internal notes
negative descriptions about users
confidential content

Internal notes must never appear in the response.