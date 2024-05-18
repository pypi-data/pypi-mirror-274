from setup_environment import *  # noqa: F403
import pytest
from footium_api import ReportStrategy


class TestMockReportStrategy(ReportStrategy):
    def __init__(self):
        self.messages = {"info": [], "event": [], "warning": [], "error": []}

    def info(self, content: str):
        self.messages["info"].append(content)

    def event(self, content: str):
        self.messages["event"].append(content)

    def warning(self, content: str):
        self.messages["warning"].append(content)

    def error(self, content: str):
        self.messages["error"].append(content)


@pytest.fixture
def mock_strategy():
    return TestMockReportStrategy()


def test_info(mock_strategy):
    mock_strategy.info("This is an info message")
    assert "This is an info message" in mock_strategy.messages["info"]


def test_event(mock_strategy):
    mock_strategy.event("This is an event message")
    assert "This is an event message" in mock_strategy.messages["event"]


def test_warning(mock_strategy):
    mock_strategy.warning("This is a warning message")
    assert "This is a warning message" in mock_strategy.messages["warning"]


def test_error(mock_strategy):
    mock_strategy.error("This is an error message")
    assert "This is an error message" in mock_strategy.messages["error"]
