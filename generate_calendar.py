import requests
import os
from datetime import datetime, timezone

# === CONFIGURATION ===
API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY")
CALENDAR_ID = "c94d7edb4a74b8d58f185ab4121d9fb35816ff03b2fb7226ca7209edf9b7dcdc@group.calendar.google.com"
OUTPUT_FILE = "phd_filtered_calendar.ics"

# Keywords to match course titles
KEYWORDS = [
    "Generative", "GANs", "Milani",
    "Visualization", "Ceccarello",
    "Deep", "Learning", "Pezze",
    "Mobile", "Communication", "Dini",
    "Biomedical", "Images", "Castellaro",
    "Automated", "Planning", "Orlandini"
]

# Words to exclude
EXCLUDE = ["Pillonetto", "Giordani", "Subhrakanti", "Nunzio"]

def fetch_events(query):
    """Fetch all events matching the query from the calendar."""
    url = (
        f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"
        f"?q={query}&singleEvents=true&orderBy=startTime&maxResults=2500&key={API_KEY}"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("items", [])

def should_exclude(event):
    """Return True if event should be excluded based on EXCLUDE words."""
    text = (
        (event.get("summary", "") or "") + " " +
        (event.get("description", "") or "") + " " +
        (event.get("location", "") or "")
    ).lower()
    return any(word.lower() in text for word in EXCLUDE)

# === FETCH AND FILTER EVENTS ===
seen = set()
filtered_events = []

for word in KEYWORDS:
    for event in fetch_events(word):
        if event["id"] not in seen and not should_exclude(event):
            seen.add(event["id"])
            filtered_events.append(event)

print(f"Found {len(filtered_events)} filtered events after excluding {EXCLUDE}.")

# === BUILD .ICS FILE ===
def format_dt(dt_str):
    """Convert ISO date/time to iCalendar format (UTC or date)."""
    if "T" in dt_str:
        # Parse the datetime with timezone info
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        # ✅ Convert to UTC before formatting
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y%m%dT%H%M%SZ")
    else:
        # All-day event (date only)
        return dt_str.replace("-", "")

ics_lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Filtered PhD Courses//EN"
]

for e in filtered_events:
    uid = e["id"]
    summary = e.get("summary", "No title").replace("\n", " ")
    description = e.get("description", "").replace("\n", " ")
    start = e["start"].get("dateTime", e["start"].get("date"))
    end = e["end"].get("dateTime", e["end"].get("date"))
    loc = e.get("location", "")
    
    ics_lines += [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:{description}",
        f"DTSTART:{format_dt(start)}",
        f"DTEND:{format_dt(end)}",
        f"LOCATION:{loc}",
        "END:VEVENT"
    ]

ics_lines.append("END:VCALENDAR")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(ics_lines))

print(f"✅ Saved {OUTPUT_FILE}")