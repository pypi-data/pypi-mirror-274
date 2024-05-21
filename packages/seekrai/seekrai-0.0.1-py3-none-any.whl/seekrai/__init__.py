from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable

from seekrai import (
    abstract,
    client,
    constants,
    error,
    filemanager,
    resources,
    seekrflow_response,
    types,
    utils,
)
from seekrai.version import VERSION


version = VERSION

log: str | None = None  # Set to either 'debug' or 'info', controls console logging

if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

requestssession: "requests.Session" | Callable[[], "requests.Session"] | None = None

aiosession: ContextVar["ClientSession" | None] = ContextVar(
    "aiohttp-session", default=None
)

from seekrai.client import AsyncClient, AsyncSeekrFlow, Client, SeekrFlow


api_key: str | None = None  # To be deprecated in the next major release

# Legacy functions
from seekrai.legacy.complete import AsyncComplete, Complete, Completion
from seekrai.legacy.embeddings import Embeddings
from seekrai.legacy.files import Files
from seekrai.legacy.finetune import Finetune
from seekrai.legacy.images import Image
from seekrai.legacy.models import Models


__all__ = [
    "aiosession",
    "constants",
    "version",
    "SeekrFlow",
    "AsyncSeekrFlow",
    "Client",
    "AsyncClient",
    "resources",
    "types",
    "abstract",
    "filemanager",
    "error",
    "seekrflow_response",
    "client",
    "utils",
]
