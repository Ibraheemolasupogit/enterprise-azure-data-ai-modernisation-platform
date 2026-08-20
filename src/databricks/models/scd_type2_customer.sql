MERGE INTO ${catalog}.gold.dim_customer AS target
USING ${catalog}.silver.customer_accounts_staged AS source
ON target.customer_id = source.customer_id
AND target.is_current = true
WHEN MATCHED AND target.change_hash <> source.change_hash THEN
  UPDATE SET
    target.effective_end_utc = source.effective_start_utc,
    target.is_current = false
WHEN NOT MATCHED THEN
  INSERT (
    customer_sk,
    customer_id,
    account_number,
    legal_name,
    service_tier,
    billing_region,
    effective_start_utc,
    effective_end_utc,
    is_current,
    change_hash
  )
  VALUES (
    source.customer_sk,
    source.customer_id,
    source.account_number,
    source.legal_name,
    source.service_tier,
    source.billing_region,
    source.effective_start_utc,
    TIMESTAMP '9999-12-31 00:00:00',
    true,
    source.change_hash
  );

