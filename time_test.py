from time_utils import convert_relative_time
from datetime import datetime

samples = [
    "৭ মিনিট আগে",
    "১২ মিনিট আগে",
    "১৬ মিনিট আগে",
    "২৩ নভেম্বর ২০২৫, ০১:৩২ পিএম",
    "২৮ মিনিট আগে",
]

print('Now:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
for s in samples:
    print(s, '->', convert_relative_time(s))
