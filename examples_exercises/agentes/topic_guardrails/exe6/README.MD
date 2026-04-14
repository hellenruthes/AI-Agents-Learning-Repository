Objective

Create a guardrail mechanism that validates an internal note before saving it to the database.

The system must prevent notes containing:

PII
negative or pejorative language about the user

from being saved normally.

What you should build

You should create a solution with the following components:

1. Database table

It is already included in init.sql. If needed run:

docker compose down
docker compose up -d

Run load_data.py again to reload the data.

2. Validation function

Create a function that receives the note text and checks whether it contains:

PII

Examples:

email
phone number
CPF or another numeric identifier
Negative content

Examples:

difficult user
rude
hostile
aggressive
manipulative
3. Decision rule

When attempting to save a note the system must choose one of these behaviors:

Minimum required option
saved
blocked
Improved option
saved
sanitized_and_saved
blocked
Expected rules
Case 1 — Safe note

Input:

Customer reported login failure after password reset.

Expected result:

saved
Case 2 — Note with negative judgment

Input:

This is a difficult user and complains frequently.

Expected result:

blocked

or if sanitization is implemented:

sanitized_and_saved
Case 3 — Note with PII

Input:

Customer email is joao.silva@email.com and asked for an update.

Expected result:

blocked

or:

sanitized_and_saved
Case 4 — Note with two problems

Input:

This rude customer called again. Phone: 41999998888

Expected result:

the system must detect PII
the system must detect inappropriate language
the note must not be saved as if it were valid