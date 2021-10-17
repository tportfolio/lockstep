from filecmp import dircmp
from os.path import join, normpath


class FileDiffEvaluator(object):
    def __init__(self, callback):
        self.callback = callback

    def generate_file_diff(self, src, dst, sync_style):
        print(f"Received file diff options: src={src}, dst={dst}, sync_style={sync_style}")
        src_delta, dst_delta = self.file_diff(src, dst)
        self.callback([[self.normalize_path(x) for x in src_delta], [self.normalize_path(x) for x in dst_delta]])

    @staticmethod
    def normalize_path(path):
        return normpath(path).replace("\\", "/")

    def file_diff(self, src, dst):
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
            child_src_delta, child_dst_delta = self.file_diff(join(src, sub_dir), join(dst, sub_dir))
            src_delta.extend(child_src_delta)
            dst_delta.extend(child_dst_delta)

        return src_delta, dst_delta
