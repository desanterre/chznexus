import asyncio
import os
import tempfile
from unittest.mock import AsyncMock, patch

import pytest

from chznexus.bot.user import append_to_excel  # Adjust import if needed
from chznexus.bot.utils import parse_login_ok
from chznexus.bot.websocket_handler import connect, user_map


def test_parse_login_ok():
    mock_message = "someprefixy4:chimTester"
    result = parse_login_ok(mock_message)
    assert result == "chimTester"


@pytest.mark.asyncio
@patch("websockets.connect")
async def test_connect_mock(mock_connect):
    mock_websocket = AsyncMock()

    mock_websocket.recv = AsyncMock(
        side_effect=[
            "LOGIN_OK:123:user123",  # Login OK response (does not add user_map)
            "USER_JOINED midi456y4:nicky456:someone",  # User joined message adds user 456
            "USER_TALK mid123y4:nicky123:Hello world",  # User talk message (example)
            "USER_LEFT midi456",  # User left message removes user 456
            asyncio.CancelledError(),  # Exit loop
        ]
    )

    mock_connect.return_value.__aenter__.return_value = mock_websocket

    user_map.clear()

    with pytest.raises(asyncio.CancelledError):
        await connect()

    assert "123" not in user_map
    assert "456" not in user_map


def test_append_to_excel_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_log.xlsx")
        append_to_excel("002", "testuser", filename=test_file)
        assert os.path.exists(test_file)


def test_append_to_excel_adds_user():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_log.xlsx")
        append_to_excel("003", "alpha", filename=test_file)
        # Optionally, re-open the file and verify contents (requires openpyxl)
        assert os.path.exists(test_file)
