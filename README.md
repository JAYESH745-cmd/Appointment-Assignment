# Appointo

A lightweight Flask and SQLite scheduling board for a small team. It ships with sample appointments so the interface is reviewable on first launch.

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
- Stores appointments in SQLite so changes remain after restarting the app.

## Assumptions

- Times are local team times; no time-zone conversion is applied.
- An appointment’s end time is exclusive, so an appointment ending at 10:00 can be followed by one beginning at 10:00.
- Cancelled appointments no longer reserve their time slot, allowing a replacement to be booked. Completed appointments continue to reserve their historical slot.
- A completed or cancelled appointment remains editable for correcting its details, but its status cannot be changed again from the board.

## Test

```bash
python3 -m unittest discover -s tests -v
```
