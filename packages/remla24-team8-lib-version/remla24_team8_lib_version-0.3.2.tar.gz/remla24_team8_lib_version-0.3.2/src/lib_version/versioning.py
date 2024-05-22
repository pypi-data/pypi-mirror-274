from importlib.metadata import version, PackageNotFoundError


class VersionUtil:
    """
    Utility class for handling version information of the
    remla24-team8-lib-version package.
    """
    @staticmethod
    def get_version():
        """Retrieve the current version of the remla24-team8-lib-version package.

        Returns:
            str: The version of the remla24-team8-lib-version package if found,
            otherwise returns 'Package not found'.
        """
        package_name = "remla24-team8-lib-version"
        try:
            return version(package_name)
        except PackageNotFoundError:
            return "Package not found"
