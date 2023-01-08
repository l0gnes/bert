class ASCIIProgressBar(object):

    full    : str = "■"
    empty   : str = "□"
    format  : str = "[%s]"
    length  : int = 20

    @staticmethod
    def bar(progress : float) -> str:

        full_bars = int(progress * ASCIIProgressBar.length) # drops decimal
        empty_bars = ASCIIProgressBar.length - full_bars

        return ASCIIProgressBar.format % (
            (ASCIIProgressBar.full * full_bars) + (ASCIIProgressBar.empty * empty_bars)
        )
