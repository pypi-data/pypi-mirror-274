from __future__ import annotations

from typing import List

from seekrai.abstract import api_requestor
from seekrai.seekrflow_response import SeekrFlowResponse
from seekrai.types import (
    ModelObject,
    SeekrFlowClient,
    SeekrFlowRequest,
)


class Models:
    def __init__(self, client: SeekrFlowClient) -> None:
        self._client = client

    def list(
        self,
    ) -> List[ModelObject]:
        """
        Method to return list of models on the API

        Returns:
            List[ModelObject]: List of model objects
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        assert isinstance(response.data, list)

        return [ModelObject(**model) for model in response.data]


class AsyncModels:
    def __init__(self, client: SeekrFlowClient) -> None:
        self._client = client

    async def list(
        self,
    ) -> List[ModelObject]:
        """
        Async method to return list of models on API

        Returns:
            List[ModelObject]: List of model objects
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        assert isinstance(response.data, list)

        return [ModelObject(**model) for model in response.data]
