-- Force a known good plan only after evidence review.
EXEC sys.sp_query_store_force_plan
    @query_id = 0,
    @plan_id = 0;

-- Remove forced plan after permanent mitigation or if forcing causes regression.
EXEC sys.sp_query_store_unforce_plan
    @query_id = 0,
    @plan_id = 0;

-- Query Store hint example. Replace query_id only after evidence review.
EXEC sys.sp_query_store_set_hints
    @query_id = 0,
    @value = N'OPTION(RECOMPILE)';

-- Clear Query Store hint safely.
EXEC sys.sp_query_store_clear_hints
    @query_id = 0;

