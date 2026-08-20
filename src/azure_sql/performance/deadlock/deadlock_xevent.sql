CREATE EVENT SESSION [cf_deadlock_capture] ON DATABASE
ADD EVENT sqlserver.xml_deadlock_report
ADD TARGET package0.ring_buffer
WITH (
    MAX_MEMORY = 4096 KB,
    EVENT_RETENTION_MODE = ALLOW_SINGLE_EVENT_LOSS,
    MAX_DISPATCH_LATENCY = 30 SECONDS,
    STARTUP_STATE = OFF
);

-- Enable only during controlled investigation:
-- ALTER EVENT SESSION [cf_deadlock_capture] ON DATABASE STATE = START;

