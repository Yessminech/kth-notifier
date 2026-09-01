# KTH Thesis Notifier

A bot that checks KTH's CS thesis listings once a day and sends a notification when new
positions appear. Written because refreshing the page manually was a bad use of a semester
abroad.

## How it works

`bot.py` scrapes the thesis listings, compares them against the previously seen set, and
notifies on anything new. It runs on a daily schedule — no manual triggering.

## Stack

Python · Docker · GitHub Actions · deployed on Render

- `Dockerfile` — containerised so it runs the same locally and on the host
- `.github/workflows/` — CI on push
- `render.yaml` — infrastructure-as-code for the Render deployment

## Running it locally

```bash
pip install -r requirements.txt
python bot.py
```

Or with Docker:

```bash
docker build -t kth-notifier .
docker run --rm kth-notifier
```

## Configuration

Credentials and the notification target are read from environment variables — see `bot.py` for
the expected names. Nothing secret is committed.
