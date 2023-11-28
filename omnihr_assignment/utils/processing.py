import json
from typing import Dict

def _dumps_dict_for_hash_map(data: Dict) -> Dict:
        formatted = {}
        for k, v in data.items():
            if isinstance(v, (list, tuple, dict, bool)) or v in (None,):
                try:
                    formatted[k] = json.dumps(v)
                except ValueError:
                    formatted[k] = v
            else:
                formatted[k] = v
        return formatted

def _loads_dict_for_hash_map(data: Dict) -> Dict:
    formatted = {}
    for k, v in data.items():
        try:
            formatted[k.decode()] = json.loads(v)
        except ValueError:
            formatted[k] = v
    return formatted