import daemon

from background_processing import main_process

with daemon.DaemonContext():
    main_process()