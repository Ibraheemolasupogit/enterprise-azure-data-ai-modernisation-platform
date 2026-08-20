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
    legacy_attributes jsonb DEFAULT '{}'::jsonb
);

CREATE TABLE billing_ops.payment (
    payment_id text PRIMARY KEY,
    invoice_id text NOT NULL REFERENCES billing_ops.invoice(invoice_id),
    paid_date date NOT NULL,
    payment_method text NOT NULL,
    amount_gbp numeric(12, 2) NOT NULL,
    legacy_batch_id text NOT NULL
);

CREATE TABLE billing_ops.service_case (
    case_id text PRIMARY KEY,
    customer_id text NOT NULL,
    shipment_id text NOT NULL,
    case_reason text NOT NULL,
    case_status text NOT NULL,
    opened_at timestamptz NOT NULL,
    closed_at timestamptz NULL,
    contact_email text NULL
);

CREATE INDEX ix_invoice_customer_ref ON billing_ops.invoice (customer_ref);
CREATE INDEX ix_invoice_shipment_id ON billing_ops.invoice (shipment_id);
CREATE INDEX ix_service_case_shipment_id ON billing_ops.service_case (shipment_id);

-- Cross-source pain point: customer_ref uses ACCT-style identifiers while the
-- SQL Server-style OLTP source uses CUST identifiers and account numbers.

