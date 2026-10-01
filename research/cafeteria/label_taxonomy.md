# Cafeteria Menu Label Taxonomy

Purpose: turn raw Boğaziçi menu text into reproducible model features without converting guesses into facts.

## Evidence hierarchy

Every label carries `label_provenance` and `label_confidence`.

1. `OFFICIAL_DISH_PAGE` — official Boğaziçi dish page gives category, kcal, portion and/or ingredients.
2. `OFFICIAL_MENU_ROLE` — official daily page explicitly places a dish under Çorba / Ana Yemek / Vejetaryen-Vegan / Yardımcı / Seçmeli.
3. `OFFICIAL_CATEGORY_INDEX` — official food-photo/category index lists the dish under a category.
4. `NAME_RULE_HEURISTIC` — transparent rule from the dish name only.
5. `UNKNOWN` — do not force a label.

A heuristic label must never overwrite an official label.

## Core dish labels

### `dish_role`

Allowed values:

- `SOUP`
- `MAIN_ANIMAL`
- `MAIN_PLANT`
- `SIDE_STARCH`
- `SIDE_VEGETABLE`
- `SALAD_COLD`
- `DESSERT`
- `BEVERAGE`
- `FRUIT`
- `BREAD_BAKERY`
- `CONDIMENT`
- `UNKNOWN`

### `protein_class`

- `RED_MEAT`
- `POULTRY`
- `FISH`
- `LEGUME`
- `EGG`
- `DAIRY_DOMINANT`
- `MIXED_ANIMAL`
- `PLANT_OTHER`
- `NONE`
- `UNKNOWN`

### `diet_class`

Use only evidence-supported values:

- `VEGAN_EXPLICIT`
- `VEGETARIAN_EXPLICIT`
- `ANIMAL_BASED`
- `PLANT_BASED_HEURISTIC`
- `UNKNOWN`

`PLANT_BASED_HEURISTIC` is not equivalent to certified vegan. Cross-contact and hidden ingredients remain unknown.

### `preparation_class`

Multi-label string separated by `|`:

- `FRIED`
- `BAKED`
- `GRILLED`
- `STEWED`
- `BOILED`
- `RAW_COLD`
- `PASTRY`
- `SANDWICH`
- `UNKNOWN`

### ingredient-derived flags

Each is tri-state: `PRESENT`, `NOT_LISTED_OFFICIAL`, `UNKNOWN`.

- `contains_dairy`
- `contains_egg`
- `contains_gluten_source`
- `contains_legume`
- `contains_red_meat`
- `contains_poultry`
- `contains_fish`

`NOT_LISTED_OFFICIAL` is allowed only when an official ingredient list exists and the ingredient family is absent from that list. It is not an allergy-safety guarantee.

## Sustainability proxy labels

These are ranking features, not measured campus impacts.

### `carbon_intensity_proxy`

- `VERY_HIGH_PROXY` — beef/lamb-heavy dish
- `HIGH_PROXY` — mixed red-meat dish
- `MEDIUM_PROXY` — poultry/fish/dairy-heavy dish
- `LOW_PROXY` — legume/vegetable/starch dominant
- `UNKNOWN`

### `water_intensity_proxy`

Same qualitative scale, kept separate from carbon. Do not translate to liters without a sourced LCA mapping.

All proxy labels use `DERIVED_LCA_CLASS`, never `MEASURED_CAMPUS_IMPACT`.

## Menu-level features

For every service (campus × date × meal), aggregate:

- `menu_item_count`
- `has_red_meat_main`
- `has_poultry_main`
- `has_fish_main`
- `has_explicit_vegan_option`
- `has_legume_option`
- `dessert_count`
- `sugary_drink_count`
- `starch_option_count`
- `vegetable_option_count`
- `mean_known_kcal`
- `known_kcal_coverage`
- `mean_known_portion_g`
- `known_portion_coverage`
- `max_carbon_proxy_ordinal`
- `menu_text_canonical`
- `menu_signature`

The recommendation model can use these features, but no feature may be created from post-service data.

## Popularity labels

Do **not** label a food `popular` from intuition. Popularity requires one of:

- observed item choice counts,
- item-level reservations,
- repeated service-level uplift after controlling for calendar/weather/campus,
- survey choice data with provenance.

Until then use `popularity_status=UNOBSERVED`.

## Allergen boundary

This pipeline is not an allergy-safety system. Ingredient-derived flags can support modeling and exploratory filtering, but must not be presented as medical-grade allergen declarations unless verified by the food service authority.

## Leakage boundary

Forbidden as model inputs for a decision made before service:

- actual served count,
- post-service waste,
- observed queue length after service begins,
- final item depletion,
- post-hoc survey score,
- realized weather when only forecast was available at decision time.

These may be labels/outcomes for training and evaluation only.