from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntegrityFlag:
    """
    Один признак возможного списывания.
    """

    code: str
    title: str
    description: str
    weight: int


@dataclass
class IntegrityReport:
    """
    Отчёт о добросовестности прохождения теста.
    """

    score: int = 0
    risk_level: str = "low"
    flags: list[IntegrityFlag] = field(default_factory=list)

    def add_flag(self, flag: IntegrityFlag) -> None:
        """
        Добавляет признак и увеличивает риск.
        """

        self.flags.append(flag)
        self.score += flag.weight

    def calculate_risk_level(self) -> None:
        """
        Рассчитывает уровень риска.
        """

        if self.score >= 70:
            self.risk_level = "high"
            return

        if self.score >= 35:
            self.risk_level = "medium"
            return

        self.risk_level = "low"

    def as_dict(self) -> dict:
        """
        Возвращает отчёт в формате словаря.
        """

        return {
            "score": self.score,
            "risk_level": self.risk_level,
            "flags": [
                {
                    "code": flag.code,
                    "title": flag.title,
                    "description": flag.description,
                    "weight": flag.weight,
                }
                for flag in self.flags
            ],
        }
