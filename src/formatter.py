import datetime
import pytz

class ScheduleFormatter:
    def __init__ (self, timezone):
        self.tz = pytz.timezone(timezone)

    def format_horizontal_grid(self, data):
        today = datetime.datetime.now(self.tz)
        end_week = today + datetime.timedelta(days=7)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        #Build per-day lists
        week = {i: [] for i in range(7)}
        for segment in data["data"]["segments"]:
            start = datetime.datetime.fromisoformat(
                segment["start_time"].replace("Z", "+00:00")
            ).astimezone(self.tz)
            if not (today <= start <= end_week):
                continue
            weekday = start.weekday()
            time_str = start.strftime("%I:%M %p").lstrip("0")
            entry = f"{time_str} {segment['title']}"
            if segment["is_canceled"]:
                entry = f"~~{entry}~~"
            week[weekday].append(entry)

        # Horizontal Grid
        max_rows = max(len(events) for events in week.values()) or 1
        lines = []

        # Header
        header = " | ".join([f"{d:^12}" for d in days])
        lines.append(header)
        lines.append("-"*len(header))

        # Rows
        for i in range(max_rows):
            row = []
            for j in range(7):
                events = week[j]
                row.append(f"{events[i]:12}" if i < len(events) else " " * 12)
            lines.append(" | ".join(row))

    return "```text\n" + "\n".join(lines) + "\n```"