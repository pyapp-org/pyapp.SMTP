from smtplib import SMTP, SMTP_SSL

from pyapp.conf.helpers import NamedFactory

__all__ = ("smtp_factory", "get_client")


class SMTPFactory(NamedFactory[SMTP]):
    """
    Factory for SMTP connections
    """

    required_keys = ("host",)
    optional_keys = ("port", "local_hostname", "timeout", "source_address")

    def create(self, name: str = None) -> SMTP:
        """
        Create an SMTP client instance
        """
        config = self.get(name)
        SMTP()

    def check_definition(self, config_defitions, name: str, **_):
        messages = super().check(config_defitions, name)

        # If there are any serious messages don't bother with connectivity check
        if any(m.is_serious() for m in messages):
            return messages

        try:
            client = self.create(name)
            client.helo()
        except Exception as ex:
            messages.append(
                Error(
                    "SMTP connection check failed",
                    f"Check connection parameters, exception raised: {ex}",
                    f"settings.{self.setting}[{name}]",
                )
            )

        return messages


smtp_factory = SMTPFactory("SMTP")
get_client = smtp_factory.create
