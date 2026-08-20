# SQL MI Authentication Failure

## Trigger

Repeated failed login alert or application identity failure.

## Triage

- Identify principal, source IP, application, and database.
- Confirm Entra group membership or managed identity assignment.
- Check recent secret, role, or deployment changes.

## Evidence

- Audit event.
- Principal mapping.
- Role membership.
- Application deployment version.

## Action

- Restore expected role membership through approved identity process.
- Do not grant direct ad hoc privileges.
- Escalate suspicious activity to security.

## Escalation

Escalate repeated unknown-source failures to security.

## Validation

- Expected principal authenticates.
- No unintended role expansion occurred.

## Closure

Record cause, identity change, and access review note.

