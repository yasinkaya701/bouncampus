# Food-demand v2 prospective validation

Historical records are development data. The 16:00 Europe/Istanbul D-1 replay assumes an outcome dated D-2 is available by the cutoff because operational row-arrival timestamps were not supplied. That assumption must remain labeled `ASSUMED_NEXT_DAY_12_LOCAL`; it is not a verified ingestion SLA.

A prospective validation starts only after the candidate code, feature set, candidate set, model parameters, cutoff, scoring support, and data source hashes are frozen. Use 56 consecutive target dates. At 16:00 Europe/Istanbul on each D-1:

1. Build the snapshot from rows whose source availability timestamp is at or before the cutoff. Record the source checksum and maximum service date used. If timestamps remain unavailable, state the assumed next-day-at-12 availability rule in every daily ledger row.
2. Emit one ledger row for each campus/meal target, including unavailable groups. Preserve missing values as missing; keep explicit zero observations as zero. Do not use a later menu, notice, holiday-calendar revision, or realized-weather value. Admit a notice only with a publication timestamp before cutoff and reviewed, explicit service fields. Admit weather only from an archived forecast vintage issued before cutoff.
3. Keep each ledger immutable with target date, campus, meal, cutoff, prediction, model/version, training-data hash, coverage, source assumptions, and status. Do not overwrite forecasts with later reruns.
4. At the documented outcome-availability time, join realized outcomes by exact campus/meal/date. Do not substitute Planlanan counts, reservation intent, or estimates for realized demand.
5. Refit weekly only with data that had become available by each cutoff. Do not change features, candidates, hyperparameters, or blend rules based on scores from the 56-day window.
6. Score all candidates on the same rows and report original-count WAPE, MAE, signed bias, coverage, campus and meal breakdowns, and a date-cluster bootstrap interval. Report the plan comparator on its own matched support and label it unvintaged if its issue time is unknown.

The 5% acceptance result is eligible to be described as prospectively verified only when all 56 dates are complete, source/outcome provenance is accepted, the score uses the frozen scoring support, and the resulting WAPE is at most 5%. Until then, report the exact offline development WAPE and label prospective validation `NOT_COMPLETED`.
