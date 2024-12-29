from enum import StrEnum


class TaskDifficultyType(StrEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    VERY_HARD = "Very Hard"
    IMPOSSIBLE = "Impossible"
    GODLIKE = "Godlike"


TASK_DIFFICULTIES = {
    TaskDifficultyType.EASY: 5,
    TaskDifficultyType.MEDIUM: 10,
    TaskDifficultyType.HARD: 15,
    TaskDifficultyType.VERY_HARD: 20,
    TaskDifficultyType.IMPOSSIBLE: 25,
    TaskDifficultyType.GODLIKE: 30,
}
