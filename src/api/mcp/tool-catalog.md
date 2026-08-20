# MCP Tool Boundary

Milestone 14 defines a future MCP-compatible boundary for read-focused AI/tool consumers. It is not an autonomous agent and it does not expose arbitrary SQL, arbitrary URLs, shell execution, filesystem access, or destructive operations.

Tools:

- `get_shipment_status`
- `get_shipment_history`
- `get_route_context`
- `search_operational_knowledge`
- `ask_grounded_operations_question`

Every tool maps to an allowlisted API or stored procedure, requires an application role, uses strict JSON schemas, propagates identity where supported, and emits auditable correlation metadata.

