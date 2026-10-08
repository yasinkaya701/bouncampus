# Optional model candidates

The core shadow pipeline depends only on the repository's normal backend environment. CatBoost is the required learned candidate; Chronos-2 and TabPFN-TS are optional, and an unavailable checkpoint never blocks core forecasting.

Chronos-2 uses `chronos==2.3.2` with the public `amazon/chronos-2` checkpoint. Checkpoint downloads are initiated explicitly by the local runner; all inference remains local. The adapter requires a complete contiguous daily context and evaluates two steps ahead from D-2, selecting D. Missing dates are not filled with invented demand.

TabPFN-TS is an optional `tabpfn-time-series==1.3.0` candidate using TabPFN-TS 3.5. It is not a hard dependency. The verified API uses `TabPFNTSPipeline(tabpfn_mode=TabPFNMode.LOCAL, tabpfn_output_selection="median", max_context_length=...)`; set `TABPFN_DISABLE_TELEMETRY=1` before importing or initializing the package. Do not use `TabPFNMode.CLIENT` or send operational records to a hosted service. Local use requires the v3.5 checkpoint and the applicable license acceptance. If either is unavailable, record `NOT_RUN` and do not attempt inference. The isolated development environment used for this implementation lacked the checkpoint; no license was accepted.

Candidate statuses distinguish package/checkpoint readiness from scored forecasts. A loaded model with no valid context has no score and cannot enter the blend. Historical model scores remain development evidence; the prospective 56-day gate is documented in [PROSPECTIVE_VALIDATION.md](PROSPECTIVE_VALIDATION.md).
