import ipih

from pih import A, PIHThread, strdict
from GatewayService.const import SD, ALISA_TIMEOUT

from typing import Any
from time import time_ns
from collections import defaultdict


SC = A.CT_SC

SD.host_changeable = True

ISOLATED: bool = False

message_list_holder: dict[str, list[strdict]] = defaultdict(list)
message_list_break: dict[str, bool] = {}


class DH:
    current_time: float = 0.0


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):

        from GatewayService.collection import WappiRawMessage
        from pih.collections import WhatsAppMessage, BarcodeInformation
        from pih.tools import j, js, ne, e, nl, esc, lw, jnl, nns, nnl, ParameterList

        from fastapi import FastAPI, Body, Request
        from fastapi.responses import HTMLResponse
        import uvicorn

        fast_api = FastAPI()

        @fast_api.get("/")
        def api_root():
            version: str = A.V.value
            return HTMLResponse(
                js((nl(nns(SD.description), normal=False), "Version:", version))
            )

        @fast_api.post("/alisa_gateway")
        def alisa_command_receive_handler(request: Request, message_body=Body(...)):
            message: strdict = message_body["request"]

            command: str = str(
                message["payload"]
                if "type" in message and message["type"] == "ButtonPressed"
                else js(message["nlu"]["tokens"]) or "pih"
            )
            DH.current_time = time_ns()
            recipient: str = A.D_TN.by_login("nak")
            message_list_holder[recipient] = []
            message_list_break[recipient] = False
            A.A_MIO.send_outside(command, recipient)
            while not message_list_break[recipient]:
                if (time_ns() - DH.current_time) // 1_000_000 > ALISA_TIMEOUT:
                    return {"text": "Долго"}
            message_list: list[strdict] = message_list_holder[recipient]
            text: str = jnl(
                A.D.map(
                    A.D_F.as_plain_message,
                    A.D.map(
                        lambda item: item["value"],
                        A.D.filter(
                            lambda item: item["type"] != "index_item",
                            message_list,
                        ),
                    ),
                )
            )
            result: strdict = {"text": text}
            buttons: list[strdict] = A.D.filter(
                lambda item: item["type"] == "index_item",
                message_list,
            )
            if ne(buttons):
                result["buttons"] = A.D.map(
                    lambda item: {
                        "title": A.D_F.as_plain_message(item["text"]),
                        "payload": item["value"],
                        "hide": True,
                    },
                    A.D.sort(lambda item: item["value"], buttons),
                )

            return result

        @fast_api.post("/message_gateway")
        def wappi_whatsapp_message_receive_handler(
            request: Request, message_body=Body(...)
        ):
            wh_type: str = message_body["wh_type"]
            if wh_type == "incoming_message":
                type: str | None = A.D.if_is_in(message_body, "type")
                if ne(type):
                    is_image: bool = type == "image"
                    is_chat: bool = type == "chat"
                    if is_chat or is_image:
                        raw_message: WappiRawMessage = A.D.fill_data_from_source(
                            WappiRawMessage(), message_body
                        )
                        raw_message.sender = message_body["from"]
                        raw_message.recipient = message_body["to"]
                        message: WhatsAppMessage = A.D.fill_data_from_source(
                            WhatsAppMessage(), raw_message.__dict__
                        )
                        message.message = (
                            A.D.if_is_in(message_body, "caption", "")
                            if is_image
                            else raw_message.body
                        )
                        recipient_telephone_number: str = nns(
                            A.D_Ex.wappi_telephone_number(raw_message.recipient)
                        )
                        sender_telephone_number: str = nns(
                            A.D_Ex.wappi_telephone_number(raw_message.sender)
                        )
                        message.from_me = A.C_ME_WH_W.from_me(sender_telephone_number)
                        message.recipient = recipient_telephone_number
                        message.sender = sender_telephone_number
                        if raw_message.chatId == raw_message.sender:
                            message.chatId = None
                        if is_image:
                            if message.profile_id == A.D.get(A.CT_ME_WH_W.Profiles.IT):
                                wait_for_input_polibase_person_pin: bool = A.IW.has(
                                    A.CT_P.NAMES.PERSON_PIN,
                                    sender_telephone_number,
                                )
                                image_path: str = A.PTH.join(
                                    A.PTH.MOBILE_HELPER.INCOME_IMAGES_FOLDER,
                                    A.PTH.add_extension(A.D.uuid(), A.CT_F_E.JPG),
                                )
                                A.D.save_base64_as_image(
                                    image_path, nns(raw_message.body)
                                )
                                barcode_information_list: (
                                    list[list[BarcodeInformation]] | None
                                ) = A.R_RCG.barcodes_information(
                                    image_path, True, 0
                                ).data
                                if (
                                    ne(barcode_information_list)
                                    and ne(nnl(barcode_information_list)[0])
                                    and A.D_C.polibase_person_barcode(
                                        nnl(barcode_information_list)[0][0]
                                    )
                                ):
                                    barcode_information: BarcodeInformation = nnl(
                                        barcode_information_list
                                    )[0][0]
                                    if ne(barcode_information.data):
                                        if wait_for_input_polibase_person_pin:
                                            message.message = barcode_information.data
                                        else:
                                            if e(message.message):
                                                message.message = js(
                                                    (
                                                        A.root.NAME,
                                                        "card",
                                                        "registry",
                                                        "find",
                                                        barcode_information.data,
                                                    )
                                                )
                                            else:
                                                message.message = js(
                                                    (
                                                        A.root.NAME,
                                                        "card",
                                                        "registry",
                                                        message.message,
                                                        barcode_information.data,
                                                    )
                                                )
                                else:
                                    if wait_for_input_polibase_person_pin:
                                        message.message = A.CT_P.BARCODE.NOT_FOUND
                                    else:
                                        if ne(message.message):
                                            message.message += " "
                                        message.message = j(
                                            (message.message, esc(image_path))
                                        )
                        else:
                            wait_for_input_polibase_person_card_registry_folder: (
                                bool
                            ) = A.IW.has(
                                A.CT_P.NAMES.PERSON_CARD_REGISTRY_FOLDER,
                                sender_telephone_number,
                            )
                            if wait_for_input_polibase_person_card_registry_folder:
                                message_parts: list[str] = A.D.not_empty_items(
                                    lw(message.message).strip().split(" ")
                                )
                                if len(message_parts) == 4:
                                    for part in [A.root.NAME, "card", "registry"]:
                                        if part in message_parts:
                                            message_parts.remove(part)
                                    if len(
                                        message_parts
                                    ) == 1 and A.C_P.person_card_registry_folder(
                                        message_parts[0]
                                    ):
                                        message.message = message_parts[0]
                        A.E.whatsapp_message_received(message)

        def service_starts_handler() -> None:
            A.SYS.kill_process_by_port(A.CT_PORT.HTTP)
            PIHThread(run_fastapi_server)

        def run_fastapi_server() -> None:
            uvicorn.run(fast_api, host="0.0.0.0", port=A.CT_PORT.HTTP)

        def listener(pl: ParameterList) -> None:
            message_list: list[strdict] = A.D.rpc_decode(pl.next())
            for message in message_list:
                recipient: str = message["recipient"]
                message_type: str = message["type"]
                message_list_holder[recipient].append(message)
                message_list_break[recipient] = message_type == "break"
            print("time", (time_ns() - DH.current_time) // 1_000_000)

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.serve_command:
                listener(pl)

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,  # type: ignore
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
