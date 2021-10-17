from dirsync import sync

from src.gui.constants import SyncOptions


class FileSynchronizer(object):
    def __init__(self, enable_purge):
        self.sync_option_dict = {v: k for k, v in SyncOptions.items()}
        self.__enable_purge = enable_purge

    @property
    def enable_purge(self):
        return self.__enable_purge

    @enable_purge.setter
    def enable_purge(self, enable_purge):
        self.__enable_purge = enable_purge

    def run_sync(self, src, dst, style):
        if self.sync_option_dict[style] == "ONE_WAY":
            sync(src, dst, "sync", purge=self.enable_purge)
        elif self.sync_option_dict[style] == "TWO_WAY":
            sync(src, dst, "sync", twoway=True, purge=self.enable_purge)
        elif self.sync_option_dict[style] == "UPDATE":
            sync(src, dst, "update")
        else:
            print(f"Received unexpected sync style: {style}")
