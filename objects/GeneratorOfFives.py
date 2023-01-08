from random import randint

__all__ = ["GeneratorOfFives"]

class GeneratorOfFives(object):

    @staticmethod
    def generate(min : int, max : int) -> int:
        """Generates a number that is a multiple of 5 between min and max"""
        real_max = max // 5
        real_min = min // 5

        return randint(real_min, real_max) * 5

    @staticmethod
    def translate(n : int) -> int:
        """Rounds n to the nearest 5"""
        return round(n / 5) * 5