import ipih

def start(as_standalone: bool = False) -> None:

    from pih import A, PIHThread
    from WSService.const import SD
    from pih.tools import ParameterList
    from pih.collections import Workstation
    from pih.consts import WorkstationMessageMethodTypes

    from datetime import datetime
    from typing import Any

    SC = A.CT_SC

    ISOLATED: bool = False

    class DH:
        action_at_work: bool = False

    def action_for_all_workstations(shutdown: bool, force: bool = False) -> None:
        def filter_function(workstation: Workstation) -> bool:
            return workstation.accessable and (
                force or A.C_WS.shutdownable(workstation)
                if shutdown
                else A.C_WS.rebootable(workstation)
            )

        def every_action(workstation: Workstation) -> None:
            ws_action(workstation.name, shutdown)

        A.R.every(every_action, A.R.filter(filter_function, A.R_WS.all()))

    def heat_beat_handler(current: datetime) -> None:
        if A.D.is_equal_by_time(current, A.S_WS.shutdown_time()):
            action_for_all_workstations(True)
        if A.D.is_equal_by_time(current, A.S_WS.reboot_time()):
            action_for_all_workstations(False)
        DH.action_at_work = False

    def service_call_handler(sc: SC, pl: ParameterList) -> Any:
        if sc == SC.heart_beat:
            if not DH.action_at_work:
                DH.action_at_work = True
                current_datetime: datetime = A.D_Ex.parameter_list(pl).get()
                PIHThread(heat_beat_handler, args=(current_datetime,))
            return True
        if sc == SC.send_message_to_user_or_workstation:
            return A.ME_WS.to_user_or_workstation(
                pl.next(),
                pl.next(),
                pl.next(),
                pl.next(),
                WorkstationMessageMethodTypes.LOCAL_PSTOOL_MSG,
            )
        if sc in [SC.reboot, SC.shutdown]:
            name: str | None = pl.next()
            force: bool = pl.next()
            shutdown: bool = sc == SC.shutdown
            if A.D.is_empty(name):
                action_for_all_workstations(shutdown, force)
            else:
                workstation: Workstation | None = None
                if not force:
                    workstation = A.R_WS.by_name(name).data
                if force or (
                    A.C_WS.shutdownable(workstation)
                    if shutdown
                    else A.C_WS.rebootable(workstation)
                ):
                    return ws_action(name, shutdown)
                return False
        if sc == SC.kill_process:
            return A.EXC.kill_process(pl.next(), pl.next(), pl.next())

    def ws_action(name: str, shutdown: bool) -> bool:
        if shutdown:
            return A.EXC.ws_shutdown(name)
        return A.EXC.ws_reboot(name)

    def service_starts_handler() -> None:
        A.SRV_A.subscribe_on(SC.heart_beat)

    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
