#!/usr/bin/env python3
# Days Math oracle - mirrors engine.js date-for-date.
import json, re
from datetime import date, timedelta

_WDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]
_EPOCH_ORDINAL = date(1970, 1, 1).toordinal()

def _leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

def _dim(y, m):
    if m == 2:
        return 29 if _leap(y) else 28
    return 30 if m in (4, 6, 9, 11) else 31

def _parse(s):
    m = re.match(r"^(\d{1,4})-(\d{1,2})-(\d{1,2})$", str(s).strip())
    if not m:
        raise ValueError(f"{s} is not a date")
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if y < 1 or mo < 1 or mo > 12 or d < 1 or d > _dim(y, mo):
        raise ValueError(f"{_MONTHS[mo - 1]} {d} is not a date" if 1 <= mo <= 12 else f"{s} is not a date")
    return {"y": y, "m": mo, "d": d, "days": date(y, mo, d).toordinal() - _EPOCH_ORDINAL}

def _comma(n):
    return f"{n:,}"

def _fmt(p):
    dt = date(p["y"], p["m"], p["d"])
    return f"{_WDAYS[dt.weekday()]}, {_MONTHS[p['m'] - 1]} {p['d']}, {p['y']}"

def _from_days(days):
    dt = date(1970, 1, 1) + timedelta(days=days)
    return {"y": dt.year, "m": dt.month, "d": dt.day, "days": days}

def days_alive_truth(birth, today):
    b, t = _parse(birth), _parse(today)
    if b["days"] >= t["days"]:
        raise ValueError("birth date must be before today")
    days = t["days"] - b["days"]
    weeks, rem = divmod(days, 7)
    w_word = f"{_comma(weeks)} week" + ("" if weeks == 1 else "s")
    tail = f"{w_word} exactly" if rem == 0 else \
        f"{w_word} and {rem} day" + ("" if rem == 1 else "s")
    return f"{_comma(days)} days since {_fmt(b)} - {tail}."

def milestone_truth(birth, today):
    b, t = _parse(birth), _parse(today)
    if b["days"] >= t["days"]:
        raise ValueError("birth date must be before today")
    days = t["days"] - b["days"]
    if days % 1000 == 0:
        return f"Today is day {_comma(days)} - the party is now."
    nxt = (days // 1000 + 1) * 1000
    when = _from_days(b["days"] + nxt)
    away = nxt - days
    return f"Day {_comma(nxt)} lands {_fmt(when)} - {_comma(away)} day" + ("" if away == 1 else "s") + " away."

def sleeps_truth(today, target):
    t, g = _parse(today), _parse(target)
    n = g["days"] - t["days"]
    if n == 0:
        return "That is today - no sleeps at all."
    if n < 0:
        ago = -n
        return f"{_fmt(g)} already passed - {_comma(ago)} sleep" + ("" if ago == 1 else "s") + " ago."
    return f"{n} sleep" + ("" if n == 1 else "s") + f" until {_fmt(g)}."

CASES = [
    ("daysAliveTruth", ("1993-04-01", "2026-10-17")),
    ("daysAliveTruth", ("2000-02-29", "2026-10-17")),
    ("daysAliveTruth", ("2026-10-10", "2026-10-17")),
    ("milestoneTruth", ("1993-04-01", "2026-10-17")),
    ("milestoneTruth", ("1999-07-06", "2026-10-17")),
    ("sleepsTruth", ("2026-10-17", "2026-11-27")),
    ("sleepsTruth", ("2026-10-17", "2026-10-18")),
    ("sleepsTruth", ("2026-10-17", "2026-10-17")),
    ("sleepsTruth", ("2026-10-17", "2026-10-10")),
    ("daysAliveTruth", ("2027-01-01", "2026-10-17")),
    ("daysAliveTruth", ("2001-02-30", "2026-10-17")),
    ("sleepsTruth", ("2026-10-17", "November 27")),
    ("sleepsTruth", ("2026-10-17", "2027-12-25")),
]

FNS = {"daysAliveTruth": days_alive_truth, "milestoneTruth": milestone_truth, "sleepsTruth": sleeps_truth}

out = []
for name, args in CASES:
    try:
        expected = FNS[name](*args)
    except ValueError as e:
        expected = "ERR:" + str(e)
    out.append({"fn": name, "args": list(args), "expected": expected})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
