from typing import Any, Dict, Union


class AutoDict(dict):
    """
    A dictionary subclass that automatically creates nested dictionaries
    for missing keys and converts standard dictionaries into AutoDict instances.

    This allows for easy access to deeply nested structures without needing
    to initialize each level manually.

    Example:
        >>> data = AutoDict()
        >>> data["config"]["settings"]["theme"] = "dark"
        >>> print(data)
        {'config': {'settings': {'theme': 'dark'}}}
    """

    def __getitem__(self, key: str) -> Union["AutoDict", Any]:
        """
        Retrieve the value associated with the given key.
        If the key does not exist, an AutoDict instance is created and returned.
        """
        if key not in self:
            self[key] = AutoDict()
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a value in the dictionary. If the value is a dictionary
        (at any level), it is automatically converted to AutoDict recursively.
        """
        if isinstance(value, dict) and not isinstance(value, AutoDict):
            value = AutoDict._convert_recursive(value)
        super().__setitem__(key, value)

    @staticmethod
    def _convert_recursive(d: Dict[str, Any]) -> "AutoDict":
        """
        Recursively convert all nested dicts into AutoDicts.
        """
        auto = AutoDict()
        for k, v in d.items():
            if isinstance(v, dict) and not isinstance(v, AutoDict):
                auto[k] = AutoDict._convert_recursive(v)
            else:
                auto[k] = v
        return auto

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the AutoDict instance into a standard dictionary, ensuring
        all nested AutoDict instances are also converted.
        """
        return {
            key: (value.to_dict() if isinstance(value, AutoDict) else value)
            for key, value in self.items()
        }

    def empty(self) -> bool:
        """Return True if the AutoDict is empty, False otherwise."""
        return not bool(self)
