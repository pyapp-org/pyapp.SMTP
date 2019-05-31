from pyapp.conf.helpers import NamedFactory
from pyapp.checks.message import CheckMessage
from typing import Union, Iterable, Dict, Any

from .client import SMTPClient

__all__ = ("factory", "create_client")


class SMTPFactory(NamedFactory[SMTPClient]):
    """
    Factory for SMTP connections
    """

    required_keys = ("host",)
    optional_keys = (
        "port",
        "local_hostname",
        "timeout",
        "source_address",
        "username",
        "password",
        "from_addr",
    )

    def create(self, name: str = None) -> SMTPClient:
        """
        Create an SMTP client instance
        """
        config = self.get(name)
        return SMTPClient(**config)

    def check_definition(
        self, config_defitions: Dict[str, Any], name: str, **_
    ) -> Union[CheckMessage, Iterable[CheckMessage]]:
        messages = super().check(config_defitions, name)

        # If there are any serious messages don't bother with connectivity check
        if any(m.is_serious() for m in messages):
            return messages

        try:
            client = self.create(name)
            client.connect()
            client.quit()
        except Exception as ex:
            messages.append(
                Error(
                    "SMTP connection check failed",
                    f"Check connection parameters, exception raised: {ex}",
                    f"settings.{self.setting}[{name}]",
                )
            )

        return messages


factory = SMTPFactory("SMTP")
create_client = smtp_factory.create
