# VOILA FRAGRANCES

Static Turkish and English demonstration storefront for VOILA FRAGRANCES.

## Local preview

From the repository root, run `python3 -m http.server 8000` and open
`http://localhost:8000/` (Turkish) or `http://localhost:8000/en/` (English).

## Catalog build

Run `python3 scripts/build_catalog.py` from the repository root to validate
`data/catalog.json` and `data/ui.json`, then generate both language versions. Run
`python3 scripts/build_catalog.py --check` to validate the data and verify the
committed HTML and output manifest are current without writing files. The build
uses only Python 3's standard library and leaves unchanged files untouched.

`src/templates/home.html` is the homepage source. The catalog, collection, and
product templates also live in `src/templates/`. The generated `index.html`,
`products/**/index.html`, `collections/*/index.html`, `cart/index.html`,
`about/index.html`, and `contact/index.html`, with corresponding routes under
`en/`, are build outputs: edit templates or source JSON, then rebuild. Do not edit
generated HTML directly.

The JSON uses stable, language-neutral `id`, `slug`, and `collection_ids` fields.
Visible fields live under `text.tr` and `text.en` (and image descriptions under
`alt.tr` and `alt.en`). Shared interface copy, labels, titles, and descriptions
live in `data/ui.json`. Both locales must provide every UI key and every required
catalog field; the build rejects incomplete translations. Proper names can have
the same value in both locales. Images use repository-relative paths under
`assets/images/`. A product may have multiple
images, an optional integer `price_minor` with `currency: "TRY"`, optional `size`
in each locale's `text`, and optional named `variants`. `status` controls publication;
`is_demo` explicitly marks sample records. The generator currently publishes
only demonstration products. Prices are formatted from integer kuruş, never
floating-point amounts.

To add a product, create a unique stable ID and language-neutral slug in
`products`, provide a valid collection ID and local image, add Turkish and English
text and image descriptions, and mark its status `published` or `draft`. Add its ID
to the ordered
`featured_product_ids` list only if it should appear on the homepage. Removing
an ID from that list removes just the featured card. To remove a product route,
delete the product record or mark it `draft`, then rebuild. Change a slug in the
record and rebuild to replace the old route. The homepage cards use that same
record for names, images, size, price, and links.

Generated routes are `/`, `/products/`, `/collections/perfumes/`, `/cart/`,
`/about/`, `/contact/`, and one `/products/<slug>/` page for each published product.
Each has an equivalent under `/en/` using the same neutral slug. The header's
TR / EN links point to the equivalent route, and each page includes reciprocal
`hreflang` links. By default these use root-relative URLs; deploy at the domain
root. If a confirmed public origin is available, pass `--site-origin https://example.com`
to both build and check to emit absolute `hreflang` URLs. No canonical URL is emitted.

`data/public-catalog.json` and `en/data/public-catalog.json` are generated. Each
contains only published product IDs, localized names and URLs, primary image paths,
and optional integer prices and currencies. The cart loads the current locale's
artifact. Do not edit either file directly.

`.generated-pages.json` records generator-owned paths and content hashes. A
successful build removes obsolete owned HTML pages and empty slug directories.
It preserves unrelated files and refuses to overwrite or delete an owned page
that was edited outside the build. This includes both locales. `--check` reports
missing, outdated, or obsolete outputs without changing them. Commit the manifest
with generated HTML.

## Content required before launch

The About page contains explicitly provisional brand copy. Replace it with
approved information about the business and products before launch. The Contact
page lists the confirmed Instagram account `@voila.fragrances`; add only verified
email, telephone, address, or service details when supplied. Prepare and review
accurate privacy, terms, returns, and other applicable legal information as a
separate pre-launch task. No legal-policy pages or unverified promises are
published in this iteration.

## Current scope

- `index.html` is the generated Turkish homepage; `en/index.html` is the English page.
- `css/styles.css`, `js/main.js`, and `js/cart.js` are shared files.
- The hero and product photos in `assets/images/` are temporary crops from the approved
  `assets/reference/build-reference.png`. The source references and official logo are unchanged.
- Product names, sizes, types, and prices are demonstrative. Real catalog details, contact
  information, legal text, and purchasing functions require confirmation.
- Search and account symbols remain noninteractive. The mobile menu is functional.
- The demonstration cart uses `localStorage` key `voila-fragrances.cart.v1` with
  `{ "version": 1, "items": [{ "id": "...", "quantity": 1 }] }`. It stores no
  authoritative names or prices. The cart re-reads current published product data
  from the current locale's public catalog JSON, removes stale IDs, and calculates
  totals in integer minor currency units. Without JavaScript or browser storage,
  catalog and product
  content remains available, but the cart cannot operate. Checkout, orders, shipping,
  tax, and payment are unavailable; all products and prices are demonstrations.
  The storage key and ID-based cart are shared across Turkish and English pages.
- The responsive styling follows the approved reference from phone through wide desktop.
  Independent production photography is deferred.
- The four homepage cards keep the approved structure and draw their content
  from `catalog.json` at build time. No JavaScript is needed to display them.
