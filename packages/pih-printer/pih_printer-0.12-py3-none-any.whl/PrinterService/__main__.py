import ipih


def start() -> None:
    from PrinterService.service import start

    start(True)


if __name__ == "__main__":
    start()
