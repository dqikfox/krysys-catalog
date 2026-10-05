# KRYSYS Master Catalog

The complete inventory: **83 periodic-table elements + 273 crystals + 17 geodes = 373 SKUs**.

## Wholesale pricing + 10%

Every item is sourced at wholesale and sold at a flat 10% markup. Free shipping over $200.

## Live catalog

**https://dqikfox.github.io/krysys-catalog/**

## Inventory coverage

- **83 of 118 periodic-table elements** — radioactive and synthetic elements intentionally excluded (Tc, Pm, Po→Og)
- **273 crystals** — quartz family, beryl, corundum, garnet, tourmaline, opal, feldspar, chalcedony, agate, jasper, plus rare collector stones (painite, jeremejevite, benitoite, red beryl, demantoid, tsavorite)
- **17 geodes** — amethyst cathedrals, agate, septarian, pyrite, celestite

## Pricing data

The full catalog with wholesale and customer prices is in [`catalog-data.json`](./catalog-data.json).

## API endpoints (KRYSYS shop server)

When the local Express server (`server.js`) is running:

- `GET /api/catalog` — all 373 items
- `GET /api/catalog/sku/:sku` — single SKU lookup
- `GET /api/catalog/category/:cat` — filter by category (`element`, `crystal`, `geode`)
- `GET /api/catalog/element/:symbol` — filter by element symbol (H, He, Li, …)
- `GET /api/catalog/search?q=...&category=...` — search by name/description/origin

## Build script

The catalog is regenerated from authoritative mineralogy/elements knowledge by [`build_master_catalog.py`](./build_master_catalog.py) — re-run that script to update.

## Legal notes

- **Uranium (92)** sold as specimen-grade depleted uranium or autunite/carnotite mineral. Photo ID required in some regions.
- **Thorium (90)** sold as sealed chunk 99.9% — legal with note.
- All radioactive and synthetic elements (43, 61, 84–118) are explicitly excluded from the catalog.