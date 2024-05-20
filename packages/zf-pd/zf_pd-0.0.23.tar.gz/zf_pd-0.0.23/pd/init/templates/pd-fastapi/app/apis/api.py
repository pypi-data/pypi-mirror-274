from typing import Dict

from ..model import Example


def example(e: Example) -> Dict[str, str]:
    return dict(msg=e.msg)
