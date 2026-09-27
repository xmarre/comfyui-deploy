# ComfyUI compatibility mode

This fork keeps the Comfy Deploy node classes available even when the installed
ComfyUI execution API is newer than the execution wrapper bundled with Comfy
Deploy.

At startup, `COMFYUI_DEPLOY_INTEGRATION_MODE` controls the behavior:

- `auto` (default): enable the Comfy Deploy routes and frontend only when the
  installed `execution.execute` signature matches a contract supported by this
  release. Otherwise, load the nodes only.
- `nodes`: always load the nodes without importing `custom_routes.py` or the
  Comfy Deploy frontend extension.
- `full`: force the complete Comfy Deploy integration.

Node-only mode deliberately does not install the global execution wrapper,
custom HTTP routes, or frontend hooks. Existing workflows can therefore keep
using node types such as `ComfyUIDeployExternalNumber`,
`ComfyUIDeployExternalNumberSlider`, and their integer variants without
depending on a stale execution monkey-patch.

`full` is an override, not a compatibility guarantee. If `auto` selects
node-only mode, use `full` only after validating the ComfyUI execution contract
against this plugin.
