from dirsync import sync

from src.gui.constants import SyncOptions


class FileSynchronizer(object):
    def __init__(self):
        self.sync_option_dict = {v: k for k, v in SyncOptions.items()}

    def run_sync(self, src, dst, style):
        if self.sync_option_dict[style] == "ONE_WAY":
            sync(src, dst, "sync", purge=True)
        elif self.sync_option_dict[style] == "TWO_WAY":
            sync(src, dst, "sync", twoway=True, purge=True)
        elif self.sync_option_dict[style] == "UPDATE":
            sync(src, dst, "update")
        else:
            print(f"Received unexpected sync style: {style}")
