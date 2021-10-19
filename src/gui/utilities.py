import PySimpleGUI as sg
from os.path import dirname, basename


def gen_treedata(data: list, icon: bytes) -> sg.TreeData:
    """
    Transforms folder delta into file tree that is displayed in GUI.
    :param data: list of files
    :param icon: icon to represent direction of file movement
    :return: PySimpleGUI tree data structure
    """
    treedata = sg.TreeData()

    for path in data:
        parent_folder = dirname(path)
        folders = parent_folder.split("/")
        filename = basename(path)

        # iteratively add parent folders as keys to tree, if necessary
        for i, folder in enumerate(folders):
            parent = "/".join(folders[:i])
            if not parent:
                parent = ''

            curr = "/".join(folders[:i + 1])
            val = folders[i]
            if curr not in treedata.tree_dict:
                treedata.insert(parent, curr, val, values=[])

        # insert file into tree
        treedata.insert(parent_folder, path, filename, values=[], icon=icon)

    return treedata

