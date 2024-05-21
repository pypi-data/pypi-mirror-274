import ipih

from pih import A, PIHThread, PIHThreadPoolExecutor

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    from pih.consts.errors import NotFound
    from PolibaseAutomationService.const import SD
    from pih.tools import ParameterList, n, e, ne, nn
    from pih.collections import PolibasePerson, EventDS, InaccesableEmailInformation

    from concurrent import futures
    from time import sleep
    from typing import Any

    new_person_executor = PIHThreadPoolExecutor(max_workers=10)
    person_information_fix_executor = PIHThreadPoolExecutor(max_workers=1)

    def check_for_person_duplication(person: PolibasePerson) -> bool | None:
        duplicated_person: PolibasePerson | None = A.D.get_first_item(
            A.D_P.duplicate_persons_by_person(person, check_for_birth=True)
        )
        if ne(duplicated_person):
            try:
                registrator_or_operator: PolibasePerson | None = (
                    A.R_P.person_registrator_by_pin(person.pin).data  # type: ignore
                )
                A.E.send(
                    *A.E_B.polibase_person_duplication_was_detected(
                        person, duplicated_person, registrator_or_operator
                    )
                )
                return True
            except NotFound:
                return False
        return None

    def new_person_action(person_pin: int, on_start: bool) -> bool:
        return create_barcode_new_format_for_person(
            A.D_P.person_by_pin(person_pin), on_start
        )

    def create_barcode_new_format_for_person(
        person: PolibasePerson, on_start: bool
    ) -> bool:
        person_pin: int = person.pin  # type: ignore
        #
        A.PTH.make_directory_if_not_exists(A.PTH_P.person_folder(person_pin))
        A.A_P.create_barcode_for_person(person)
        result: bool = A.A_P.set_barcode(
            A.CT_P.BARCODE.get_file_name(person_pin, True), person
        )
        if on_start:
            A.E.send(*A.E_B.polibase_person_was_created(person))
            check_for_person_duplication(person)
        else:
            A.E.send(*A.E_B.polibase_person_was_updated(person))
        return result

    def service_starts_thread_action() -> None:
        person_pin_list: list[int] = (
            A.R_P.person_pin_list_with_old_format_barcode().data
        )  # type: ignore
        if ne(person_pin_list):
            A.E.send(
                *A.E_B.polibase_persons_barcodes_old_format_were_detected(
                    person_pin_list
                )
            )
            future_to_person_list = {
                new_person_executor.submit(
                    new_person_action, person_pin, True
                ): person_pin
                for person_pin in person_pin_list
            }
            for future_person in futures.as_completed(future_to_person_list):  # type: ignore
                if e(future_person.exception()):
                    future_person.result()
            A.E.send(
                *A.E_B.polibase_person_barcodes_new_format_were_created(person_pin_list)
            )
            person_list: list[PolibasePerson] = A.R_P.persons_by_pin(
                person_pin_list
            ).data  # type: ignore
            for person in person_list:
                if person_information_fix(person, update=False, actual=False):
                    sleep(0.5)
        fix_prerecording_person()

    def service_starts_handler() -> None:
        A.SRV_A.subscribe_on(SC.send_event)
        PIHThread(service_starts_thread_action)

    def fix_prerecording_person(person: PolibasePerson | None = None) -> None:
        person = person or A.R_P.person_by_pin(A.CT_P.PRERECORDING_PIN).data
        for index in range(A.CT_P.TELEPHONE_NUMBER_COUNT):
            telephone_number: str | None = person.__getattribute__(
                A.CT_UP.TELEPHONE_NUMBER + A.D_F.index(index)
            )
            if ne(telephone_number):
                if A.C.telephone_number(telephone_number, True):  # type: ignore
                    A.A_P.set_telephone_number(index, A.CT_P.EMPTY_VALUE, person)  # type: ignore
        if A.C.email(person.email):  # type: ignore
            A.A_P.email(A.CT_P.EMPTY_VALUE, person)  # type: ignore

    def service_call_handler(sc: SC, pl: ParameterList) -> Any:
        if sc == SC.send_event:
            event, parameters = A.D_Ex_E.with_parameters(pl)
            if event in [
                A.E_B.polibase_person_was_updated(),
                A.E_B.polibase_person_was_created(),
            ]:
                update: bool = event == A.E_B.polibase_person_was_updated()
                person_pin: int = parameters[1]
                person: PolibasePerson = A.R_P.person_by_pin(person_pin).data  # type: ignore
                if update:
                    if person_pin == A.CT_P.PRERECORDING_PIN:
                        fix_prerecording_person(person)
                if not A.D_C.polibase_person_has_new_barcode_format(person):
                    A.E.send(
                        *A.E_B.polibase_persons_barcodes_old_format_were_detected(
                            [person.pin]  # type: ignore
                        )
                    )
                    create_barcode_new_format_for_person(person, False)
                    A.E.send(
                        *A.E_B.polibase_person_barcodes_new_format_were_created(
                            [person.pin]  # type: ignore
                        )
                    )
                person_information_fix(person, update=update, actual=True)
            return True

    def send_person_email_was_added(person: PolibasePerson, exists: bool) -> None:
        if exists:
            A.A_E.remove(*A.E_B.polibase_person_email_was_added(None, person))
        A.E.send(*A.E_B.polibase_person_email_was_added(person))

    def person_information_fix(
        person: PolibasePerson, update: bool, actual: bool
    ) -> None:
        # fix email
        test: bool = A.S.get(A.CT_S.EMAIL_VALIDATION_TEST)

        def person_information_fix_action(
            person: PolibasePerson, update: bool, actual: bool
        ) -> bool:
            person_card_registry_folder_update(person, update)
            if A.S.get(A.CT_S.EMAIL_VALIDATION_IS_ON) and (
                not test or person.pin == A.CT.TEST.PIN
            ):
                #<email> text -> <email>
                
                email_src: str | None = A.D_Ex.email(person.email)
                if e(email_src):
                    A.A_E.remove_by_key(*A.E_B.ask_for_polibase_person_email(person))
                    return False
                if email_src in A.CT_P.ASK_EMAIL_LOCALY_VARIANTS:
                    A.E.send(*A.E_B.ask_for_polibase_person_email(person, True))
                    return False
                # if email is empty or email equal one of varianst of empty values - "нет" or "-"
                if email_src in A.CT_P.EMPTY_EMAIL_VARIANTS:
                    return False
                else:
                    A.A_E.remove_by_key(*A.E_B.ask_for_polibase_person_email(person))
                    email_formatted: str | None = A.D_F.email(
                        email_src,  # type: ignore
                        use_default_domain=False,
                        email_correction=True,
                    )
                    if email_formatted != email_src:
                        A.A_P.email(email_formatted, person)
                        return False
                    registrator_or_operator: PolibasePerson = (
                        get_registrator_or_operator_person(person, update)
                    )
                    if n(registrator_or_operator.pin):
                        registrator_or_operator = A.R_P.person_registrator_by_pin(
                            person.pin  # type: ignore
                        ).data  # type: ignore
                    (
                        event,
                        parameters_for_search,
                    ) = A.E_B.polibase_person_with_inaccessable_email_was_detected(
                        person
                    )  # type: ignore

                    def compare_email(email: str, email_event_ds: EventDS) -> bool:
                        return (
                            email.lower()
                            == A.D.fill_data_from_source(
                                InaccesableEmailInformation(),
                                email_event_ds.parameters,
                            ).email.lower()
                        )

                    email_accessable: bool | None = None
                    # get event information form DS if is exists: eventDS
                    event_inaccessable_email_ds: EventDS | None = (
                        A.R.get_first_item(A.R_E.get(event, parameters_for_search))  # type: ignore
                        if update
                        else None
                    )  # type: ignore
                    event_added_ds: EventDS | None = None
                    if nn(event_inaccessable_email_ds):
                        if not compare_email(email_src, event_inaccessable_email_ds):  # type: ignore
                            email_accessable = A.C.email(
                                email_src, check_accesability=True  # type: ignore
                            )
                        A.A_E.remove(event, parameters_for_search)
                    else:
                        if update:
                            (
                                event,
                                parameters_for_search,
                            ) = A.E_B.polibase_person_email_was_added(
                                None, person
                            )  # type: ignore
                            event_added_ds = A.R.get_first_item(
                                A.R_E.get(event, parameters_for_search)  # type: ignore
                            )  # type: ignore
                        if (
                            not update
                            or e(event_added_ds)
                            or not compare_email(email_src, event_added_ds)  # type: ignore
                        ):
                            email_accessable = A.C.email(
                                email_src, check_accesability=True  # type: ignore
                            )
                    if email_accessable == True:
                        send_person_email_was_added(person, nn(event_added_ds))
                    if email_accessable == False:
                        A.E.send(
                            *A.E_B.polibase_person_with_inaccessable_email_was_detected(
                                person, registrator_or_operator, actual
                            )
                        )
                return True
            return False

        person_information_fix_executor.submit(
            person_information_fix_action, person, update, actual
        )

    def get_registrator_or_operator_person(
        person: PolibasePerson, update: bool
    ) -> PolibasePerson:
        return (
            A.R_P.person_operator_by_pin if update else A.R_P.person_registrator_by_pin
        )(
            person.pin # type: ignore
        ).data  # type: ignore

    def person_card_registry_folder_update(
        person: PolibasePerson, update: bool
    ) -> None:
        person_pin: int = person.pin  # type: ignore
        is_test: bool = person_pin == A.CT.TEST.PIN
        person_card_registry_folder: str | None = person.ChartFolder
        if ne(person_card_registry_folder):
            if person_card_registry_folder in A.CT_CR.SUITABLE_FOLDER_NAME_SYMBOL:
                registrator_or_operator: PolibasePerson = (
                    get_registrator_or_operator_person(person, update)
                )
                person_card_registry_folder = A.CR.get_suitable_folder_name_for_person(
                    person
                )
                A.A_P.set_card_registry_folder(person_card_registry_folder, person)
                if not is_test:
                    A.E.send(
                        *A.E_B.polibase_person_set_suitable_card_registry_folder(
                            person_card_registry_folder,
                            person,
                            registrator_or_operator,
                        )
                    )
                return
            person_card_registry_folder_formatted: str = (
                A.D_F.polibase_person_card_registry_folder(person_card_registry_folder)  # type: ignore
            )
            if person_card_registry_folder != person_card_registry_folder_formatted:
                A.A_P.set_card_registry_folder(
                    person_card_registry_folder_formatted, person
                )
                return
        A.CR.set_folder_for_person(
            person_card_registry_folder,
            person,
            get_registrator_or_operator_person(person, update),
            set_by_polibase=True,
        )

    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
