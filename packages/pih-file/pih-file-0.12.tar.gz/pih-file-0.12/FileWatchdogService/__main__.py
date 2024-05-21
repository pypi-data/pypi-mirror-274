import ipih


def start() -> None:

    from FileWatchdogService.service import start

    start(True)


if __name__ == "__main__":
    start()
