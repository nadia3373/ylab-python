"""
У каждого фильма есть расписание, по каким дням он идёт в кинотеатрах.
Для эффективности дни проката хранятся периодами дат.
Например, прокат фильма проходит с 1 по 7 января,
а потом показ возобновляется с 15 января по 7 февраля:
Вам дан class Movie. Реализуйте у него метод schedule.
Он будет генерировать дни, в которые показывают фильм.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple


@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        delta = timedelta(days=1)
        for date in range(len(self.dates)):
            start = self.dates[date][0]
            end = self.dates[date][1]
            current = start
            while current <= end:
                yield current
                current += delta
        return []

m = Movie('sw', [
  (datetime(2020, 1, 1), datetime(2020, 1, 7)),
  (datetime(2020, 1, 15), datetime(2020, 2, 7))
])

for d in m.schedule():
    print(d)
