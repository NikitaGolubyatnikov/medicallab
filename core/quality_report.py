from statistics import mean, pstdev
from typing import List, Tuple

class QualityStats:
    def __init__(self, results: List[float]):
        self.results = results
        self.avg = mean(results)
        self.stddev = pstdev(results) if len(results) > 1 else 0.0

    def get_limits(self) -> List[Tuple[str, float]]:
        return [
            ("-3S", self.avg - 3 * self.stddev),
            ("-2S", self.avg - 2 * self.stddev),
            ("-1S", self.avg - 1 * self.stddev),
            ("Среднее", self.avg),
            ("+1S", self.avg + 1 * self.stddev),
            ("+2S", self.avg + 2 * self.stddev),
            ("+3S", self.avg + 3 * self.stddev),
        ]

    def get_cv(self) -> float:
        return (self.stddev / self.avg) * 100 if self.avg != 0 else 0.0