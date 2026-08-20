-- Structured Streaming progress is normally inspected from stream progress/event logs.
-- Persist selected progress fields into an audit Delta table before querying this view.
SELECT
  stream_name,
  batch_id,
  input_rows_per_second,
  processed_rows_per_second,
  event_time_watermark,
  state_rows_total,
  checkpoint_age_minutes,
  late_record_count,
  duplicate_record_count,
  last_progress_at_utc
FROM contoso_freight_prod.audit.streaming_progress
WHERE last_progress_at_utc >= current_timestamp() - INTERVAL 1 DAY;

