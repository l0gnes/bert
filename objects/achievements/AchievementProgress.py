class AchievementProgress(object):

    def __init__(self, progress : int, requirement : int) -> None:
        self.progress = progress
        self.requirement = requirement

    @property
    def ratio(self) -> float:
        return self.progress / self.requirement

    @property
    def is_completed(self) -> bool:
        return self.progress >= self.requirement