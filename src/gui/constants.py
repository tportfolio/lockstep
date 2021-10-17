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
    "EVALUATE",
    "EVALUATION_COMPLETE",
    "SYNCHRONIZE",
    "SOURCE_FOLDER",
    "SOURCE_TREE",
    "DESTINATION_FOLDER",
    "DESTINATION_TREE",
    "SYNC_DROPDOWN",
    "TAB_GROUP"
])

SyncOptions = {
    "ONE_WAY": "One-way",
    "TWO_WAY": "Two-way",
    "UPDATE": "Update",
}
