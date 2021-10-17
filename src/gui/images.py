from os.path import dirname, join
import base64


def load_image(path) -> bytes:
    return base64.b64encode(open(join(dirname(__file__), path), 'rb').read())


# credit to MUI for original SVG paths of these icons
LOCK_ICON = load_image("res/png/lock.png")
ADD_ICON = load_image("res/png/add.png")
REMOVE_ICON = load_image("res/png/remove.png")



