from PIL import Image, ImageDraw, ImageFont
import datetime
import pytz
import os
import textwrap  # for wrapping long text

class ScheduleFormatter:
    def __init__(self, timezone="UTC"):
        self.tz = pytz.timezone(timezone)

        # Font paths
        base_path = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        self.header_font_path = os.path.join(base_path, "Roboto-Bold.ttf")
        self.event_font_path = os.path.join(base_path, "Roboto-Regular.ttf")

        # Fallback if fonts not found
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
        padding = 10

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

        # Draw events with wrapping
        for col, day_events in enumerate(week):
            x0 = col * cell_width
            for row, event in enumerate(day_events):
                y0 = header_height + row * cell_height
                draw.rectangle([x0, y0, x0 + cell_width, y0 + cell_height], outline=(100, 100, 100))

                text = event["title"]

                # Wrap text to fit cell width
                max_width = cell_width - 2 * padding
                wrapped_lines = self.wrap_text(text, event_font, max_width, draw)

                line_offset = 0

                if event["is_canceled"]:
                    cancel_text = "CANCELED"
                    cancel_bbox = draw.textbbox((0, 0), cancel_text, font=header_font)
                    cancel_w = cancel_bbox[2] - cancel_bbox[0]

                    cancel_x = x0 + (cell_width - cancel_w) // 2
                    cancel_y = y0 + padding

                    draw.text((cancel_x, cancel_y), cancel_text, fill=(255, 80, 80), font=header_font)

                    line_offset = event_font.size + 10

                # Draw wrapped lines
                for i, line in enumerate(wrapped_lines):
                    line_x = x0 + padding
                    line_y = y0 + padding + line_offset + i * (event_font.size + 2)

                    text_color = (255, 120, 120) if event["is_canceled"] else "white"

                    draw.text((line_x, line_y), line, fill=text_color, font=event_font)

                    if event["is_canceled"]:
                        bbox = draw.textbbox((line_x, line_y), line, font=event_font)
                        y_middle = (bbox[1] + bbox[3]) // 2

                        draw.line(
                            [(bbox[0], y_middle), (bbox[2], y_middle)],
                            fill=(255, 80, 80),
                            width=3
                        )

        img.save(filename)
        return filename

    def wrap_text(self, text, font, max_width, draw):
        """Wrap text to fit within max_width pixels"""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0,0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

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

            is_canceled = (
            segment.get("canceled_until") is not None
            )

            week[weekday].append({
                "title": title,
                "is_canceled": is_canceled
            })

        return week