from typing import Optional
import enum
import dataclasses

class BotModel(enum.Enum):
    EB3_5 = 'EB35'
    EB4_0 = 'EB40'

@dataclasses.dataclass
class SessionBase:
    sessionId: str
    name: str
    pluginIds: list
    botModel: str
    creationTimestamp: int

@dataclasses.dataclass
class Session:
    tops: list[SessionBase]
    normals: list[SessionBase]

@dataclasses.dataclass
class SessionDetailBase:
    name: str
    botModel: str
    creationTimestamp: int

@dataclasses.dataclass
class SessionDetailHistory:
    chatId: str
    role: str
    text: str
    creationTimestamp: int

@dataclasses.dataclass
class SessionDetail:
    base: SessionDetailBase
    histories: list[SessionDetailHistory]
    currentChatId: str

@dataclasses.dataclass
class Plugin:
    id: str
    name: str
    description: str
    fileTypes: Optional[list]
    raw: dict

class FileExtension(enum.Enum):
    jpeg = 'jpeg-image'
    jpg = 'jpg-image'
    png = 'png-image'
    doc = 'doc-file'
    docx = 'docx-file'
    pdf = 'pdf-file'

    @property
    def value(self):
        return self._value_.split('-')[1]

@dataclasses.dataclass
class File:
    name: str
    type_: str
    size: int
    url: str

@dataclasses.dataclass
class Response:
    answer: str
    sessionId: str
    botChatId: str

@dataclasses.dataclass
class AskStreamResponse(Response):
    done: bool

@dataclasses.dataclass
class AskResponse(Response):
    pass