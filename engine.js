// Days Math engine - day counts, milestones, and sleeps, run exactly.
// Mirrored date-for-date by oracle.py; keep the calendar logic identical.

var _WDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var _MONTHS = ["January", "February", "March", "April", "May", "June", "July",
  "August", "September", "October", "November", "December"];

function _leap(y) {
  return y % 4 === 0 && (y % 100 !== 0 || y % 400 === 0);
}

function _dim(y, m) {
  if (m === 2) return _leap(y) ? 29 : 28;
  return [4, 6, 9, 11].indexOf(m) >= 0 ? 30 : 31;
}

// "1993-04-01" -> {y, m, d, days since epoch}; strict, no rollover.
function _parse(s) {
  var m = /^(\d{1,4})-(\d{1,2})-(\d{1,2})$/.exec(String(s).trim());
  if (!m) throw new Error(s + " is not a date");
  var y = +m[1], mo = +m[2], d = +m[3];
  if (y < 1 || mo < 1 || mo > 12 || d < 1 || d > _dim(y, mo)) {
    throw new Error(_MONTHS[mo - 1] ? _MONTHS[mo - 1] + " " + d + " is not a date" : s + " is not a date");
  }
  return { y: y, m: mo, d: d, days: Math.floor(Date.UTC(y, mo - 1, d) / 86400000) };
}

function _comma(n) {
  var s = String(n), out = "";
  while (s.length > 3) { out = "," + s.slice(-3) + out; s = s.slice(0, -3); }
  return s + out;
}

function _fmt(p) {
  return _WDAYS[new Date(Date.UTC(p.y, p.m - 1, p.d)).getUTCDay()] + ", " + _MONTHS[p.m - 1] + " " + p.d + ", " + p.y;
}

function _fromDays(days) {
  var t = new Date(days * 86400000);
  return { y: t.getUTCFullYear(), m: t.getUTCMonth() + 1, d: t.getUTCDate(), days: days };
}

// The alive truth: the count nobody tracks.
function daysAliveTruth(birth, today) {
  var b = _parse(birth), t = _parse(today);
  if (b.days >= t.days) throw new Error("birth date must be before today");
  var days = t.days - b.days;
  var weeks = Math.floor(days / 7), rem = days % 7;
  var wWord = _comma(weeks) + " week" + (weeks === 1 ? "" : "s");
  var tail = rem === 0 ? wWord + " exactly" :
    wWord + " and " + rem + " day" + (rem === 1 ? "" : "s");
  return _comma(days) + " days since " + _fmt(b) + " - " + tail + ".";
}

// The milestone truth: the round-number day is coming whether or not anyone plans for it.
function milestoneTruth(birth, today) {
  var b = _parse(birth), t = _parse(today);
  if (b.days >= t.days) throw new Error("birth date must be before today");
  var days = t.days - b.days;
  if (days % 1000 === 0) {
    return "Today is day " + _comma(days) + " - the party is now.";
  }
  var next = (Math.floor(days / 1000) + 1) * 1000;
  var when = _fromDays(b.days + next);
  var away = next - days;
  return "Day " + _comma(next) + " lands " + _fmt(when) + " - " + _comma(away) + " day" + (away === 1 ? "" : "s") + " away.";
}

// The sleeps truth: countdowns the way kids keep them.
function sleepsTruth(today, target) {
  var t = _parse(today), g = _parse(target);
  var n = g.days - t.days;
  if (n === 0) return "That is today - no sleeps at all.";
  if (n < 0) {
    var ago = -n;
    return _fmt(g) + " already passed - " + _comma(ago) + " sleep" + (ago === 1 ? "" : "s") + " ago.";
  }
  return n + " sleep" + (n === 1 ? "" : "s") + " until " + _fmt(g) + ".";
}
