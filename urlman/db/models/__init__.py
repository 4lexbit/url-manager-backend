import pkgutil
from pathlib import Path

from urlman.db.models.urls import UrlModel
from urlman.db.models.user import UserModel


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="urlman.db.models.",
    )
    for module in modules:
        __import__(module.name)


__all__ = [
    "UrlModel",
    "UserModel",
    "load_all_models",
]
