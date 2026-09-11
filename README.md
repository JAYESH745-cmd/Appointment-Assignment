# Appointo

A lightweight Flask scheduling board for a small team. It uses SQLite locally and PostgreSQL in production.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Open `http://127.0.0.1:5000` in a browser.

## What it does

- Shows scheduled, completed, and cancelled appointments in one time-ordered board.
- Adds and edits appointments with required-field and time-order validation.
- Filters the board by a specific date and/or status.
- Completes or cancels scheduled appointments. Cancelled entries stay visible and are clearly labelled.
- Prevents overlapping active appointments on the same date, including overlaps that only partially intersect.
- Stores appointments persistently in SQLite locally or PostgreSQL when `DATABASE_URL` is configured.

## Deploy to Vercel with PostgreSQL

1. In the Vercel Marketplace, add the **Neon** integration to this project and create a PostgreSQL database. Vercel injects its pooled `DATABASE_URL` automatically.
2. In Vercel **Settings → Environment Variables**, add `APPOINTO_SECRET` with a long random value for Production and Preview.
3. Redeploy the `main` branch. Appointo creates its database table and sample records on its first connection.

For manual Neon setup, copy the Neon PostgreSQL connection string into a Vercel environment variable named `DATABASE_URL`, select Production and Preview, then redeploy. Never commit the database URL or secret to Git.

## Assumptions

- Times are local team times; no time-zone conversion is applied.
- An appointment’s end time is exclusive, so an appointment ending at 10:00 can be followed by one beginning at 10:00.
- Cancelled appointments no longer reserve their time slot, allowing a replacement to be booked. Completed appointments continue to reserve their historical slot.
- A completed or cancelled appointment remains editable for correcting its details, but its status cannot be changed again from the board.
- The PostgreSQL database is shared by the current application; account-level data separation requires a later authentication and `users` implementation.

## Test

```bash
python3 -m unittest discover -s tests -v
```
