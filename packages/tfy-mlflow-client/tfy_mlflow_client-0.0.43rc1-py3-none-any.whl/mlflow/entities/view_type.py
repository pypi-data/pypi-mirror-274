class ViewType:
    """Enum to filter requested experiment types."""

    ACTIVE_ONLY, DELETED_ONLY, HARD_DELETED_ONLY, ALL = range(1, 5)
    # TODO: Sort this out later
    _VIEW_TO_STRING = {
        ACTIVE_ONLY: "ACTIVE_ONLY",
        DELETED_ONLY: "DELETED_ONLY",
        HARD_DELETED_ONLY: "HARD_DELETED_ONLY",
        ALL: "ALL",
    }
    _STRING_TO_VIEW = {value: key for key, value in _VIEW_TO_STRING.items()}

    @classmethod
    def from_string(cls, view_str):
        if view_str not in cls._STRING_TO_VIEW:
            raise Exception(
                "Could not get valid view type corresponding to string %s. "
                "Valid view types are %s" % (view_str, list(cls._STRING_TO_VIEW.keys()))
            )
        return cls._STRING_TO_VIEW[view_str]

    @classmethod
    def to_string(cls, view_type):
        if view_type not in cls._VIEW_TO_STRING:
            raise Exception(
                "Could not get valid view type corresponding to string %s. "
                "Valid view types are %s" % (view_type, list(cls._VIEW_TO_STRING.keys()))
            )
        return cls._VIEW_TO_STRING[view_type]
