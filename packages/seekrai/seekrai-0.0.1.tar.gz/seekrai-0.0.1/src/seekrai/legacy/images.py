import warnings
from typing import Any, Dict

import seekrai
from seekrai.legacy.base import API_KEY_WARNING, deprecated


class Image:
    @classmethod
    @deprecated  # type: ignore
    def create(
        cls,
        prompt: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Legacy image function."""

        api_key = None
        if seekrai.api_key:
            warnings.warn(API_KEY_WARNING)
            api_key = seekrai.api_key

        client = seekrai.SeekrFlow(api_key=api_key)

        return client.images.generate(prompt=prompt, **kwargs).model_dump()
