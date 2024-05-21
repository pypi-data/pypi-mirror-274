import time
import shutil
import locale
from time import sleep
from typing import Any

import ipih

from pih import A

from MedicalAutomationService.const import SD, VALENTA_SOURCE_HOST

SC = A.CT_SC

ISOLATED: bool = False

def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, as_standalone=as_standalone):

        from pih import subscribe_on, serve
        from pih.tools import ParameterList
        from pih.consts.errors import NotFound
        from pih.collections import PolibaseDocument
        from pih.collections import User, ActionWasDone
        from MobileHelperService.client import Client as MIO
        from pih.collections.service import SubscribtionResult
        from MobileHelperService.const import COMMAND_KEYWORDS
        from pih.tools import j, js, one, while_not_do, nn, n, ln
        from MobileHelperService.api import MobileOutput, mio_command
        from pih.consts.errors import OperationExit, OperationCanceled
        
        target_GROUP: A.CT_ME_WH.GROUP = A.CT_ME_WH.GROUP.SCANNED_DOCUMENT_HELPER_CLI
        target: MobileOutput = MIO.create_output(target_GROUP)

        def new_polibase_scanned_document_processed(path: str) -> None:
            A.E.new_polibase_scanned_document_processed(path)
            A.PTH.confirm_file(path)

        def service_call_handler(
            sc: SC,
            pl: ParameterList,
            subscribtion_result: SubscribtionResult | None,
        ) -> Any:
            doctor_user: User | None = None
            if sc == SC.heart_beat:
                if (A.SE.life_time.seconds / 60) % 2 == 0:
                    A.SYS.start_windows_service_if_stopped(
                        A.CT_WINDOWS.SERVICES.WIA, VALENTA_SOURCE_HOST
                    )
                return
            A.PTH
            if sc == SC.send_event:
                if subscribtion_result.result:  # type: ignore
                    event: A.CT_E | None = None
                    event_parameters: list[Any] | None = None
                    event, event_parameters = A.D_Ex_E.with_parameters(pl)
                    if event == A.E_B.service_was_started():
                        if A.D.get(A.CT_SR.FILE_WATCHDOG) == event_parameters[0]:
                            A.A_PTH.listen(A.PTH.MEDICAL_DATA.VALUE)
                        return
                    if event == A.E_B.action_was_done():
                        action_data: ActionWasDone = A.D_Ex_E.action(event_parameters)  # type: ignore
                        action: A.CT_ACT = action_data.action  # type: ignore
                        if action == A.CT_ACT.VALENTA_SYNCHRONIZATION:
                            A.SYS.start_windows_service_if_stopped(
                                A.CT_WINDOWS.SERVICES.WIA, VALENTA_SOURCE_HOST
                            )
                            file_path_list: list[str] | None = (
                                A.PTH.file_path_list_by_directory_info(
                                    A.PTH.MEDICAL_DATA.VALUE, confirmed=False
                                )
                            )
                            file_path_list_length: int = ln(file_path_list)
                            forced: bool = action_data.forced
                            new_document_is_present: bool = file_path_list_length > 0
                            if new_document_is_present or forced:
                                user: User | None = None
                                while True:
                                    try:
                                        user = A.R_U.by_login(action_data.user_login).data  # type: ignore
                                    except NotFound as exception:
                                        break
                                user_output: MobileOutput = MIO.create_output(
                                    user.telephoneNumber  # type: ignore
                                )
                                with user_output.personalized():
                                    if new_document_is_present:
                                        user_output.write_line(
                                            js(
                                                (
                                                    "Cинхронизация Валенты: найдены новые исследования в количестве:",
                                                    file_path_list_length,
                                                    ".",
                                                )
                                            )
                                        )
                                    else:
                                        user_output.write_line(
                                            "Принудительная синхронизация Валенты."
                                        )
                                    user_output.write_line(
                                        "Начат процесс синхронизации Валенты: закрытие программы Валента на компьютерах."
                                    )
                                    close_valenta_clients()
                                    user_output.write_line(
                                        "Идёт процесс синхронизации Валенты: начато копирование файлов."
                                    )
                                    synchronize_valenta_files()
                                    user_output.write_line(
                                        "Завершён процесс синхронизации Валенты."
                                    )
                                    doctor_user = one(
                                        A.R_U.by_group(
                                            A.CT_AD.Groups.FunctionalDiagnostics
                                        )
                                    )
                                    doctor_output: MobileOutput = MIO.create_output(
                                        doctor_user.telephoneNumber  # type: ignore
                                    )
                                    for file_path in file_path_list:  # type: ignore
                                        doctor_output.write_line(
                                            js(
                                                (
                                                    "День добрый,",
                                                    j(
                                                        (
                                                            doctor_output.user.get_formatted_given_name(),
                                                            ".",
                                                        )
                                                    ),
                                                    "Новое исследование",
                                                )
                                            )
                                        )
                                        while_not_do(
                                            check_action=lambda: doctor_output.write_image(
                                                "Журнал пациента",
                                                A.D_CO.file_to_base64(file_path),  # type: ignore
                                            ),
                                            success_handler=lambda: new_polibase_scanned_document_processed(
                                                file_path
                                            ),
                                        )
                                    A.A_PTH.listen(A.PTH.MEDICAL_DATA.VALUE)
                        return
                    if event == A.CT_E.NEW_FILE_DETECTED:
                        file_path: str = A.PTH.path(event_parameters[0])
                        if A.PTH.get_extension(file_path) in (
                            A.CT_F_E.JPEG,
                            A.CT_F_E.JPG,
                        ):
                            if not valenta_source_host_is_available():
                                A.L.it_bot(
                                    js(
                                        (
                                            "Компьютер",
                                            VALENTA_SOURCE_HOST,
                                            "недоступен или выключен. Синхронизация продолжиться автоматически после того, как компьютер станет доступным",
                                        )
                                    )
                                )
                                while True:
                                    if A.C_R.accessibility_by_smb_port(
                                        VALENTA_SOURCE_HOST
                                    ):
                                        sleep(10 * 60)

                            A.L.polibase_document(
                                js(("Кандидат на документ Полибейс:", file_path)),
                                image_path=file_path,
                            )
                            polibase_document: PolibaseDocument | None = one(
                                A.R_RCG.polibase_document(file_path)
                            )  # type: ignore
                            if n(polibase_document):
                                while True:
                                    try:
                                        polibase_document = A.D.fill_data_from_source(
                                            PolibaseDocument(),
                                            MIO.waiting_for_result(
                                                js(
                                                    (
                                                        mio_command(
                                                            COMMAND_KEYWORDS.CHECK
                                                        ),
                                                        mio_command(
                                                            COMMAND_KEYWORDS.SCAN
                                                        ),
                                                    )
                                                ),
                                                A.CT_ME_WH.GROUP.PIH_CLI,
                                                target_GROUP,
                                                args=(file_path,),
                                            ),
                                        )

                                    except OperationCanceled as _:
                                        target.good("Это не документ Полибейс")
                                        polibase_document = None
                                        break
                                    except OperationExit as _:
                                        target.error("Нельзя отменить")
                                        continue
                                    if nn(polibase_document):
                                        break
                            if nn(polibase_document):
                                A.E.new_polibase_scanned_document_detected(
                                    polibase_document  # type: ignore
                                )
                                polibase_person_pin: int = (
                                    polibase_document.polibase_person_pin  # type: ignore
                                )
                                document_name: A.CT_P_DT = A.D.get(
                                    A.CT_P_DT, polibase_document.document_type  # type: ignore
                                )
                                if document_name in [
                                    A.CT_P_DT.HOLTER_JOURNAL,
                                    A.CT_P_DT.ABPM_JOURNAL,
                                ]:
                                    is_holter: bool = (
                                        document_name == A.CT_P_DT.HOLTER_JOURNAL
                                    )
                                    file_name: str = A.PTH.get_file_name(file_path)
                                    test: bool = file_name.startswith(A.CT.TEST.NAME)
                                    only_notify: bool = file_name.startswith("-")
                                    path_destination: str = A.PTH.join(
                                        A.PTH.POLIBASE.person_folder(
                                            polibase_person_pin
                                        ),
                                        A.PTH.add_extension(
                                            (
                                                "holter_journal"
                                                if is_holter
                                                else "abpm_journal"
                                            ),
                                            A.PTH.get_extension(file_path),
                                        ),
                                    )
                                    if not (test or only_notify):
                                        close_valenta_clients()
                                        synchronize_valenta_files()
                                    doctor_user = A.R_U.by_login(
                                        A.CT.TEST.USER
                                        if test
                                        else one(
                                            A.R_U.by_group(
                                                A.CT_AD.Groups.FunctionalDiagnostics
                                            )
                                        ).samAccountName  # type: ignore
                                    ).data
                                    doctor_output: MobileOutput = MIO.create_output(
                                        doctor_user.telephoneNumber  # type: ignore
                                    )
                                    patient_name: str = A.R_P.person_by_pin(
                                        polibase_person_pin
                                    ).data.FullName  # type: ignore
                                    doctor_output.write_line(
                                        j(
                                            (
                                                "День добрый, ",
                                                doctor_output.user.get_formatted_given_name(),
                                                ". Новое исследование - монитор ",
                                                (
                                                    "Холтера"
                                                    if is_holter
                                                    else "артериального давления"
                                                ),
                                                ": ",
                                                patient_name,
                                                ".",
                                            )
                                        )
                                    )
                                    while_not_do(
                                        check_action=lambda: doctor_output.write_image(
                                            "Журнал пациента",
                                            A.D_CO.file_to_base64(file_path),  # type: ignore
                                        ),
                                        success_handler=lambda: new_polibase_scanned_document_processed(
                                            file_path
                                        ),
                                    )
                                    if not (test or only_notify):
                                        A.ME_WS.by_workstation_name(
                                            A.CT.HOST.WS816.NAME,
                                            js(
                                                (
                                                    "Журнал пациента",
                                                    patient_name,
                                                    "отсканирован. Спасибо!",
                                                )
                                            ),
                                        )
                                        shutil.copy(file_path, path_destination)
                                    target.write_image(
                                        j(
                                            (
                                                "Документ отправлен доктору: ",
                                                doctor_user.name,  # type: ignore
                                                " (",
                                                A.D_F.whatsapp_send_message_to(
                                                    doctor_user.telephoneNumber,  # type: ignore
                                                    js(
                                                        (
                                                            "День добрый,",
                                                            A.D.to_given_name(
                                                                doctor_user.name  # type: ignore
                                                            ),
                                                        )
                                                    ),
                                                ),
                                                ")",
                                            )
                                        ),
                                        A.D_CO.file_to_base64(file_path),  # type: ignore
                                    )
                                    A.L.polibase_document(
                                        js(
                                            (
                                                "Отправленный документ Полибейс:",
                                                file_path,
                                            )
                                        )
                                    )
                                else:
                                    A.PTH.confirm_file(file_path)
                            else:
                                A.PTH.confirm_file(file_path)
                        else:
                            A.PTH.confirm_file(file_path)
            return True

        def close_valenta_clients() -> None:
            for host_name in [A.CT.HOST.WS816.NAME, A.CT.HOST.WS255.NAME]:
                A.A_WS.kill_process(A.CT.VALENTA.PROCESS_NAME, host_name)

        def valenta_source_host_is_available() -> bool:
            return A.C_R.accessibility_by_smb_port(A.CT_H.WS816.NAME)

        def synchronize_valenta_files() -> None:
            if valenta_source_host_is_available():
                robocopy_job_name: str = A.CT.VALENTA.NAME
                while True:
                    A.A_B.start_robocopy_job_by_name(robocopy_job_name, force=True)
                    if A.E.on_robocopy_job_complete(robocopy_job_name):
                        break
                    else:
                        time.sleep(2)
                        close_valenta_clients()

        def service_starts_handler() -> None:
            subscribe_on(SC.heart_beat)
            subscribe_on(SC.send_event)

        def service_started_handler() -> None:
            A.A_PTH.listen(A.PTH.MEDICAL_DATA.VALUE)

        serve(
            SD,
            service_call_handler,  # type: ignore
            service_starts_handler,
            service_started_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
