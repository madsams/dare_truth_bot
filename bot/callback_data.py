from enum import Enum
from typing import Optional, Tuple, Union, List


class CallbackDataType(Enum):
    START = "START"
    GET_IN = "GET_IN"
    HELP = "NOT_FOUND"
    SEND_QUESTION = "SEND_QUESTION"
    SEND_QUESTION_TYPE = "SEND_QUESTION_TYPE"
    CHOOSE = "CHOOSE"
    ANSWER = "ANSWER"
    VOTE = "VOTE"


def _create_callback_data(data_type: CallbackDataType, payload: Optional = None) -> str:
    data = data_type.value
    if payload is not None:
        data += ";" + payload
    return data


def restore_callback_data(data: str) -> Tuple[str, Union[List, None]]:
    if data.find(";"):
        split: List[str] = data.split(";")
        type, payloads = split[0], split[1:]
        return type, payloads
    else:
        return data, None


def help_cbd() -> str:
    return _create_callback_data(CallbackDataType.HELP)


def send_question_cbd() -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION)


def send_question_type_cbd(payload: str) -> str:
    return _create_callback_data(CallbackDataType.SEND_QUESTION_TYPE, payload)


def start_cbd(start_payload: str) -> str:
    return _create_callback_data(CallbackDataType.START, start_payload)


def get_in_cbd(get_in_payload: str) -> str:
    return _create_callback_data(CallbackDataType.GET_IN, get_in_payload)


def dare_cbd(payload: str = None):
    return _create_callback_data(CallbackDataType.CHOOSE, payload)


def truth_cbd(payload: str = None):
    return _create_callback_data(CallbackDataType.CHOOSE, payload)


def answer_cbd(payload: str):
    return _create_callback_data(CallbackDataType.ANSWER, payload)


def vote_cbd(payload: str):
    return _create_callback_data(CallbackDataType.VOTE, payload)


callbacks = {
    'help': help_cbd,
    'send_question': send_question_cbd,
    'send_question_type': send_question_type_cbd,
    'start': start_cbd,
    'get_in': get_in_cbd,
    'dare': dare_cbd,
    'truth': truth_cbd,
    'answered': answer_cbd,
    'yes': vote_cbd,
    'no': vote_cbd,
}
