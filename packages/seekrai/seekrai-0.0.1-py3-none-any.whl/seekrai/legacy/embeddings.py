import warnings
from typing import Any, Dict

import seekrai
from seekrai.legacy.base import API_KEY_WARNING, deprecated


class Embeddings:
    @classmethod
    @deprecated  # type: ignore
    def create(
        cls,
        input: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Legacy embeddings function."""

        api_key = None
        if seekrai.api_key:
            warnings.warn(API_KEY_WARNING)
            api_key = seekrai.api_key

        client = seekrai.SeekrFlow(api_key=api_key)

        return client.embeddings.create(input=input, **kwargs).model_dump()
