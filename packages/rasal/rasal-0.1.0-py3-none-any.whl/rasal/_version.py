import logging
import importlib.metadata



LOGGER = logging.getLogger(__name__)

package_name = "rasal"

# try:
__version__ = importlib.metadata.version(package_name)

# except pkg_resources.DistributionNotFound:
#     LOGGER.warning("Failed to find distribution of package %s.", package_name)
#     __version__ = "unknown"

__all__ = (
    "__version__",
)
