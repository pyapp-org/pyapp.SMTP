import socket

from email.message import Message
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Sequence, Optional, Union, Dict

__all__ = ("SMTPClient", "NotConnected")


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
        from_addr: str = None,
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

        self.smtp: Optional[SMTP] = None

    def __enter__(self) -> "SMTPClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def connect(self):
        """
        Connect to SMTP server
        """
        if self.smtp is None:
            self.smtp = SMTP(
                self.host,
                self.port,
                self.local_hostname,
                self.timeout,
                self.source_address,
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

    def send_message(self, msg: Message) -> Dict[str, Sequence]:
        """
        Send an email message

        :returns: List of failed recipients (unless all failed) and the reason

        """
        if self.smtp is None:
            raise NotConnected("`connect` has not been called prior to `send_message`")

        return self.smtp.send_message(msg)

    def send_plain(
        self,
        to: Union[str, Sequence[str]],
        subject: str,
        body: str,
        *,
        cc: Union[str, Sequence[str]] = None,
        bcc: Union[str, Sequence[str]] = None,
        from_: str = None,
    ) -> Dict[str, Sequence]:
        """
        Send a plain text basic email message.
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_ or self.from_addr
        msg["To"] = to if isinstance(to, str) else ", ".join(to)

        if cc:
            msg["CC"] = cc if isinstance(cc, str) else ", ".join(cc)

        if bcc:
            msg["BCC"] = bcc if isinstance(bcc, str) else ", ".join(bcc)

        return self.send_message(msg)
