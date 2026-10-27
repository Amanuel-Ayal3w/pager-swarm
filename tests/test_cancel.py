import threading

import pytest

from pager.graph.cancel import RunControl, Stopped, request_stop
from pager.graph.model import _wait_turn


def test_wait_returns_when_stop_is_already_set():
    control = RunControl()
    control.event.set()
    with pytest.raises(Stopped):
        _wait_turn(21, control.event)


def test_wait_stops_during_the_gap():
    control = RunControl()
    _wait_turn(0.4)

    def trip() -> None:
        control.event.set()

    timer = threading.Timer(0.05, trip)
    timer.start()
    with pytest.raises(Stopped):
        _wait_turn(0.4, control.event)
    timer.cancel()


def test_request_stop_closes_the_client():
    from pager.graph.cancel import close_run, open_run

    control = open_run("thread-stop")
    closed = []
    control.client = type("Client", (), {"close": lambda self: closed.append(True)})()
    request_stop()
    close_run("thread-stop")
    assert closed == [True]
