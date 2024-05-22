"""Tests for importing the package."""

import importlib
import pkgutil


def test_import_rasal():
    """Test import of whole rasal package.

    Walks the package and imports each submodule.
    """
    package_name = "rasal"
    package = importlib.import_module(package_name)
    for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        importlib.import_module(name)
