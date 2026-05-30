# Task Checklist - Implement Webhook Routing Architecture

- [x] Implement new Dialogflow CX webhook endpoints in `main.py`
  - [x] Add `/webhook/wismo-lookup` route (Zendesk lookup helper)
  - [x] Add `/webhook/faq-lookup` route (grounded FAQ placeholder / referral link helper)
- [x] Update `RECEPTIONIST_SOP.md` with schema definitions and instructions for the new endpoints
- [x] Verify the python code using a compiler/syntax check
- [x] Manually test the new webhook routes with mock requests
- [x] Create/update `walkthrough.md` to summarize implementation details and test results

# Task Checklist - Verify Status Report (MCP Audit Suite)

- [ ] Execute programmatic handshakes and sweep system processes using `verify_mcp_connections.py`
  - [ ] Terminate background zombie processes mapping to PPID 1 matching server signatures
  - [ ] Run pre-flight JSON-RPC handshakes on stdio servers (`supermemory`, `exa`, `toon-mcp`) and output active tool names
  - [ ] Apply **Rule 1 (Dynamic Header Validation)** to skip checking Supabase SSE when credentials are missing to avoid initialization hangs
- [ ] Implement and verify policy boundaries inside `native_orchestrator.py:get_policies_for_role`
  - [ ] Block list directory operations on broad search queries
  - [ ] Ban write tools for file alterations without active implementation plans
  - [ ] Restrict orchestrator and auditor capabilities to designated file and command boundaries
- [ ] Compile and output programmatic status summary to `system_status_report.md`
- [ ] Run python compiler check: `/home/dnguyen029/.venv/bin/python -m py_compile verify_mcp_connections.py native_orchestrator.py`
- [ ] Execute full integration test CLI: `python native_orchestrator.py "verify status report"`
