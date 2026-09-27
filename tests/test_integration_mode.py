import unittest

from integration_mode import resolve_integration_mode


class IntegrationModeTests(unittest.TestCase):
    def test_supported_async_signatures_enable_full_integration_in_auto_mode(self):
        async def execute_v10(
            server,
            dynprompt,
            caches,
            current_item,
            extra_data,
            executed,
            prompt_id,
            execution_list,
            pending_subgraph_results,
            pending_async_nodes,
        ):
            pass

        async def execute_v11(
            server,
            dynprompt,
            caches,
            current_item,
            extra_data,
            executed,
            prompt_id,
            execution_list,
            pending_subgraph_results,
            pending_async_nodes,
            ui_outputs,
        ):
            pass

        self.assertTrue(resolve_integration_mode(execute_v10, "auto")[0])
        self.assertTrue(resolve_integration_mode(execute_v11, "auto")[0])

    def test_unknown_async_signature_falls_back_to_nodes_only(self):
        async def execute_current(
            server,
            dynprompt,
            caches,
            current_item,
            extra_data,
            executed,
            prompt_id,
            execution_list,
            pending_subgraph_results,
            pending_async_nodes,
            ui_outputs,
            asset_manager,
        ):
            pass

        enabled, reason = resolve_integration_mode(execute_current, "auto")

        self.assertFalse(enabled)
        self.assertIn("asset_manager", reason)

    def test_explicit_modes_override_auto_detection(self):
        async def execute_current(*args, **kwargs):
            pass

        self.assertTrue(resolve_integration_mode(execute_current, "full")[0])
        self.assertFalse(resolve_integration_mode(execute_current, "nodes")[0])

    def test_invalid_mode_fails_safe(self):
        async def execute_supported(
            server,
            dynprompt,
            caches,
            current_item,
            extra_data,
            executed,
            prompt_id,
            execution_list,
            pending_subgraph_results,
            pending_async_nodes,
        ):
            pass

        enabled, reason = resolve_integration_mode(execute_supported, "invalid")

        self.assertFalse(enabled)
        self.assertIn("invalid", reason)


if __name__ == "__main__":
    unittest.main()
