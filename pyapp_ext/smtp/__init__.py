"""
pyApp SMTP Extension
~~~~~~~~~~~~~~~~~~~~

"""
from pyapp.app import CommandGroup, argument

from .client import *
from .factory import *


class Extension:
    """
    SMTP Extension
    """
    default_settings = ".default_settings"
    checks = ".checks"

    @staticmethod
    def register_commands(root: CommandGroup):
        group = root.create_command_group("smtp")

        @group.command
        @argument("TO", help_text="Message recipient")
        @argument("SUBJECT", help_text="Message subject")
        @argument("--from", dest="from_", help_text="Message sender")
        @argument("--body", help_text="Message body; defaults to 'Test Email'")
        @argument("--config", default="default", help_text="Email configuration to use.")
        def send(opts):
            """
            Send a test email
            """
            smtp_client = create_client(opts.config)
            smtp_client.send_plain(opts.TO, opts.SUBJECT, opts.body or "Test Email", from_=opts.from_)
