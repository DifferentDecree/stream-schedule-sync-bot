from PIL import Image, ImageDraw, ImageFont
import datetime
import pytz

class ScheduleFormatter:
    def __init__(self, timezone="UTC"):
        self.tz = pytz.timezone(timezone)

    def format_image(self, data, filename="calendar.png"):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        #Image settings
        cell_width = 200
        cell_height = 100
        header_height = 50
        padding = 10
        width = cell_width * 7
        max_rows = max(len(day) for day in self._prepare_data(data)) or 1
        height = header_height + (cell_height * max_rows)

        img = Image.new("RGB", (width, height), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        week = self._prepare_data(data)

        #Draw headers
        for i, day in enumerate(days):
            x0 = i * cell_width
            draw.rectangle([x0, 0, x0 + cell_width, header_height], fill=(80, 80, 160))
            w, h = draw.textsize(day, font=font)
            draw.text((x0 + (cell_width - w)//2, (header_height - h)//2), day, fill="white", font=font)

        #Draw events
        for i, day_events in enumerate(week):
            x0 = i * cell_width
            for j, event in enumerate(day_events):
                y0 = header_height + j * cell_height
                draw.rectangle([x0, y0, x0 + cell_width, y0 + cell_height], outline=(100,100,100))
                text = event["title"]
                if event["is_canceled"]:
                    text += " (Canceled)"
                draw.text((x0 + padding, y0 + padding), text, fill="white", font=font)
        img.save(filename)
        return filename

    def _prepare_data(self, data):
        """Organize events per weekday"""
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
            week[weekday].append({"title": segment["title"], "is_canceled": segment.get("is_canceled", False)})

        return week