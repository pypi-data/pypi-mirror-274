from .version import __version__


class VersionUtil:
    """
    A utility class to get the version of the library.
    """

    @staticmethod
    def get_version():
        """
        Get the current version of the library.

        Returns:
            str: The current version of the library.
        """
        return __version__
