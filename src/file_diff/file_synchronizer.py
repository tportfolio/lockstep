from dirsync import sync

from src.gui.constants import SyncOptions


class FileSynchronizer(object):
    """
    This class is responsible for managing the synchronization process between two folders.
    """
    def __init__(self, enable_purge):
        # inverse dictionary to look up text values from GUI
        self.sync_option_dict = {v: k for k, v in SyncOptions.items()}
        self.__enable_purge = enable_purge

    @property
    def enable_purge(self):
        """
        Getter for whether to enable file purge on sync.
        :return: enable_purge value
        """
        return self.__enable_purge

    @enable_purge.setter
    def enable_purge(self, enable_purge):
        """
        Setter for enable file purge option.
        :param enable_purge: boolean
        :return: None
        """
        self.__enable_purge = enable_purge

    def run_sync(self, src, dst, style):
        """
        Run synchronization process from dirsync.
        :param src: source folder
        :param dst: destination folder
        :param style: how to sync folder (one-way, two-way, update)
        :return: None
        """
        if self.sync_option_dict[style] == "ONE_WAY":
            sync(src, dst, "sync", purge=self.enable_purge)
        elif self.sync_option_dict[style] == "TWO_WAY":
            sync(src, dst, "sync", twoway=True, purge=self.enable_purge)
        elif self.sync_option_dict[style] == "UPDATE":
            sync(src, dst, "update")
        else:
            print(f"Received unexpected sync style: {style}")
