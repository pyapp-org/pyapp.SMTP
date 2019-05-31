from typing import Any, Dict

import mock
import pytest

from pae.smtp import client


class TestSMTPClient:
    @pytest.fixture
    def mock_smtp(self, monkeypatch):
        mock_smtp = mock.Mock()
        monkeypatch.setattr(client, "SMTP", mock_smtp)
        return mock_smtp

    def test_context_manager(self, mock_smtp: mock.Mock):
        target = client.SMTPClient("localhost")

        with target:
            assert target.smtp is mock_smtp.return_value
            mock_smtp.assert_called_once_with(
                "localhost", 0, None, client.socket._GLOBAL_DEFAULT_TIMEOUT, None
            )

        assert target.smtp is None

    def test_connect(self, mock_smtp: mock.Mock):
        target = client.SMTPClient("localhost", port=25, timeout=50)

        target.connect()
        assert target.smtp is mock_smtp.return_value
        mock_smtp.assert_called_with("localhost", 25, None, 50, None)

    def test_connect__with_credentials(self, mock_smtp: mock.Mock):
        target = client.SMTPClient("localhost", username="foo", password="bar")

        target.connect()
        assert target.smtp is mock_smtp.return_value
        mock_smtp.assert_called_with(
            "localhost", 0, None, client.socket._GLOBAL_DEFAULT_TIMEOUT, None
        )
        target.smtp.login.assert_called_with("foo", "bar")

    def test_send_message(self, mock_smtp: mock.Mock):
        target = client.SMTPClient("localhost")
        msg = client.MIMEText("Foo")

        with target:
            target.send_message(msg)

        mock_smtp.return_value.send_message.assert_called_once_with(msg)

    def test_send_message__not_connected(self, mock_smtp: mock.Mock):
        target = client.SMTPClient("localhost")
        msg = client.MIMEText("Foo")

        with pytest.raises(client.NotConnected):
            target.send_message(msg)

    @pytest.mark.parametrize("msg_args, expected_args", (
            ({}, {}),
            ({"to": "foo@localhost"}, {"To": "foo@localhost"}),
            ({"cc": "1@localhost"}, {"CC": "1@localhost"}),
            ({"cc": ["1@localhost", "2@localhost"]}, {"CC": "1@localhost, 2@localhost"}),
            ({"bcc": "1@localhost"}, {"BCC": "1@localhost"}),
            ({"bcc": ["1@localhost", "2@localhost"]}, {"BCC": "1@localhost, 2@localhost"}),
    ))
    def test_send_plain(
        self,
        mock_smtp: mock.Mock,
        msg_args: Dict[str, Any],
        expected_args: Dict[str, str],
    ):
        target = client.SMTPClient("localhost", from_addr="eek@localhost")

        msg_args.setdefault("to", ["foo@localhost", "bar@localhost"])
        msg_args.setdefault("subject", "Test Subject")
        msg_args.setdefault("body", "Hi Everybody\n\n- Bye!")

        expected_args.setdefault("To", "foo@localhost, bar@localhost")
        expected_args.setdefault("From", "eek@localhost")
        expected_args.setdefault("Subject", "Test Subject")
        expected_args.setdefault("CC", None)
        expected_args.setdefault("BCC", None)

        with target:
            target.send_plain(**msg_args)

        mock_smtp.return_value.send_message.assert_called_once()
        actual = mock_smtp.return_value.send_message.call_args[0][0]

        for key, value in expected_args.items():
            assert actual[key] == value
        assert actual._payload == "Hi Everybody\n\n- Bye!"
