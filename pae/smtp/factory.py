import socket

from email.message import Message
from email.mime.text import MIMEText
from pyapp.conf.helpers import NamedFactory
from smtplib import SMTP, SMTP_SSL
from typing import Sequence

__all__ = ("factory", "create_client", "SMTPClient", "NotConnected")


class NotConnected(Exception):
    pass


class SMTPClient:
    """
    Wrapper around `smtplib.SMTP` to provide a simple API
    """

    def __init__(
        self,
        host: str,
        *,
        port: int = 0,
        local_hostname: str = None,
        timeout: int = socket._GLOBAL_DEFAULT_TIMEOUT,
        source_address: str = None,
        username: str = None,
        password: str = None,
        sender_addr: str = None,
    ):

        # SMTP client args
        self.host = host
        self.port = port
        self.local_hostname = local_hostname
        self.timeout = timeout
        self.source_address = source_address

        self.username = username
        self.password = password
        self.from_addr = from_addr

        self.smtp: SMTP = None

    def __enter__(self) -> "SMTPClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def connect(self):
        """
        Connect to SMTP server
        """
        if self.smtp is not None:
            return

        self.smtp = SMTP(
            self.host, self.port, self.local_hostname, self.timeout, self.source_address
        )
        if self.username:
            self.smtp.login(self.username, self.password)

    def quit(self):
        """
        Disconnect from SMTP server
        """
        if self.smtp is not None:
            self.smtp.quit()
            self.smtp = None

    def send_message(self, msg: Message):
        """
        Send an email message
        """
        if self.smtp is None:
            raise NotConnected("`connect` has not been called prior to `send_message`")

        self.smtp.send_message(msg)

    def send_plain(
        self,
        to_addrs: Sequence[str],
        subject: str,
        body: str,
        *,
        cc_addrs: Sequence[str] = None,
        bcc_addrs: Sequence[str] = None,
        from_addr: str = None,
    ):
        """
        Send a plain text basic email message.
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr or self.from_addr
        msg["To"] = ", ".join(to_addrs)

        if cc_addrs:
            msg["CC"] = ", ".join(cc_addrs)

        if bcc_addrs:
            msg["BCC"] = ", ".join(bcc_addrs)

        self.send_message(msg)


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
