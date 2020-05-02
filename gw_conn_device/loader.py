import yaml
import logging
from typing import Dict, Iterator, List, TypeVar, Union, overload

_LOGGER = logging.getLogger(__name__)
JSON_TYPE = Union[List, Dict, str]  # pylint: disable=invalid-name

class SafeLineLoader(yaml.SafeLoader):
    """Loader class that keeps track of line numbers."""
    def compose_node(self, parent: yaml.nodes.Node, index: int) -> yaml.nodes.Node:
        """Annotate a node with the first line it was seen."""
        last_line: int = self.line
        node: yaml.nodes.Node = super().compose_node(parent, index)
        node.__line__ = last_line + 1  # type: ignore
        return node

def load_yaml(fname: str) -> JSON_TYPE:
    """Load a YAML file."""
    try:
        with open(fname, encoding="utf-8") as conf_file:
            # If configuration file is empty YAML returns None
            # We convert that to an empty dict
            return yaml.load(conf_file, Loader=SafeLineLoader) or OrderedDict()
    except yaml.YAMLError as exc:
        _LOGGER.error(str(exc))
        return "error"
        #raise HomeAssistantError(exc)
    except UnicodeDecodeError as exc:
        _LOGGER.error("Unable to read file %s: %s", fname, exc)
        #raise HomeAssistantError(exc)
        return "error"