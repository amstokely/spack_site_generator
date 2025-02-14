import yaml
from typing import Dict, Any


def convert_to_spack_yaml(
        yaml_data: Dict[str, Any]
) -> str:
    """
    Convert a dictionary to a YAML-formatted string, applying Spack-specific formatting.

    This function modifies the YAML output by adding double colons (`::`) 
    to keys that have the attribute `override: true` in their subfields, 
    ensuring compatibility with Spack's configuration format.

    Args:
        yaml_data (Dict[str, Any]): The dictionary to convert.

    Returns:
        str: The formatted YAML string.
    """
    yaml_lines = yaml.dump(
        yaml_data,
        default_flow_style=False,
        sort_keys=False
    ).splitlines()

    formatted_lines = []
    line_index = 0

    while line_index < len(yaml_lines):
        if (line_index < len(yaml_lines) - 2 and "override: true" in
                yaml_lines[line_index + 2]):
            key = yaml_lines[line_index].split(":")[0]
            formatted_lines.append(f"{key}:: \n{yaml_lines[line_index + 1]}")
            line_index += 3
        elif (line_index < len(yaml_lines) - 1 and "override: true" in
              yaml_lines[line_index + 1]):
            key = yaml_lines[line_index].split(":")[0]
            formatted_lines.append(f"{key}::")
            line_index += 2
        else:
            formatted_lines.append(yaml_lines[line_index])
            line_index += 1

    return "\n".join(formatted_lines)


def to_yaml(
        yaml_data: Dict[str, Any],
        spack_format: bool = True
) -> str:
    """
    Convert a dictionary to a YAML-formatted string.

    Args:
        yaml_data (Dict[str, Any]): The dictionary to convert.
        spack_format (bool, optional): Whether to apply Spack-specific formatting.
                                       Defaults to True.

    Returns:
        str: The formatted YAML string.
    """
    if spack_format:
        return convert_to_spack_yaml(yaml_data)
    return yaml.dump(yaml_data,
                     default_flow_style=False,
                     sort_keys=False
                     )
