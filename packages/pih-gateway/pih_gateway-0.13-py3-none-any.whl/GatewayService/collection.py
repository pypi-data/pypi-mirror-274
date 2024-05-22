from dataclasses import dataclass


@dataclass
class WappiRawMessage:
    profile_id: str | None = None
    id: str | None = None
    body: str | None = None
    type: str | None = None
    sender: str | None = None
    recipient: str | None = None
    ack: int | None = None
    star: bool | None = None
    isFromTemplate: bool | None = None
    broadcast: bool | None = None
    isVcardOverMmsDocument: bool | None = None
    isForwarded: bool | None = None
    hasReaction: bool | None = None
    isDynamicReplyButtonsMsg: bool | None = None
    isMdHistoryMsg: bool | None = None
    senderName: str | None = None
    chatId: str | None = None
    time: int | None = None
    image_path: str | None = None
