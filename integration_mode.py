import asyncio
import inspect
import os

INTEGRATION_MODE_ENV = "COMFYUI_DEPLOY_INTEGRATION_MODE"

_BASE_PARAMS = (
    "server",
    "dynprompt",
    "caches",
    "current_item",
    "extra_data",
    "executed",
    "prompt_id",
    "execution_list",
    "pending_subgraph_results",
)
_SUPPORTED_ASYNC_SIGNATURES = {
    _BASE_PARAMS + ("pending_async_nodes",),
    _BASE_PARAMS + ("pending_async_nodes", "ui_outputs"),
}
_SUPPORTED_SYNC_SIGNATURES = {_BASE_PARAMS}


def resolve_integration_mode(execute_fn, mode=None):
    """Return (enable_full_integration, reason).

    In ``auto`` mode we only enable the route/frontend integration when the
    installed ComfyUI ``execution.execute`` signature matches a contract that
    this plugin's execution wrapper actually forwards.
    """
    requested = (
        mode if mode is not None else os.environ.get(INTEGRATION_MODE_ENV, "auto")
    )
    requested = str(requested).strip().lower()

    if requested == "full":
        return True, "full integration forced by environment"
    if requested == "nodes":
        return False, "node-only mode forced by environment"
    if requested != "auto":
        return (
            False,
            f"invalid {INTEGRATION_MODE_ENV}={requested!r}; using node-only mode",
        )

    try:
        parameters = tuple(inspect.signature(execute_fn).parameters)
    except (TypeError, ValueError):
        return False, "unable to inspect ComfyUI execution.execute; using node-only mode"

    supported = (
        parameters in _SUPPORTED_ASYNC_SIGNATURES
        if asyncio.iscoroutinefunction(execute_fn)
        else parameters in _SUPPORTED_SYNC_SIGNATURES
    )
    if supported:
        return True, "ComfyUI execution.execute signature is supported"

    return (
        False,
        "unsupported ComfyUI execution.execute signature "
        f"{parameters!r}; using node-only mode",
    )
