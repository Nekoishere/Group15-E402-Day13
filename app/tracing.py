from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Generator

try:
    from langfuse import observe as _lf_observe, get_client as _lf_get_client

    observe = _lf_observe

    @contextmanager
    def propagate_attributes(**kwargs: Any) -> Generator[None, None, None]:
        """Set trace-level attributes (user_id, session_id, tags) on current trace."""
        try:
            client = _lf_get_client()
            obs = client.get_current_observation()
            if obs and hasattr(obs, 'update'):
                obs.update(**{k: v for k, v in kwargs.items()
                              if k in ('user_id', 'session_id', 'tags')})
        except Exception:
            pass
        yield

    def get_client():
        return _lf_get_client()

    # Keep langfuse_context shim for any legacy usage
    class _LangfuseContextShim:
        def update_current_trace(self, **kwargs: Any) -> None:
            try:
                obs = _lf_get_client().get_current_observation()
                if obs and hasattr(obs, 'update'):
                    obs.update(**{k: v for k, v in kwargs.items()
                                  if k in ('user_id', 'session_id', 'tags')})
            except Exception:
                pass

        def update_current_observation(self, **kwargs: Any) -> None:
            try:
                obs = _lf_get_client().get_current_observation()
                if obs and hasattr(obs, 'update'):
                    obs.update(**kwargs)
            except Exception:
                pass

    langfuse_context = _LangfuseContextShim()

except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):  # type: ignore[misc]
        def decorator(func):
            return func
        return decorator

    @contextmanager
    def propagate_attributes(**kwargs: Any) -> Generator[None, None, None]:  # type: ignore[misc]
        yield

    class _DummyObservation:
        def __enter__(self) -> "_DummyObservation":
            return self

        def __exit__(self, *args: Any) -> None:
            return None

        def update(self, **kwargs: Any) -> None:
            return None

    class _DummyClient:
        def get_current_observation(self) -> None:
            return None

        def start_as_current_observation(self, **kwargs: Any) -> _DummyObservation:
            return _DummyObservation()

        def shutdown(self) -> None:
            return None

        def flush(self) -> None:
            return None

    def get_client() -> _DummyClient:  # type: ignore[misc]
        return _DummyClient()

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()  # type: ignore[assignment]


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
