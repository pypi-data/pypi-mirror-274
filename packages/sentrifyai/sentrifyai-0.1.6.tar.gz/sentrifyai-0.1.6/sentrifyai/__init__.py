__import__('pkg_resources').declare_namespace(__name__)

from .api import Moderation
from .api import Emotions
from .exceptions import SentrifyAIError

__all__ = ['Moderation', 'Emotions', 'SentrifyAIError']