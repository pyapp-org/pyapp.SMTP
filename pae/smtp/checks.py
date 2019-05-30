from pyapp.checks.registry import register
from .factory import smtp_factory

register(smtp_factory)

