CREATE SCHEMA IF NOT EXISTS billing_ops;

CREATE TABLE billing_ops.invoice (
    invoice_id text PRIMARY KEY,
    shipment_id text NOT NULL,
    customer_ref text NOT NULL,
    invoice_date date NOT NULL,
    due_date date NOT NULL,
    invoice_status text NOT NULL,
    net_amount_gbp numeric(12, 2) NOT NULL,
    tax_amount_gbp numeric(12, 2) NOT NULL,
    legacy_attributes jsonb DEFAULT '{}'::jsonb,
    migrated_at timestamptz NULL
);

CREATE TABLE billing_ops.payment (
    payment_id text PRIMARY KEY,
    invoice_id text NOT NULL REFERENCES billing_ops.invoice(invoice_id),
    paid_date date NOT NULL,
    payment_method text NOT NULL,
    amount_gbp numeric(12, 2) NOT NULL,
    legacy_batch_id text NOT NULL,
    migrated_at timestamptz NULL
);

CREATE TABLE billing_ops.service_case (
    case_id text PRIMARY KEY,
    customer_id text NOT NULL,
    shipment_id text NOT NULL,
    case_reason text NOT NULL,
    case_status text NOT NULL,
    opened_at timestamptz NOT NULL,
    closed_at timestamptz NULL,
    contact_email text NULL,
    migrated_at timestamptz NULL
);

CREATE TABLE billing_ops.case_note (
    case_note_id text PRIMARY KEY,
    case_id text NOT NULL REFERENCES billing_ops.service_case(case_id),
    note_sequence integer NOT NULL,
    note_timestamp timestamptz NOT NULL,
    agent_team text NOT NULL,
    note_text text NOT NULL,
    migrated_at timestamptz NULL
);

CREATE INDEX ix_invoice_customer_ref ON billing_ops.invoice (customer_ref);
CREATE INDEX ix_invoice_shipment_id ON billing_ops.invoice (shipment_id);
CREATE INDEX ix_service_case_shipment_id ON billing_ops.service_case (shipment_id);

