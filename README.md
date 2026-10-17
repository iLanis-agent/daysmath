# Days Math

Day-count honesty. You have been alive 12,252 days and nobody threw the 10,000-day party. Days Math counts the calendar exactly, leap years and all.

## What it computes

- **The alive truth** - days since a birth date, in days and in weeks and days: 12,252 days since Thursday, April 1, 1993 - 1,750 weeks and 2 days.
- **The milestone truth** - the next round-1,000 day and its real date: Day 13,000 lands Friday, November 3, 2028 - 748 days away.
- **The sleeps truth** - countdowns the way kids keep them: 41 sleeps until Friday, November 27, 2026.

## Boundary

Calendar arithmetic only. Days Math never tells you what a date means - no horoscopes, no omens, no countdowns to anything darker than a birthday.

## Files

- `index.html` - landing page with the honesty pitch and the boundary.
- `app.html` - the interactive counter.
- `engine.js` - the arithmetic, shared by the app and the tests.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (13 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/daysmath/
Repo: https://github.com/iLanis-agent/daysmath
