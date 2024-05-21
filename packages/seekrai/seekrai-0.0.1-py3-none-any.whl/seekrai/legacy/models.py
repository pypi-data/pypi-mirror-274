import warnings
from typing import Any, Dict, List

import seekrai
from seekrai.legacy.base import API_KEY_WARNING, deprecated


class Models:
    @classmethod
    @deprecated  # type: ignore
    def list(
        cls,
    ) -> List[Dict[str, Any]]:
        """Legacy model list function."""

        api_key = None
        if seekrai.api_key:
            warnings.warn(API_KEY_WARNING)
            api_key = seekrai.api_key

        client = seekrai.SeekrFlow(api_key=api_key)

        return [item.model_dump() for item in client.models.list()]

    @classmethod
    @deprecated  # type: ignore
    def info(
        cls,
        model: str,
    ) -> Dict[str, Any]:
        """Legacy model info function."""

        api_key = None
        if seekrai.api_key:
            warnings.warn(API_KEY_WARNING)
            api_key = seekrai.api_key

        client = seekrai.SeekrFlow(api_key=api_key)

        model_list = client.models.list()

        for item in model_list:
            if item.id == model:
                return item.model_dump()
