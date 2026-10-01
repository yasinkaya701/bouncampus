# BOUNCAMPUS Cafeteria Data Lab

This directory is the CS1 research surface for building a defensible cafeteria demand / production recommendation dataset.

## Current public-data coverage

- Full January 2026 lunch+dinner seed: **62 service rows**.
- Current official daily semantic-role snapshot for 2026-10-01: lunch, dinner, package lunch, package dinner.
- Verified archive index covering monthly, package and breakfast menu families across multiple 2025–2026 periods.
- Official-dish registry seed with exact kcal / portion / ingredient records where the university exposes them.
- Official category-only records for additional soups, mains, vegan/vegetarian foods, sides and desserts.
- Model feature/target contract.
- Private export request schema for the outcome variables required for a serious forecast.

This is a seed, not a claim that every historic menu page has already been exhaustively materialized.

## Files

### Raw/public source snapshots

- `public_menu_seed_2026_01_01_to_16.csv`
- `public_menu_seed_2026_01_17_to_31.csv`
- `public_daily_roles_2026_10_01.csv`
- `archive_index.csv`

### Label/reference layers

- `official_dish_registry_seed.csv`
- `label_taxonomy.md`
- `model_feature_contract.csv`
- `source_manifest.csv`

### Modeling / acquisition design

- `modeling_plan.md`
- `private_export_request_schema.csv`

## Label pipeline

Run from repository root.

```bash
python scripts/cafeteria_labeler.py \
  --menu-csv research/cafeteria/public_menu_seed_2026_01_01_to_16.csv \
  --dish-output research/cafeteria/derived/jan_a_dishes.csv \
  --service-output research/cafeteria/derived/jan_a_services.csv
```

Repeat for the second half or any new normalized menu file.

Build an active-review queue:

```bash
python scripts/cafeteria_review_queue.py \
  research/cafeteria/public_menu_seed_2026_01_01_to_16.csv \
  research/cafeteria/public_menu_seed_2026_01_17_to_31.csv \
  --output research/cafeteria/manual_label_queue.csv
```

Run focused regression checks:

```bash
python scripts/test_cafeteria_labeler.py
```

## Labeling rule

Priority:

`OFFICIAL_DISH_PAGE > OFFICIAL_MENU_ROLE > OFFICIAL_CATEGORY_INDEX > NAME_RULE_HEURISTIC > UNKNOWN`

A model may use heuristics, but the provenance is retained so we can ablate them or exclude low-confidence features.

Popularity is never manually invented. Dish popularity is learned later from historical demand residuals or item-choice observations.

## Serious-model prerequisite

Public menu data can build context features, but the supervised production model requires real outcomes. P0 institutional export fields are:

1. actual served count by campus/date/service,
2. prepared count,
3. waste kg or waste portions,
4. reservations at the decision cutoff.

Strong additions are reserved-served, unreserved-served, sellout, decision-freeze timestamps and operator plan/override records.

Until those exist, model outputs stay offline/sandbox and must not be sold as demonstrated waste reduction.

## Recommended growth order

1. Materialize all reachable 2025–2026 monthly menus.
2. Materialize package menus and breakfast as separate service regimes.
3. Crawl canonical official dish pages referenced by menus.
4. Grow the exact ingredient/kcal/portion registry.
5. Resolve high-frequency manual-label queue items.
6. Join academic calendar.
7. Join decision-time weather forecast snapshots.
8. Obtain and reconcile institutional served/prepared/waste/reservation outcomes.
9. Run baseline-first expanding-window benchmarks.
10. Promote complexity only if it improves future-time decision loss.

## Truth boundary

- Menu and official dish-page fields are `OFFICIAL_PUBLIC`.
- Rule labels are `NAME_RULE_HEURISTIC`.
- LCA classes are external proxies, not measured Boğaziçi carbon/water impact.
- `NOT_LISTED_OFFICIAL` means absent from the exposed official ingredient list, not allergy-safe.
- Outcome metrics do not exist until real operational data is imported and reconciled.
