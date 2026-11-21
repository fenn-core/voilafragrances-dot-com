# VOILA FRAGRANCES

Static Turkish homepage and demonstration catalog for the VOILA FRAGRANCES storefront.

## Local preview

From the repository root, run `python3 -m http.server 8000` and open
`http://localhost:8000/`.

## Catalog build

Run `python3 scripts/build_catalog.py` from the repository root to validate
`data/catalog.json` and generate six static pages. Run
`python3 scripts/build_catalog.py --check` to validate the data and verify the
committed HTML is current without writing files. The build uses only Python 3's
standard library and leaves unchanged output files untouched.

The JSON uses stable, language-neutral `id`, `slug`, and `collection_ids` fields.
Visible fields live under `text.tr` (and image descriptions under `alt.tr`) so a
future language can add its own text without changing product identity. Images
use repository-relative paths under `assets/images/`. A product may have multiple
images, an optional integer `price_minor` with `currency: "TRY"`, optional `size`
in `text.tr`, and optional named `variants`. `status` controls publication;
`is_demo` explicitly marks sample records. The generator currently publishes
only demonstration products. Prices are formatted from integer kuruş, never
floating-point amounts.

Generated routes are `/products/`, `/collections/perfumes/`, and one
`/products/<slug>/` page for each published product. `/en/` remains reserved.
The generator does not remove previously generated routes after a slug is
deleted; remove obsolete output deliberately during a catalog change.

## Current scope

- `index.html` is the Turkish homepage. `/en/` is reserved for a future English site.
- `css/styles.css` and `js/main.js` are shared, language-neutral files.
- The hero and product photos in `assets/images/` are temporary crops from the approved
  `assets/reference/build-reference.png`. The source references and official logo are unchanged.
- Product names, sizes, types, and prices are demonstrative. Real catalog details, contact
  information, legal text, and commerce functions require confirmation.
- Search, account, wishlist, and cart symbols are noninteractive. The mobile menu is functional.
- The responsive styling follows the approved reference from phone through wide desktop.
  Independent production photography is deferred.
- The four homepage cards retain their approved hand-authored markup and repeat
  demonstration data from `catalog.json`. They link to generated product pages;
  unifying homepage rendering is deferred to a separate iteration.
