from datetime import datetime, timedelta
import re


def convert_relative_time(text, now=None):
    """Convert Bangla relative or absolute time strings to a standardized timestamp.

    Returns string in format YYYY-MM-DD HH:MM:SS on success; if parsing fails,
    returns the original text.
    """
    if not text:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if now is None:
        now = datetime.now()

    # Translate Bangla digits to western digits
    bn2en = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
    normalized = text.translate(bn2en)

    # Strip extra separators and surrounding whitespace
    normalized = normalized.strip()

    # Handle relative times like '৭ মিনিট আগে', '২ ঘন্টা আগে', '১ দিন আগে', '৩৫ সেকেন্ড আগে'
    rel_match = re.search(r"(\d+)\s*(সেকেন্ড|সেকেন্ডে|সেকেন্ডের|সেকেন্ডেরই|সেকেন্ডের?|'সেকেন্ড'|মিনিট|মিন|ঘন্টা|ঘণ্টা|ঘন্টা|দিন)\b", normalized)
    if rel_match:
        value = int(rel_match.group(1))
        unit = rel_match.group(2)

        if "সেক" in unit:
            dt = now - timedelta(seconds=value)
        elif "মিন" in unit:
            dt = now - timedelta(minutes=value)
        elif "ঘণ্ট" in unit or "ঘন্টা" in unit:
            dt = now - timedelta(hours=value)
        elif "দিন" in unit:
            dt = now - timedelta(days=value)
        else:
            dt = now

        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # Try to parse absolute Bangla date like: '২৩ নভেম্বর ২০২৫, ০১:৩২ পিএম' or '২৩ নভেম্বর ২০২৫ 01:32 PM'
    # Map common Bangla month names to month numbers
    months = {
        "জানুয়ারি": 1, "জানুয়ারি": 1, "ফেব্রুয়ারি": 2, "ফেব্রুয়ারি": 2,
        "মার্চ": 3, "এপ্রিল": 4, "মে": 5, "জুন": 6, "জুলাই": 7,
        "জুলাই": 7, "আগস্ট": 8, "অগাস্ট": 8, "সেপ্টেম্বর": 9, "অক্টোবর": 10,
        "নভেম্বর": 11, "ডিসেম্বর": 12
    }

    # Normalize AM/PM in Bangla
    normalized = normalized.replace("পিএম", "PM").replace("পূর্বাহ্ণ", "AM").replace("এএম", "AM").replace("এম", "PM")

    # Regex to capture day, month_name, year, optional time and am/pm
    abs_match = re.search(r"(\d{1,2})\s+([\w\u0980-\u09FF]+)\s+(\d{4})(?:[,\s]+(\d{1,2}:\d{2}))?(?:\s*(AM|PM))?", normalized, re.I)
    if abs_match:
        day = int(abs_match.group(1))
        month_name = abs_match.group(2)
        year = int(abs_match.group(3))
        time_part = abs_match.group(4)
        ampm = abs_match.group(5)

        month = months.get(month_name, None)
        if month is None:
            # try lowercase variant
            month = months.get(month_name.strip(), None)

        try:
            hour = 0
            minute = 0
            if time_part:
                hh, mm = time_part.split(":")
                hour = int(hh)
                minute = int(mm)
                if ampm:
                    ampm = ampm.upper()
                    if ampm == "PM" and hour < 12:
                        hour += 12
                    if ampm == "AM" and hour == 12:
                        hour = 0

            if month:
                dt = datetime(year, month, day, hour, minute)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

    # Fallback: if string already looks like an ISO datetime after digit translation
    iso_try = re.search(r"(\d{4}-\d{2}-\d{2})[T\s](\d{2}:\d{2}:?\d{0,2})", normalized)
    if iso_try:
        try:
            dt = datetime.fromisoformat(iso_try.group(0))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

    # Give up: return original text so caller can decide
    return text
