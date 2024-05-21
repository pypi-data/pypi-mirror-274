__import__('pkg_resources').declare_namespace(__name__)

from .api import SentrifyAI
from .exceptions import SentrifyAIError

__all__ = ['SentrifyAI', 'SentrifyAIError']