class SplashDil:
    """ It is used as a splash screen while loading/executing something.
    :param SpinnerWidget spinner: Stores the spinner widget.
    :param QLabel text: Stores a QLabel widget that shows text while something is loading.
    :param QPushButton cancel: Stores the 'Cancel' button (QPushButton)"""
    text = None
    spinner = None
    cancel = None

    def show(self):
        """Use it to show this."""
