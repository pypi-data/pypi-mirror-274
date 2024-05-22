import atexit
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Optional, TypeVar, Generic
from ctypes import c_void_p, c_int64
import traceback
from reactivex.subject import Subject

from .dto_object import DtoObject
from .dto import requests as dto
from .serialization import deserialize
from .bindings import c_set_event_handler, CALLBACK


TEventData = TypeVar('TEventData', bound=DtoObject)


class Event(Generic[TEventData]):
    def __init__(self, name: str, data: TEventData) -> None:
        self.name = name
        self.data = data


events = Subject[Event[DtoObject]]()

event_executor = ThreadPoolExecutor(max_workers=1)  # pylint: disable=consider-using-with


def on_shutdown() -> None:
    event_executor.shutdown()


atexit.register(on_shutdown)


def event_handler(event_data: c_void_p, _tag: c_int64) -> None:
    try:
        event_buffers = deserialize(event_data)
        event_executor.submit(process_event_catch, event_buffers)
    except RuntimeError:
        # the error appears due to race condition with python shutting down and cannot be prevented
        pass


event_handler_cb = CALLBACK(event_handler)

c_set_event_handler(0, event_handler_cb)

parsers: Dict[str, Optional[Callable[[bytes], DtoObject]]] = {
    'test/event': dto.TestEvent.from_binary,
    'interface/unknown_response': dto.UnknownResponseEventWrapper.from_binary,
    'binary/interface/unknown_response': dto.UnknownBinaryResponseEventWrapper.from_binary,
    'interface/alert': dto.AlertEventWrapper.from_binary,
    'binary/interface/reply_only': dto.BinaryReplyOnlyEventWrapper.from_binary,
    'interface/disconnected': dto.DisconnectedEvent.from_binary,
}


def process_event_catch(event_buffers: List[bytes]) -> None:
    try:
        process_event(event_buffers)
    except:  # noqa, pylint: disable=W0702
        print("Unhandled exception in event:")
        traceback.print_exc()


def process_event(event_buffers: List[bytes]) -> None:
    event = dto.GatewayEvent.from_binary(event_buffers[0])

    if event.event not in parsers:
        raise RuntimeError(f"Event not supported: {event.event}")
    parse_event_data = parsers.get(event.event)

    has_data = len(event_buffers) > 1

    if has_data:
        if parse_event_data is None:
            raise RuntimeError(f"Event has data but no parser: {event.event}")
        event_data = parse_event_data(event_buffers[1])
    else:
        if parse_event_data is not None:
            raise RuntimeError(f"Event has no data but parser: {event.event}")
        raise RuntimeError(f"Event without data is not supported: {event.event}")

    events.on_next(Event(event.event, event_data))
