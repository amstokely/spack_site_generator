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

        Args:
            key (str): The key to retrieve.

        Returns:
            Union[AutoDict, Any]: The stored value or a new AutoDict if the key was missing.
        """
        if key not in self:
            self[key] = AutoDict()  # Create a new AutoDict for missing keys
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a value in the dictionary. If the value is a standard dictionary,
        it is automatically converted to an AutoDict.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
        """
        if isinstance(value, dict) and not isinstance(value, AutoDict):
            value = AutoDict(value)  # Convert normal dicts to AutoDict recursively
        super().__setitem__(key, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the AutoDict instance into a standard dictionary, ensuring
        all nested AutoDict instances are also converted.

        Returns:
            Dict[str, Any]: A standard Python dictionary representation.
        """
        return {
            key: (value.to_dict() if isinstance(value, AutoDict) else value)
            for key, value in self.items()
        }
