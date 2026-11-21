# VOILA FRAGRANCES

Static Turkish homepage and demonstration catalog for the VOILA FRAGRANCES storefront.

## Local preview

From the repository root, run `python3 -m http.server 8000` and open
`http://localhost:8000/`.

## Catalog build

Run `python3 scripts/build_catalog.py` from the repository root to validate
`data/catalog.json` and generate the Turkish homepage plus catalog pages. Run
`python3 scripts/build_catalog.py --check` to validate the data and verify the
committed HTML and output manifest are current without writing files. The build
uses only Python 3's standard library and leaves unchanged files untouched.

`src/templates/home.html` is the homepage source. The catalog, collection, and
product templates also live in `src/templates/`. The generated `index.html`,
`products/**/index.html`, and `collections/*/index.html` are build outputs: edit
their templates or `data/catalog.json`, then rebuild. Do not edit generated HTML
directly.

The JSON uses stable, language-neutral `id`, `slug`, and `collection_ids` fields.
Visible fields live under `text.tr` (and image descriptions under `alt.tr`) so a
future language can add its own text without changing product identity. Images
use repository-relative paths under `assets/images/`. A product may have multiple
images, an optional integer `price_minor` with `currency: "TRY"`, optional `size`
in `text.tr`, and optional named `variants`. `status` controls publication;
`is_demo` explicitly marks sample records. The generator currently publishes
only demonstration products. Prices are formatted from integer kuruş, never
floating-point amounts.

To add a product, create a unique stable ID and language-neutral slug in
`products`, provide a valid collection ID and local image, set its Turkish text,
and mark its status `published` or `draft`. Add its ID to the ordered
`featured_product_ids` list only if it should appear on the homepage. Removing
an ID from that list removes just the featured card. To remove a product route,
delete the product record or mark it `draft`, then rebuild. Change a slug in the
record and rebuild to replace the old route. The homepage cards use that same
record for names, images, size, price, and links.

Generated routes are `/`, `/products/`, `/collections/perfumes/`, and one
`/products/<slug>/` page for each published product. `/en/` remains reserved.
`.generated-pages.json` records generator-owned paths and content hashes. A
successful build removes obsolete owned HTML pages and empty slug directories.
It preserves unrelated files and refuses to overwrite or delete an owned page
that was edited outside the build. `--check` reports missing, outdated, or
obsolete outputs without changing them. Commit the manifest with generated HTML.

## Current scope

- `index.html` is the generated Turkish homepage. `/en/` is reserved for a future English site.
- `css/styles.css` and `js/main.js` are shared, language-neutral files.
- The hero and product photos in `assets/images/` are temporary crops from the approved
  `assets/reference/build-reference.png`. The source references and official logo are unchanged.
- Product names, sizes, types, and prices are demonstrative. Real catalog details, contact
  information, legal text, and commerce functions require confirmation.
- Search, account, wishlist, and cart symbols are noninteractive. The mobile menu is functional.
- The responsive styling follows the approved reference from phone through wide desktop.
  Independent production photography is deferred.
- The four homepage cards keep the approved structure and draw their content
  from `catalog.json` at build time. No JavaScript is needed to display them.
