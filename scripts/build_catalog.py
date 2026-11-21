#!/usr/bin/env python3
"""Validate the Turkish demo catalog and build static HTML pages."""

import argparse
import html
import json
import re
import sys
from pathlib import Path, PurePosixPath
from string import Template


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "src" / "templates"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
IDENTIFIER = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")


class CatalogError(ValueError):
    """Invalid catalog source or generated output."""


def require_text(value, location):
    if not isinstance(value, str) or not value.strip():
        raise CatalogError(f"{location}: expected nonempty text")
    return value


def require_object(value, location):
    if not isinstance(value, dict):
        raise CatalogError(f"{location}: expected object")
    return value


def require_list(value, location, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise CatalogError(f"{location}: expected {'nonempty ' if nonempty else ''}array")
    return value


def localized(value, location, fields):
    tr = require_object(require_object(value, location).get("tr"), f"{location}.tr")
    for field in fields:
        require_text(tr.get(field), f"{location}.tr.{field}")
    for optional in ("size", "description"):
        if optional in tr:
            require_text(tr[optional], f"{location}.tr.{optional}")
    return tr


def safe_image(path, location):
    require_text(path, location)
    parts = PurePosixPath(path)
    if (
        path.startswith("/") or "\\" in path or "?" in path or "#" in path
        or any(part in ("", ".", "..") for part in path.split("/"))
        or len(parts.parts) < 3 or parts.parts[:2] != ("assets", "images")
        or parts.suffix.lower() not in {".webp", ".png", ".jpg", ".jpeg"}
    ):
        raise CatalogError(f"{location}: unsafe or unsupported image path: {path}")
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to((ROOT / "assets" / "images").resolve()):
        raise CatalogError(f"{location}: image escapes assets/images: {path}")
    if not resolved.is_file():
        raise CatalogError(f"{location}: image does not exist: {path}")


def validate_catalog(data):
    require_object(data, "catalog")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise CatalogError("catalog.schema_version: expected 1")
    collections = require_list(data.get("collections"), "collections", nonempty=True)
    products = require_list(data.get("products"), "products")
    ids, slugs, collection_ids = set(), set(), set()

    for index, collection in enumerate(collections):
        where = f"collections[{index}]"
        require_object(collection, where)
        for key, pattern, seen in (("id", IDENTIFIER, ids), ("slug", SLUG, slugs)):
            value = require_text(collection.get(key), f"{where}.{key}")
            if not pattern.fullmatch(value) or value in seen:
                raise CatalogError(f"{where}.{key}: duplicate or invalid {key}: {value}")
            seen.add(value)
        collection_ids.add(collection["id"])
        localized(collection.get("text"), f"{where}.text", ("name",))

    referenced = set()
    for index, product in enumerate(products):
        where = f"products[{index}]"
        require_object(product, where)
        for key, pattern, seen in (("id", IDENTIFIER, ids), ("slug", SLUG, slugs)):
            value = require_text(product.get(key), f"{where}.{key}")
            if not pattern.fullmatch(value) or value in seen:
                raise CatalogError(f"{where}.{key}: duplicate or invalid {key}: {value}")
            seen.add(value)
        membership = require_list(product.get("collection_ids"),
                                  f"{where}.collection_ids", nonempty=True)
        for collection_id in membership:
            require_text(collection_id, f"{where}.collection_ids")
        if len(membership) != len(set(membership)):
            raise CatalogError(f"{where}.collection_ids: duplicate collection")
        for collection_id in membership:
            if collection_id not in collection_ids:
                raise CatalogError(f"{where}.collection_ids: unknown collection {collection_id}")
            referenced.add(collection_id)
        images = require_list(product.get("images"), f"{where}.images", nonempty=True)
        for image_index, image in enumerate(images):
            image_where = f"{where}.images[{image_index}]"
            require_object(image, image_where)
            safe_image(image.get("path"), f"{image_where}.path")
            require_text(require_object(image.get("alt"), f"{image_where}.alt").get("tr"),
                         f"{image_where}.alt.tr")
        localized(product.get("text"), f"{where}.text",
                  ("name", "short_description", "description"))
        if product.get("status") not in ("published", "draft"):
            raise CatalogError(f"{where}.status: expected published or draft")
        if type(product.get("is_demo")) is not bool:
            raise CatalogError(f"{where}.is_demo: expected boolean")
        if product.get("status") == "published" and not product["is_demo"]:
            raise CatalogError(f"{where}: only demonstration products may be published")
        if "price_minor" in product:
            if type(product["price_minor"]) is not int or product["price_minor"] < 0:
                raise CatalogError(f"{where}.price_minor: expected nonnegative integer")
            if product.get("currency") != "TRY":
                raise CatalogError(f"{where}.currency: only TRY formatting is supported")
        elif "currency" in product:
            raise CatalogError(f"{where}.currency: requires price_minor")
        variants = require_list(product.get("variants", []), f"{where}.variants")
        variant_ids = set()
        for variant_index, variant in enumerate(variants):
            variant_where = f"{where}.variants[{variant_index}]"
            require_object(variant, variant_where)
            variant_id = require_text(variant.get("id"), f"{variant_where}.id")
            if not IDENTIFIER.fullmatch(variant_id) or variant_id in variant_ids:
                raise CatalogError(f"{variant_where}.id: duplicate or invalid ID")
            variant_ids.add(variant_id)
            localized(variant.get("text"), f"{variant_where}.text", ("name",))

    for collection in collections:
        if collection["id"] not in referenced:
            raise CatalogError(f"collection {collection['id']}: no products reference it")
    return data


def escape(value):
    return html.escape(value, quote=True)


def template(filename, **values):
    source = (TEMPLATES / filename).read_text(encoding="utf-8")
    return Template(source).substitute(values)


def format_price(product):
    if "price_minor" not in product:
        return ""
    whole, minor = divmod(product["price_minor"], 100)
    number = f"{whole:,}".replace(",", ".")
    if minor:
        number += f",{minor:02d}"
    return f"{number} ₺"


def product_card(product, root):
    tr = product["text"]["tr"]
    image = product["images"][0]
    price = format_price(product)
    return template(
        "product-card.html",
        product_url=f"{root}products/{product['slug']}/",
        image_url=root + image["path"],
        image_alt=escape(image["alt"]["tr"]),
        name=escape(tr["name"]),
        size=escape(tr.get("size", tr["short_description"])),
        price=(f'<p class="product-price" aria-label="Temsilî fiyat: {escape(price)}">'
               f'{escape(price)}</p>') if price else "",
    )


def page(body, root, title, description, collections, current_collection=None):
    navigation_links = []
    for item in collections:
        active = ' aria-current="page"' if item["id"] == current_collection else ""
        navigation_links.append(
            f'<li><a href="{root}collections/{item["slug"]}/"{active}>'
            f'{escape(item["text"]["tr"]["name"])}</a></li>'
        )
    return template(
        "layout.html", root=root, main=body,
        page_title=escape(title), meta_description=escape(description),
        collection_navigation="\n".join(navigation_links),
    )


def render_pages(data):
    pages = {}
    published = [item for item in data["products"] if item["status"] == "published"]
    collections = {item["id"]: item for item in data["collections"]}
    links = "\n".join(
        f'<li><a href="../collections/{item["slug"]}/">'
        f'{escape(item["text"]["tr"]["name"])}</a></li>'
        for item in data["collections"]
    )
    body = template("catalog.html", collection_links=links,
                    product_cards="\n".join(product_card(item, "../") for item in published))
    pages[ROOT / "products" / "index.html"] = page(
        body, "../", "Ürünler", "Temsilî VOILA FRAGRANCES ürün kataloğu.",
        data["collections"])

    for collection in data["collections"]:
        tr = collection["text"]["tr"]
        matching = [item for item in published if collection["id"] in item["collection_ids"]]
        body = template(
            "collection.html", root="../../", name=escape(tr["name"]),
            description=f'<p>{escape(tr["description"])}</p>'
                        if tr.get("description") else "",
            product_cards="\n".join(product_card(item, "../../") for item in matching),
            empty_state="" if matching else "<p>Bu koleksiyonda yayımlanmış ürün bulunmuyor.</p>",
        )
        pages[ROOT / "collections" / collection["slug"] / "index.html"] = page(
            body, "../../", tr["name"], tr.get("description", ""),
            data["collections"], current_collection=collection["id"])

    for product in published:
        tr = product["text"]["tr"]
        primary_collection = collections[product["collection_ids"][0]]
        primary_name = primary_collection["text"]["tr"]["name"]
        images = product["images"]
        secondary = "\n".join(
            f'<img src="../../{image["path"]}" alt="{escape(image["alt"]["tr"])}" '
            'loading="lazy" width="285" height="200">' for image in images[1:]
        )
        price = format_price(product)
        variants = product.get("variants", [])
        variant_markup = (
            '<div class="catalog-variants"><h2>Seçenekler</h2><ul>'
            + "".join(f'<li>{escape(item["text"]["tr"]["name"])}</li>'
                      for item in variants)
            + "</ul></div>"
        ) if variants else ""
        body = template(
            "product.html", root="../../", name=escape(tr["name"]),
            collection_url=f"../../collections/{primary_collection['slug']}/",
            collection_name=escape(primary_name),
            main_image_url="../../" + images[0]["path"],
            main_image_alt=escape(images[0]["alt"]["tr"]),
            secondary_images=secondary, short_description=escape(tr["short_description"]),
            description=escape(tr["description"]),
            size=f'<p><strong>Boyut / tür:</strong> {escape(tr["size"])}</p>'
                 if tr.get("size") else "",
            variants=variant_markup,
            price=f'<p><strong>Temsilî fiyat:</strong> {escape(price)}</p>' if price else "",
        )
        pages[ROOT / "products" / product["slug"] / "index.html"] = page(
            body, "../../", tr["name"], tr["short_description"], data["collections"])
    return pages


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate and check generated files")
    args = parser.parse_args()
    try:
        source = (ROOT / "data" / "catalog.json").read_text(encoding="utf-8")
        data = validate_catalog(json.loads(source, object_pairs_hook=no_duplicate_keys))
        pages = render_pages(data)
        changed = []
        for path, content in pages.items():
            content = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                changed.append(path.relative_to(ROOT).as_posix())
                if not args.check:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
        if args.check and changed:
            raise CatalogError("generated pages missing or outdated: " + ", ".join(changed))
        verb = "checked" if args.check else "generated"
        print(f"Catalog valid: {len(data['products'])} products, "
              f"{len(data['collections'])} collections; {verb} {len(pages)} pages "
              f"({len(changed)} changed).")
    except (CatalogError, OSError, json.JSONDecodeError, KeyError) as error:
        print(f"Catalog error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
