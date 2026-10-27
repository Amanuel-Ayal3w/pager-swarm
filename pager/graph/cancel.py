"""Stop a live run. The model wait and the in-flight client both watch this."""

import threading


class Stopped(Exception):
    pass


class RunControl:
    def __init__(self) -> None:
        self.event = threading.Event()
        self.client: object | None = None
        self.incident_id = ""


_lock = threading.Lock()
_controls: dict[str, RunControl] = {}
_by_incident: dict[str, str] = {}


def open_run(thread_id: str) -> RunControl:
    control = RunControl()
    with _lock:
        _controls[thread_id] = control
    return control


def attach_incident(thread_id: str, incident_id: str) -> None:
    with _lock:
        control = _controls.get(thread_id)
        if control is None:
            return
        control.incident_id = incident_id
        _by_incident[incident_id] = thread_id


def close_run(thread_id: str) -> None:
    with _lock:
        control = _controls.pop(thread_id, None)
        if control and control.incident_id:
            _by_incident.pop(control.incident_id, None)


def request_stop(incident_id: str | None = None) -> list[str]:
    with _lock:
        if incident_id:
            thread_ids = [thread_id for thread_id, control in _controls.items() if control.incident_id == incident_id]
            mapped = _by_incident.get(incident_id)
            if mapped and mapped not in thread_ids:
                thread_ids.append(mapped)
        else:
            thread_ids = list(_controls)
        clients = []
        for thread_id in thread_ids:
            control = _controls.get(thread_id)
            if control is None:
                continue
            control.event.set()
            if control.client is not None:
                clients.append(control.client)
    for client in clients:
        closer = getattr(client, "close", None)
        if closer is None:
            continue
        try:
            closer()
        except Exception:
            continue
    return thread_ids


def caused_by_stop(exc: BaseException) -> bool:
    if isinstance(exc, Stopped):
        return True
    nested = getattr(exc, "exceptions", None)
    if nested and any(caused_by_stop(item) for item in nested):
        return True
    cause = exc.__cause__ or exc.__context__
    return bool(cause and cause is not exc and caused_by_stop(cause))
