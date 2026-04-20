from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Generator

try:
    from langfuse import observe, propagate_attributes, get_client
except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    @contextmanager
    def propagate_attributes(**kwargs: Any) -> Generator[None, None, None]:
        yield

    class _DummyObservation:
        def __enter__(self) -> "_DummyObservation":
            return self

        def __exit__(self, *args: Any) -> None:
            return None

    class _DummyClient:
        def shutdown(self) -> None:
            return None

        def flush(self) -> None:
            return None

        def start_as_current_observation(self, **kwargs: Any) -> _DummyObservation:
            return _DummyObservation()

    def get_client() -> _DummyClient:
        return _DummyClient()


def tracing_enabled() -> bool:
    if os.getenv("LANGFUSE_TRACING_ENABLED", "").lower() == "false":
        return False
    return bool(
        os.getenv("LANGFUSE_PUBLIC_KEY")
        and os.getenv("LANGFUSE_SECRET_KEY")
        and (os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST"))
    )
