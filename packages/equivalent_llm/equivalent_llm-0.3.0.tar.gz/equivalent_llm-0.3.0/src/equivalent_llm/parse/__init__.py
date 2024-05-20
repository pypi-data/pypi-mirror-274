import ast
import json
import logging
import traceback
from typing import Any

def json_loads(content: Any, warning: bool = False) -> Any:
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        try:
            if warning:
                logging.warn(f"### JSON Failed to parse content as JSON: {content}\tERROR: {e}")
            return ast.literal_eval(content)
        except Exception:
            logging.warn(f"Failed to parse content by AST: {content}")
            logging.warn(traceback.extract_stack())
            return {}
