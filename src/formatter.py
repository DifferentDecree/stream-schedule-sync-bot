from PIL import Image, ImageDraw, ImageFont
import datetime
import pytz
import os 

class ScheduleFormatter:
    def __init__(self, timezone="UTC"):
        self.tz = pytz.timezone(timezone)

        base_path = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        self.header_font_path = os.path.join(base_path, "Roboto-Bold.ttf")
        self.event_font_path = os.path.join(base_path, "Roboto-Regular.ttf")

        if not os.path.exists(self.header_font_path):
            self.header_font_path = None
        if not os.path.exists(self.event_font_path):
            self.event_font_path = None

    def format_image(self, data, filename="calendar.png"):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Image settings
        cell_width = 300
        cell_height = 120
        header_height = 80
        padding = 15

        # Prepare week data
        week = self._prepare_data(data)
        max_rows = max(len(day) for day in week) or 1
        width = cell_width * 7
        height = header_height + (cell_height * max_rows)

        img = Image.new("RGB", (width, height), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            header_font = ImageFont.truetype(self.header_font_path, 28) if self.header_font_path else ImageFont.load_default()
            event_font = ImageFont.truetype(self.event_font_path, 22) if self.event_font_path else ImageFont.load_default()
        except OSError:
            header_font = ImageFont.load_default()
            event_font = ImageFont.load_default()

        # Draw headers and vertical lines
        for i, day in enumerate(days):
            x0 = i * cell_width
            draw.rectangle([x0, 0, x0 + cell_width, header_height], fill=(80, 80, 160))
            bbox = header_font.getbbox(day)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            draw.text((x0 + (cell_width - w)//2, (header_height - h)//2), day, fill="white", font=header_font)
            draw.line([(x0, 0), (x0, height)], fill=(100, 100, 100), width=2)
        draw.line([(width-1, 0), (width-1, height)], fill=(100, 100, 100), width=2)
        draw.line([(0, header_height), (width, header_height)], fill=(100, 100, 100), width=2)

        # Draw events
        for col, day_events in enumerate(week):
            x0 = col * cell_width
            for row, event in enumerate(day_events):
                y0 = header_height + row * cell_height
                draw.rectangle([x0, y0, x0 + cell_width, y0 + cell_height], outline=(100, 100, 100))
                text = event["title"]
                if event["is_canceled"]:
                    text += " (Canceled)"
                draw.text((x0 + padding, y0 + padding), text, fill="white", font=event_font)

        img.save(filename)
        return filename

    def _prepare_data(self, data):
        """
        Organize events per weekday, include formatted time.
        Returns: list of 7 lists (Mon-Sun), each containing dicts with title and is_canceled
        """
        week = [[] for _ in range(7)]
        today = datetime.datetime.now(self.tz)
        end_week = today + datetime.timedelta(days=7)

        for segment in data["data"]["segments"]:
            start = datetime.datetime.fromisoformat(
                segment["start_time"].replace("Z", "+00:00")
            ).astimezone(self.tz)

            if not (today <= start <= end_week):
                continue

            weekday = start.weekday()
            time_str = start.strftime("%I:%M %p").lstrip("0")
            tz_str = start.tzname()
            title = f"{time_str} {tz_str} {segment['title']}"
            week[weekday].append({
                "title": title,
                "is_canceled": segment.get("is_canceled", False)
            })

        return week