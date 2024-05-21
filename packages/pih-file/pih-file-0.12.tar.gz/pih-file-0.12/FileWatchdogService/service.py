import ipih

from pih.tools import nn
from pih import A, PIHThread
from FileWatchdogService.const import SD

from dataclasses import dataclass

SC = A.CT_SC


@dataclass
class HostInfo:
    name: str | None = None
    accessible: bool | None = None


ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, as_standalone=as_standalone):

        from pih.tools import ParameterList, ne

        from typing import Any
        from time import sleep
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler, FileSystemEvent

        path_list: list[str] = []
        host_info_map: dict[str, HostInfo] = {}
        observer_map: dict[str, Observer] = {}  # type: ignore

        def on_new_file(value: str) -> None:
            A.E.new_file_detected(value)

        class Handler(FileSystemEventHandler):
            def on_created(self, event: FileSystemEvent):
                if not event.is_directory:
                    on_new_file(A.PTH.path(event.src_path))

            def on_deleted(self, event: FileSystemEvent):
                pass

            def on_moved(self, event: FileSystemEvent):
                pass

        def update_observer(path: str, create: bool, stop: bool) -> None:
            observer: Observer | None = None  # type: ignore
            if stop and path in observer_map:
                observer = observer_map[path]
                observer.stop()  # type: ignore
            if create:
                observer = Observer()
                observer_map[path] = observer
                observer.schedule(Handler(), path)  # type: ignore
                observer.start()  # type: ignore

        def service_starts_handler() -> None:
            PIHThread(file_observer_action)

        def detect_new_files(path: str) -> None:
            unconfirmed_file_path_list: list[str] = A.PTH.file_path_list_by_directory_info(path, confirmed=False)  # type: ignore
            if ne(unconfirmed_file_path_list):
                for file_path in unconfirmed_file_path_list:
                    on_new_file(file_path)

        def file_observer_action() -> None:
            while True:
                for host in list(host_info_map):
                    before_accessable: bool | None = host_info_map[host].accessible
                    after_accessable: bool = A.C_R.accessibility_by_smb_port(
                        host, count=1, check_all=False
                    )
                    host_info_map[host].accessible = after_accessable
                    if nn(before_accessable):
                        for path in path_list:
                            if A.PTH.host(path).lower() == host:
                                if not before_accessable and after_accessable:
                                    update_observer(path, True, False)
                                if before_accessable and not after_accessable:
                                    update_observer(path, False, True)
                sleep(5)

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.listen_for_new_files:
                path: str = A.PTH.path(pl.next())
                if path not in path_list:
                    path_list.append(path)
                host: str = A.PTH.host(path).lower()
                host_info_map[host] = HostInfo(host)
                update_observer(path, True, True)
                detect_new_files(path)

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,  # type: ignore
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
