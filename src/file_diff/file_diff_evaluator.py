from filecmp import dircmp
from os.path import join, normpath
from typing import Callable


class FileDiffEvaluator(object):
    """
    This class is responsible for producing the delta between the source and destination folders.
    """
    def __init__(self, callback: Callable) -> None:
        self.__callback = callback  # called after diff is completed

    def generate_file_diff(self, src: str, dst: str, sync_style: str) -> None:
        """
        Generates differences in files between source and destination folder.
        :param src: source folder
        :param dst: destination folder
        :param sync_style: currently used for debug
        :return: None
        """
        print(f"Received file diff options: src={src}, dst={dst}, sync_style={sync_style}")
        deltas = self.__file_diff(src, dst)
        self.__callback([self.__normalize_paths(delta) for delta in deltas])

    @staticmethod
    def __normalize_paths(paths: list) -> list:
        """
        Makes path separators consistent, then swaps to forward slash to mitigate rendering errors.
        PySimpleGUI doesn't appear to handle escaping backslashes cleanly.
        :param paths: list of raw file paths
        :return: list of normalized file paths
        """
        return [normpath(path).replace("\\", "/") for path in paths]

    def __file_diff(self, src: str, dst: str) -> tuple:
        """
        Find full paths of files that differ between source and destination folder.
        Recursive solution from: https://stackoverflow.com/a/43462738
        :param src: source folder
        :param dst: destination folder
        :return: source and destination deltas
        """
        dcmp = dircmp(src, dst)
        src_delta = [join(src, f) for f in dcmp.left_only]
        dst_delta = [join(dst, f) for f in dcmp.right_only]

        for sub_dir in dcmp.common_dirs:
            child_src_delta, child_dst_delta = self.__file_diff(join(src, sub_dir), join(dst, sub_dir))
            src_delta.extend(child_src_delta)
            dst_delta.extend(child_dst_delta)

        return src_delta, dst_delta
