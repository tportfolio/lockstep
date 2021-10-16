class Enum(set):
    """
    Wrapper class for self-named enums.
    See: https://stackoverflow.com/a/2182437
    """
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


CallbackKey = Enum([
    "SETTINGS",
    "EVALUATE",
    "SYNCHRONIZE",
    "SOURCE_FOLDER",
    "DESTINATION_FOLDER",
    "SYNC_DROPDOWN"
])

