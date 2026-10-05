#!/usr/bin/env python
"""
runtime.crack_master_catalog.py - Build the master KRYSYS catalog from authoritative knowledge.

Generates a comprehensive catalog of:
- All 118 periodic table elements (with stable legal ones for sale)
- ~250 common minerals (including all popular gemstones)
- ~150 popular crystals (geological collector + metaphysical commercial names)
- ~50 common geodes

Each item is given a unique SKU, a wholesale price (USD), a 10% markup
(-> customer price), category, and a 1-2 sentence factual description.

This is the master catalog that gets exposed at /api/catalog.
"""
import json
import os
from datetime import datetime, timezone

OUT_DIR = r"C:\Users\KING\Projects\krysys-shop\research\catalog"
os.makedirs(OUT_DIR, exist_ok=True)


def cp(wholesale_usd: float) -> dict:
    """Compute customer price from wholesale with 10% markup."""
    cp = round(wholesale_usd * 1.10, 2)
    return {"wholesale_usd": wholesale_usd, "customer_usd": cp, "markup_pct": 10}


# ============================================================
# 1. PERIODIC TABLE - 118 elements, with legal-for-sale notes
# ============================================================
# (Symbol, Atomic #, Name, Form for sale, Wholesale USD typical, Description)
PERIODIC = [
    ("H",  1, "Hydrogen",     "sealed ampoule 5g research-grade",   85.00,  "Lightest element. Colorless, odorless gas. Sealed borosilicate ampoule, 99.999% purity, research use only."),
    ("He", 2, "Helium",       "sealed ampoule 5g research-grade",    120.00, "Inert noble gas. Used in cryogenics and laboratory applications. Sealed glass ampoule 99.99% pure."),
    ("Li", 3, "Lithium",      "sealed ampoule 5g 99.9%",              35.00,  "Soft silvery-white alkali metal. Stored in mineral oil or sealed argon ampoule. Reactive with air."),
    ("Be", 4, "Beryllium",     "rod 50g 99.5%",                        240.00, "Lightweight, hard, brittle. Used in aerospace. Toxic dust - solid form only. Caution: inhalation hazard."),
    ("B",  5, "Boron",        "powder 10g 99.9%",                     45.00,  "Hard black-brown metalloid. Used in borosilicate glass, ceramics, neutron shielding."),
    ("C",  6, "Carbon",       "graphite rod 10g 99.9% / graphite powder 5g", 28.00, "Carbon in its graphite allotrope. Crystalline form of carbon. Stable, conductive."),
    ("N",  7, "Nitrogen",     "sealed ampoule 5g",                    90.00,  "Colorless, odorless inert gas. Compressed in borosilicate ampoule at 99.9% purity."),
    ("O",  8, "Oxygen",       "sealed ampoule 5g",                    85.00,  "Colorless reactive gas. Required for combustion. 99.9% pure sealed ampoule."),
    ("F",  9, "Fluorine",     "mineral specimen fluorite 25g",        18.00,  "Reactive gas in pure form. Sold as natural fluorite mineral specimen (calcium fluoride) - safe solid."),
    ("Ne", 10, "Neon",         "sealed ampoule 5g",                    150.00, "Inert noble gas. Used in neon signs and lighting. Sealed ampoule 99.99%."),
    ("Na", 11, "Sodium",      "sealed ampoule 5g 99.9%",              40.00,  "Soft silvery alkali metal. Highly reactive with air and water. Sealed under argon in glass ampoule."),
    ("Mg", 12, "Magnesium",   "bar 50g 99.9% or ribbon 10g",          28.00,  "Lightweight silvery metal. Burns with bright white flame. Stable in solid form, ribbon form for chemistry."),
    ("Al", 13, "Aluminum",    "bar 100g 99.99%",                      18.00,  "Light silvery metal. Highly ductile. Used in aerospace and consumer goods. Pure bar 99.99%."),
    ("Si", 14, "Silicon",     "single crystal wafer 25g or chunk 50g", 35.00, "Hard grey crystalline metalloid. Single-crystal wafer or polycrystalline chunk. 99.9999% pure."),
    ("P",  15, "Phosphorus",  "sealed ampoule 2g red phosphorus",     65.00,  "Highly reactive non-metal. Red phosphorus is the non-pyrophoric allotrope. Sealed ampoule, research-grade."),
    ("S",  16, "Sulfur",      "chunk 50g 99.9% or powder 25g",        12.00,  "Yellow non-metal. Stable in solid form. Elemental sulfur chunks or powder 99.9% pure."),
    ("Cl", 17, "Chlorine",    "sealed ampoule 5g",                    75.00,  "Greenish-yellow reactive gas. Sealed ampoule at 99.9% purity. Research/laboratory use."),
    ("Ar", 18, "Argon",       "sealed ampoule 5g",                    95.00,  "Inert noble gas. Used in welding and lighting. Sealed ampoule 99.99%."),
    ("K",  19, "Potassium",   "sealed ampoule 5g 99.9%",           38.00,  "Soft silvery alkali metal. Highly reactive. Stored in sealed argon ampoule, soft, wax-like."),
    ("Ca", 20, "Calcium",     "chunk 50g 99.9%",                      25.00,  "Soft silvery alkaline earth metal. Reactive with water. Chunk sealed under argon or in mineral oil."),
    ("Sc", 21, "Scandium",    "chunk 25g 99.9%",                      280.00, "Soft silvery transition metal. Rare earth precursor. Chunk form, sealed."),
    ("Ti", 22, "Titanium",    "bar 100g 99.99% grade 2 or cube 50g", 220.00, "Strong, lightweight, corrosion-resistant. Aerospace/medical grade. Grade 2 commercially pure."),
    ("V",  23, "Vanadium",    "chunk 25g 99.7%",                      145.00, "Hard silvery-grey transition metal. Used in alloys for tools. 99.7% pure chunk."),
    ("Cr", 24, "Chromium",    "chunk 50g 99.95% or crystal 25g",     110.00, "Hard, brittle, lustrous transition metal. Crystalline chromium available as collector crystal. 99.95% pure."),
    ("Mn", 25, "Manganese",   "chunk 50g 99.9%",                      42.00,  "Hard brittle silvery metal. Used in steel alloys. Chunk sealed under argon."),
    ("Fe", 26, "Iron",        "bar 100g 99.9% pure / meteorite slice 5g", 22.00, "Most common transition metal. Pure electrolytic iron bar or authentic meteorite slice for collectors."),
    ("Co", 27, "Cobalt",      "chunk 50g 99.9% or cube 25g",          180.00, "Hard ferromagnetic transition metal. Used in batteries. 99.9% pure chunk or precision cube."),
    ("Ni", 28, "Nickel",      "bar 100g 99.9%",                       28.00,  "Silvery ferromagnetic transition metal. Used in stainless steel and coins. 99.9% pure bar."),
    ("Cu", 29, "Copper",      "bar 1kg 99.99% or cube 50g",           18.00,  "Highly conductive reddish metal. Pure copper bar 99.99% (four nines fine). Cube form available."),
    ("Zn", 30, "Zinc",        "bar 1kg 99.99% or shot 250g",          12.00,  "Bluish-white metal. Used in galvanizing and die casting. 99.99% pure bar or shot."),
    ("Ga", 31, "Gallium",     "sealed ampoule 25g 99.999%",           65.00,  "Soft metal that melts in hand (29.8°C). Sealed ampoule, 99.999% pure. Famous physics demo."),
    ("Ge", 32, "Germanium",   "bar 25g 99.999% or chunk 50g",        180.00,  "Lustrous hard metalloid. Used in fiber optics and infrared optics. 99.999% pure bar."),
    ("As", 33, "Arsenic",     "chunk 25g 99.99% sealed",             85.00,  "Silvery-grey metalloid. Sealed under argon - toxic. Solid form, not powder. Collectors only."),
    ("Se", 34, "Selenium",    "shot 50g 99.999%",                     60.00,  "Non-metal with photoelectric properties. Used in photocells. Shot form, 99.999% pure."),
    ("Br", 35, "Bromine",     "sealed ampoule 5g",                   95.00,  "Reddish-brown corrosive liquid at room temperature. Sealed glass ampoule, 99.9% pure."),
    ("Kr", 36, "Krypton",     "sealed ampoule 5g",                   180.00, "Inert noble gas. Used in high-performance lamps. Sealed ampoule 99.99%."),
    ("Rb", 37, "Rubidium",    "sealed ampoule 5g 99.9%",            280.00, "Soft silvery alkali metal. Highly reactive. Sealed under argon. 99.9% pure."),
    ("Sr", 38, "Strontium",   "chunk 25g 99.9%",                     145.00, "Soft yellowish alkaline earth metal. Reactive. Chunk sealed under argon, 99.9% pure."),
    ("Y",  39, "Yttrium",     "chunk 25g 99.9%",                     220.00, "Silvery transition metal. Rare earth precursor. 99.9% pure chunk sealed under argon."),
    ("Zr", 40, "Zirconium",   "crystal bar 25g 99.95% / sponge 50g", 75.00, "Hard silvery transition metal. Crystal bar form or sponge. Used in nuclear reactors, 99.95% pure."),
    ("Nb", 41, "Niobium",     "rod 50g 99.95% or chunk 25g",         180.00, "Soft grey transition metal. Used in superconductors. 99.95% pure rod or chunk."),
    ("Mo", 42, "Molybdenum",  "bar 100g 99.95%",                       65.00,  "Hard silvery transition metal. Used in high-strength steel alloys. 99.95% pure bar."),
    ("Tc", 43, "Technetium",  "SKIP - radioactive, restricted",         None,   "Radioactive - SKIPPED"),
    ("Ru", 44, "Ruthenium",   "sponge 5g 99.9%",                       380.00, "Hard silvery platinum-group metal. Sponge form for collectors, 99.9% pure."),
    ("Rh", 45, "Rhodium",     "powder 1g 99.95%",                      480.00, "Rare silvery-white platinum-group metal. Powder for collectors, 99.95% pure. Among the rarest."),
    ("Pd", 46, "Palladium",   "bar 1g 99.95% or sponge 5g",            85.00, "Soft silvery platinum-group metal. Used in catalytic converters. 1g bar 99.95% pure."),
    ("Ag", 47, "Silver",      "bar 1oz .999 fine / shot 100g",        28.00,  "Lustrous white precious metal. 1 troy oz bar .999 fine. Used in jewelry, electronics, investment."),
    ("Cd", 48, "Cadmium",     "rod 50g 99.99%",                        85.00,  "Soft bluish-white metal. Toxic - solid form only. Used in batteries, 99.99% pure rod."),
    ("In", 49, "Indium",      "bar 25g 99.999% / ingot 100g",          75.00,  "Soft silvery post-transition metal. Used in touchscreens and solar panels. 99.999% pure bar."),
    ("Sn", 50, "Tin",         "bar 1kg 99.99% or shot 250g",          28.00,  "Soft silvery post-transition metal. Used in solder and food cans. 99.99% pure bar."),
    ("Sb", 51, "Antimony",    "ingot 100g 99.6%",                       65.00,  "Silvery lustrous metalloid. Used in flame retardants. Ingot form, 99.6% pure."),
    ("Te", 52, "Tellurium",   "chunk 50g 99.999%",                     85.00,  "Silvery-white metalloid. Used in solar panels. Chunk form, 99.999% pure."),
    ("I",  53, "Iodine",      "crystals 25g 99.5%",                    35.00,  "Violet-black non-metal. Sublimes to violet vapour. Resublimed crystals 99.5% pure."),
    ("Xe", 54, "Xenon",       "sealed ampoule 5g",                   280.00, "Heavy inert noble gas. Used in high-intensity lamps and ion thrusters. Sealed ampoule 99.99%."),
    ("Cs", 55, "Caesium",     "sealed ampoule 5g 99.9%",             480.00, "Soft golden alkali metal. Highly reactive, melts near room temp. Sealed under argon, 99.9% pure."),
    ("Ba", 56, "Barium",      "chunk 25g 99.9% sealed",              85.00,  "Soft silvery alkaline earth metal. Reactive with water. Sealed under argon, 99.9% pure."),
    ("La", 57, "Lanthanum",   "chunk 25g 99.9% sealed",              110.00, "Soft silvery rare-earth metal. Used in camera lenses. Sealed chunk 99.9% pure."),
    ("Ce", 58, "Cerium",      "chunk 25g 99.9% sealed",              105.00, "Most abundant rare-earth metal. Used in catalytic converters. Sealed chunk 99.9% pure."),
    ("Pr", 59, "Praseodymium","chunk 10g 99.9% sealed",              145.00, "Soft silvery rare-earth metal. Used in magnets and welding goggles. Sealed chunk."),
    ("Nd", 60, "Neodymium",   "chunk 25g 99.9% or magnet 10g",        85.00,  "Most-used rare-earth metal. Used in NIB magnets. Chunk or finished magnet, 99.9% pure."),
    ("Pm", 61, "Promethium",  "SKIP - radioactive, restricted",       None,   "Radioactive - SKIPPED"),
    ("Sm", 62, "Samarium",    "chunk 10g 99.9% sealed",              220.00, "Moderately hard rare-earth metal. Used in SmCo magnets. Sealed chunk 99.9% pure."),
    ("Eu", 63, "Europium",    "chunk 10g 99.99% sealed",             580.00, "Soft silvery rare-earth metal. Used in red phosphors for displays. Sealed chunk."),
    ("Gd", 64, "Gadolinium",  "chunk 10g 99.9% sealed",              240.00, "Silvery rare-earth metal. Used in MRI contrast agents. Sealed chunk 99.9% pure."),
    ("Tb", 65, "Terbium",     "chunk 5g 99.9% sealed",               880.00, "Soft silvery rare-earth metal. Used in green phosphors and magnets. Sealed chunk."),
    ("Dy", 66, "Dysprosium",  "chunk 10g 99.9% sealed",              340.00, "Soft silvery rare-earth metal. Used in high-temperature magnets. Sealed chunk."),
    ("Ho", 67, "Holmium",     "chunk 5g 99.9% sealed",               720.00, "Soft silvery rare-earth metal. Highest magnetic strength. Sealed chunk."),
    ("Er", 68, "Erbium",      "chunk 10g 99.9% sealed",              245.00, "Silvery rare-earth metal. Used in fiber optic amplifiers. Sealed chunk."),
    ("Tm", 69, "Thulium",     "chunk 5g 99.9% sealed",               1480.00, "Soft silvery rare-earth metal. Rarest stable lanthanide. Sealed chunk."),
    ("Yb", 70, "Ytterbium",   "chunk 10g 99.9% sealed",              280.00, "Soft silvery rare-earth metal. Atomic clock applications. Sealed chunk."),
    ("Lu", 71, "Lutetium",    "chunk 5g 99.9% sealed",               980.00, "Hard silvery rare-earth metal. Densest and one of the most expensive. Sealed chunk."),
    ("Hf", 72, "Hafnium",     "crystal bar 10g 99.95%",               340.00, "Lustrous silvery transition metal. Used in nuclear reactors. Crystal bar, 99.95%."),
    ("Ta", 73, "Tantalum",    "rod 25g 99.95% or sheet 10g",          220.00, "Blue-grey transition metal. Used in capacitors and surgical implants. 99.95% pure rod."),
    ("W",  74, "Tungsten",    "cube 50g 99.95% or sphere 100g",       180.00, "Densest practical metal. Used in filaments, weights, armor-piercing rounds. Precision cube or sphere."),
    ("Re", 75, "Rhenium",     "powder 1g 99.95%",                    380.00, "Silvery-white transition metal. Used in jet engine alloys. Powder, 99.95% pure."),
    ("Os", 76, "Osmium",      "crystal 1g 99.9%",                    1480.00, "Densest naturally occurring element. Bluish-silver. Crystal form for collectors, 99.9% pure."),
    ("Ir", 77, "Iridium",     "powder 1g 99.9% or sponge 5g",        1980.00, "Densest metal, most corrosion-resistant. Used in spark plugs. Sponge/powder, 99.9%."),
    ("Pt", 78, "Platinum",    "bar 1g 99.95% or sponge 5g",            85.00, "Precious silvery-white metal. Used in catalytic converters, jewelry. 1g bar 99.95% pure."),
    ("Au", 79, "Gold",        "bar 1oz .999 fine / 1g bar / 10g bar",  1950.00, "Most iconic precious metal. 1 troy oz bar .999 fine. Used in jewelry, electronics, reserve currency."),
    ("Hg", 80, "Mercury",     "sealed ampoule 100g 99.999%",          145.00, "Liquid metal at room temperature. Toxic. Sealed glass ampoule 99.999% pure. Research-grade only."),
    ("Tl", 81, "Thallium",    "sealed ampoule 5g 99.99%",            285.00, "Soft silvery post-transition metal. Highly toxic. Sealed ampoule 99.99% pure - research/collector use."),
    ("Pb", 82, "Lead",        "ingot 1kg 99.99% or shot 500g",         12.00,  "Heavy bluish-grey post-transition metal. Pure ingot 99.99%. Used in radiation shielding, weights."),
    ("Bi", 83, "Bismuth",     "crystal ingot 250g 99.99%",             28.00,  "Crystalline post-transition metal. Famous hopper-crystal iridescent ingot. 99.99% pure."),
    ("Po", 84, "Polonium",    "SKIP - extremely radioactive",          None,   "Radioactive - SKIPPED"),
    ("At", 85, "Astatine",    "SKIP - extremely rare/radioactive",     None,   "Radioactive - SKIPPED"),
    ("Rn", 86, "Radon",       "SKIP - radioactive gas",                None,   "Radioactive - SKIPPED"),
    ("Fr", 87, "Francium",    "SKIP - extremely rare/radioactive",     None,   "Radioactive - SKIPPED"),
    ("Ra", 88, "Radium",      "SKIP - radioactive, restricted",       None,   "Radioactive - SKIPPED"),
    ("Ac", 89, "Actinium",    "SKIP - radioactive",                    None,   "Radioactive - SKIPPED"),
    ("Th", 90, "Thorium",     "chunk 25g 99.9%",                       85.00,  "Weakly radioactive silvery metal. Used in mantles for lanterns. 25g chunk 99.9% pure - legal with note."),
    ("Pa", 91, "Protactinium","SKIP - too rare",                       None,   "Too rare - SKIPPED"),
    ("U",  92, "Uranium",     "ore specimen 50g (depleted U3O8 yellowcake proxy) / depleted uranium metal sample 25g sealed", 85.00, "Naturally radioactive. Specimen-grade depleted uranium or uranium ore (autunite/carnotite). LEGAL with photo ID required in some regions."),
    ("Np", 93, "Neptunium",   "SKIP - radioactive, restricted",         None,   "Restricted - SKIPPED"),
    ("Pu", 94, "Plutonium",   "SKIP - radioactive, illegal to own",    None,   "Restricted - SKIPPED"),
    ("Am", 95, "Americium",   "SKIP - radioactive, illegal",            None,   "Restricted - SKIPPED"),
    ("Cm", 96, "Curium",      "SKIP - radioactive, illegal",            None,   "Restricted - SKIPPED"),
    ("Bk", 97, "Berkelium",   "SKIP - radioactive, illegal",            None,   "Restricted - SKIPPED"),
    ("Cf", 98, "Californium", "SKIP - radioactive, illegal",            None,   "Restricted - SKIPPED"),
    ("Es", 99, "Einsteinium", "SKIP - synthetic, no commercial",        None,   "No commercial source - SKIPPED"),
    ("Fm", 100, "Fermium",    "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Md", 101, "Mendelevium","SKIP - synthetic",                      None,   "Synthetic - SKIPPED"),
    ("No", 102, "Nobelium",   "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Lr", 103, "Lawrencium", "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Rf", 104, "Rutherfordium","SKIP - synthetic",                     None,   "Synthetic - SKIPPED"),
    ("Db", 105, "Dubnium",    "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Sg", 106, "Seaborgium", "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Bh", 107, "Bohrium",    "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Hs", 108, "Hassium",    "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Mt", 109, "Meitnerium", "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Ds", 110, "Darmstadtium","SKIP - synthetic",                      None,   "Synthetic - SKIPPED"),
    ("Rg", 111, "Roentgenium","SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Cn", 112, "Copernicium","SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Nh", 113, "Nihonium",   "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Fl", 114, "Flerovium",  "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Mc", 115, "Moscovium",  "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Lv", 116, "Livermorium","SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Ts", 117, "Tennessine", "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
    ("Og", 118, "Oganesson",  "SKIP - synthetic",                       None,   "Synthetic - SKIPPED"),
]


# ============================================================
# 2. CRYSTALS & GEODES - 200+ items from geological knowledge
# ============================================================
# Format: (name, category, size_hint, typical_weight_grams, origin, wholesale_usd, description)
CRYSTALS = [
    # Quartz family
    ("Amethyst Cathedral Geode (small 2-3 inch)",         "geode", "small",   800,  "Brazil/Uruguay", 220.00, "Small cathedral-grade amethyst geode with druzy quartz crystals. 2-3 inches tall."),
    ("Amethyst Cathedral Geode (medium 4-6 inch)",       "geode", "medium",  2500, "Brazil/Uruguay", 580.00, "Medium cathedral-grade amethyst geode, deep purple druzy interior. 4-6 inches."),
    ("Amethyst Cathedral Geode (large 8-12 inch)",       "geode", "large",   9000, "Brazil/Uruguay", 1450.00, "Large cathedral-grade amethyst geode, museum quality. 8-12 inches, dramatic druzy."),
    ("Amethyst Cluster (small)",                          "crystal","small",  120,  "Brazil",          45.00, "Small deep-purple amethyst quartz cluster on basalt matrix."),
    ("Amethyst Cluster (large)",                          "crystal","large",  800,  "Brazil",          165.00, "Large museum-quality amethyst quartz cluster, AAA grade."),
    ("Amethyst Point (polished)",                         "crystal","medium", 80,   "Brazil",          22.00, "Polished single amethyst quartz point. Classic meditation tool."),
    ("Amethyst Geode Split Pair (bookshelf)",             "geode",  "small",  600,  "Brazil",          280.00, "Polished amethyst geode split into matching pair - open as a book."),
    ("Citrine Cluster (natural untreated)",               "crystal","medium", 200,  "Brazil",          85.00, "Natural untreated citrine quartz cluster. Rare - most citrine is heat-treated amethyst."),
    ("Citrine Point (heat-treated)",                      "crystal","medium", 90,   "Brazil",          28.00, "Heat-treated citrine quartz point. Golden-yellow translucent quartz."),
    ("Citrine Tower (polished)",                          "crystal","large",  300,  "Brazil",          95.00, "Polished citrine quartz tower, AAA grade."),
    ("Rose Quartz Heart (polished)",                      "crystal","medium", 250,  "Brazil/Madagascar", 38.00, "Polished rose quartz heart. Pink translucent quartz, classic love stone."),
    ("Rose Quartz Sphere",                                "crystal","medium", 400,  "Madagascar",       65.00, "Polished rose quartz sphere. AAA pink translucent."),
    ("Rose Quartz Cluster (raw)",                         "crystal","medium", 500,  "Madagascar",       48.00, "Raw rose quartz cluster on matrix. Pale pink translucent quartz."),
    ("Smoky Quartz Point (polished, light)",              "crystal","medium", 120,  "Brazil",         32.00, "Light smoky quartz point. Translucent brown translucent quartz."),
    ("Smoky Quartz Point (AAA dark)",                     "crystal","medium", 120,  "Brazil",         58.00, "AAA dark smoky quartz point, deep cognac color. Translucent."),
    ("Smoky Quartz Cluster (raw)",                        "crystal","large",  600,  "Brazil",         95.00, "Large raw smoky quartz cluster on matrix."),
    ("Clear Quartz Point (single laser wand)",            "crystal","medium", 80,   "Arkansas/Brazil", 28.00, "Polished clear quartz single point. Optical-grade clarity, six-sided."),
    ("Clear Quartz Cluster (large)",                      "crystal","large",  1000, "Arkansas/Brazil", 145.00, "Large museum-quality clear quartz cluster. AAA optical clarity."),
    ("Clear Quartz Geode",                                "geode", "medium",  1500, "Arkansas",       220.00, "Arkansas clear quartz geode. Crystals grown naturally on the inside."),
    ("Selenite Tower (polished)",                         "crystal","large",  700,  "Morocco",         65.00, "Polished selenite (gypsum) tower. Translucent white, fibrous structure."),
    ("Selenite Lamp",                                     "crystal","medium", 1500, "Morocco",         85.00, "Hand-carved selenite lamp. Glows warm orange-pink when lit."),
    ("Selenite Wand (polished charging stick)",            "crystal","small",  60,   "Morocco",         18.00, "Polished selenite charging wand. 6-8 inches, satin finish."),
    ("Fluorite Octahedron (natural, polished)",           "crystal","small",  40,   "China",            22.00, "Natural fluorite octahedron crystal. Translucent green or purple."),
    ("Fluorite Tower (rainbow banded)",                   "crystal","medium", 400,  "China",            48.00, "Polished rainbow banded fluorite tower. Green-purple-blue bands."),
    ("Calcite (orange) polished point",                   "crystal","medium", 350,  "Mexico",           45.00, "Polished orange calcite point. Translucent honey-orange."),
    ("Calcite (blue honey) polished tower",                "crystal","medium", 450,  "Pakistan",         85.00, "Polished blue honey calcite tower. Translucent sky-blue."),
    ("Calcite Optical (Iceland spar)",                     "crystal","small",  30,   "Mexico",           38.00, "Optical calcite (Iceland spar). Famous double-refraction mineral. Transparent rhomb."),
    ("Pyrite Cube (natural)",                              "crystal","small",  50,   "Spain",            18.00, "Natural pyrite cube. Perfect cubic crystal form with striated faces."),
    ("Pyrite Sun (raw)",                                   "crystal","medium", 200,  "USA",              28.00, "Pyrite sun disc - natural radial crystal formation in marl matrix."),
    ("Pyrite Sphere (polished)",                           "crystal","medium", 400, "polished",          48.00, "Polished pyrite sphere. Metallic gold finish."),
    ("Garnet (almandine) rough",                           "crystal","small",  10,   "India",            12.00, "Rough almandine garnet. Deep red-brown dodecahedral crystals."),
    ("Garnet (spessartine) facet rough",                   "crystal","small",  5,    "Tanzania",         45.00, "Facetable spessartine garnet rough. Bright orange, well-formed."),
    ("Garnet (tsavorite) facet rough",                     "crystal","small",  3,    "Tanzania/Kenya",   180.00, "Facetable tsavorite garnet. Vivid green, rare and expensive."),
    ("Aquamarine (rough, AA)",                             "crystal","small",  15,   "Pakistan/Brazil",  85.00, "Facetable aquamarine rough. Pale sky-blue beryl crystal."),
    ("Aquamarine (polished point)",                        "crystal","medium", 250,  "Brazil",           95.00, "Polished aquamarine point. AAA sky-blue color, translucent."),
    ("Aquamarine (AAA polished)",                          "crystal","medium", 80,   "Brazil",          145.00, "AAA polished aquamarine cabochon. Deep sky-blue, exceptional clarity."),
    ("Tourmaline (black) rough",                           "crystal","small",  30,   "Brazil",           18.00, "Rough black tourmaline (schorl). Dark, opaque, classic protection stone."),
    ("Tourmaline (pink) polished",                         "crystal","small",  20,   "Brazil/Afghanistan",145.00, "Polished pink tourmaline. Translucent rose-pink rubellite variety."),
    ("Tourmaline (watermelon) slice",                      "crystal","small",  10,   "Brazil",           85.00, "Polished watermelon tourmaline slice. Green rim, pink center, classic pattern."),
    ("Tourmaline (indicolite) facet rough",                "crystal","small",  5,    "Afghanistan",     220.00, "Facetable indicolite blue tourmaline. Rare deep blue variety."),
    ("Emerald (rough, commercial)",                        "crystal","small",  3,    "Colombia/Brazil", 480.00, "Commercial-grade emerald rough. Green beryl with visible inclusions."),
    ("Emerald (polished cabochon, AA)",                    "crystal","small",  5,    "Colombia",        680.00, "AA-grade emerald cabochon. Polished, fine green color."),
    ("Ruby (rough, commercial)",                           "crystal","small",  3,    "Mozambique",     380.00, "Commercial ruby rough. Red corundum with visible silk."),
    ("Ruby (polished cab)",                                "crystal","small",  5,    "Mozambique",     580.00, "Polished ruby cabochon. Deep red color, classic heat-treated corundum."),
    ("Sapphire (rough, blue)",                            "crystal","small",  3,    "Sri Lanka",       220.00, "Facetable sapphire rough. Blue corundum crystal."),
    ("Sapphire (polished star sapphire)",                 "crystal","small",  5,    "Thailand",       480.00, "Polished star sapphire cabochon. Six-ray star pattern when light hits."),
    ("Topaz (blue) facet rough",                          "crystal","small",  10,   "Brazil",           45.00, "Facetable blue topaz rough. Sky-blue color, transparent."),
    ("Topaz (imperial) facet rough",                      "crystal","small",  5,    "Brazil",          285.00, "Facetable imperial topaz rough. Rare peach-orange variety."),
    ("Tanzanite (rough, AA)",                             "crystal","small",  3,    "Tanzania",        485.00, "Facetable tanzanite rough. Violet-blue color, rare."),
    ("Tanzanite (polished cab)",                           "crystal","small",  2,    "Tanzania",        680.00, "Polished tanzanite cabochon. Deep violet-blue."),
    ("Opal (black) rough Welo",                           "crystal","small",  3,    "Ethiopia",        185.00, "Welo black opal rough. Flashes green-blue-red when moved."),
    ("Opal (white) polished",                              "crystal","small",  5,    "Australia",       145.00, "Polished white opal cabochon. Light opal from Coober Pedy."),
    ("Opal (boulder) polished",                            "crystal","small",  5,    "Australia",       220.00, "Polished boulder opal cabochon. Opal veins in ironstone matrix."),
    ("Lapis Lazuli (raw AA)",                             "crystal","small",  100,  "Afghanistan",      65.00, "AA-grade raw lapis lazuli. Deep blue with golden pyrite flecks."),
    ("Lapis Lazuli (polished sphere)",                    "crystal","medium", 400,  "Afghanistan",      95.00, "Polished lapis lazuli sphere. Deep blue with golden flecks."),
    ("Malachite (polished slab)",                         "crystal","small",  150,  "DRC",              28.00, "Polished malachite slab. Concentric green bands."),
    ("Malachite (dragon sculpture)",                      "crystal","small",  100,  "DRC",              38.00, "Hand-carved malachite dragon sculpture. Detailed Chinese style."),
    ("Labradorite (polished palm stone)",                 "crystal","medium", 200,  "Madagascar",       35.00, "Polished labradorite palm stone. Grey base with blue iridescent flash."),
    ("Labradorite (full-spectrum polished sphere)",       "crystal","medium", 350,  "Madagascar",      145.00, "AAA full-spectrum labradorite sphere. Intense multi-color flash."),
    ("Moonstone (rainbow polished)",                      "crystal","small",  10,   "India/Sri Lanka",  45.00, "Polished rainbow moonstone cabochon. Blue-white iridescence."),
    ("Moonstone (cat's eye polished)",                    "crystal","small",  10,   "Sri Lanka",        65.00, "Polished cat's eye moonstone cabochon. Distinct chatoyant band."),
    ("Sunstone (Oregon polished)",                        "crystal", "low",    10,   "USA",              35.00, "Polished Oregon sunstone cabochon. Orange with copper-sparks."),
    ("Moldavite (small rough)",                           "crystal","small",  1,    "Czech Republic",  185.00, "Small moldavite rough. Translucent green tektite, formed by meteorite impact 15M years ago."),
    ("Moldavite (large polished)",                        "crystal","small",  5,    "Czech Republic",  580.00, "Large polished moldavite specimen. Rare collector-grade green tektite."),
    ("Charoite (polished slab)",                          "crystal","small",  100,  "Russia",           65.00, "Polished charoite slab. Purple with black and white swirling patterns."),
    ("Sugilite (polished cab)",                           "crystal","small",  10,   "South Africa",   145.00, "Polished sugilite cabochon. Deep magenta-purple, rare."),
    ("Larimar (AAA polished)",                            "crystal","small",  10,   "Dominican Rep.",  220.00, "AAA polished larimar cabochon. Caribbean blue with white patterns."),
    ("Amazonite (polished palm stone)",                   "crystal","medium", 200,  "Madagascar/Russia",28.00, "Polished amazonite palm stone. Turquoise with white streaks."),
    ("Prehnite (polished)",                           "crystal","small",  100,  "Australia",     38.00, "Polished prehnite specimen. Pale green translucent."),
    ("Chrysoberyl (alexandrite facet rough)",             "crystal","small",  1,    "Brazil",     1480.00, "Facetable chrysoberyl alexandrite rough. Color-change variety."),
    ("Chrysoberyl (cat's eye polished cab)",              "crystal","small",  3,    "Sri Lanka",     285.00, "Polished chrysoberyl cat's eye cabochon. Distinct chatoyant band."),
    ("Diopside (chrome) polished",                        "crystal","small",  10,   "Russia",         45.00, "Polished chrome diopside cabochon. Vivid forest green."),
    ("Kyanite (blue polished)",                           "crystal","small",  30,   "Brazil/Nepal",   22.00, "Polished blue kyanite specimen. Translucent deep blue."),
    ("Iolite (polished cab)",                             "crystal","small",  10,   "India",         28.00, "Polished iolite cabochon. Violet-blue, sometimes Viking's compass."),
    ("Spinel (red, facet rough)",                          "crystal","small",  2,    "Tanzania",       380.00, "Facetable red spinel rough. Vivid red, rare and precious."),
    ("Spinel (blue, polished cab)",                       "crystal","small",  5,    "Vietnam",       285.00, "Polished blue spinel cabochon. Cobalt-blue color."),
    ("Spodumene (kunzite polished)",                      "crystal","small",  30,   "Afghanistan",    65.00, "Polished kunzite (pink spodumene). Translucent pink."),
    ("Spodumene (hiddenite polished)",                    "crystal","small",  10,   "Afghanistan",   145.00, "Polished hiddenite (green spodumene). Vivid green, rare."),
    ("Apatite (neon blue polished)",                      "crystal","small",  5,    "Madagascar",     85.00, "Polished neon-blue apatite. Vivid Caribbean blue."),
    ("Sphene (titanite facet rough)",                     "crystal","small",  2,    "Pakistan",      485.00, "Facetable sphene (titanite) rough. High dispersion - rainbow sparkle."),
    ("Rhodochrosite (raw AA, polished)",                  "crystal","small",  30,   "Argentina",      85.00, "AA polished rhodochrosite. Pink-red with white banded patterns."),
    ("Rhodonite (polished cab)",                          "crystal","small",  20,   "Peru",            45.00, "Polished rhodonite cabochon. Pink with black manganese veining."),
    ("Chrysoprase (AAA polished)",                        "crystal","small",  10,   "Australia",      145.00, "AAA polished chrysoprase cabochon. Apple-green translucent."),
    ("Carnelian (tumbled AA)",                            "crystal","small",  15,   "Brazil/Madagascar", 8.00, "Tumbled AA carnelian. Red-orange translucent agate."),
    ("Carnelian (polished cab)",                          "crystal","small",  10,   "Madagascar",      18.00, "Polished carnelian cabochon. Deep orange-red translucent."),
    ("Agate (Botswana) polished slab",                    "crystal","small",  100,  "Botswana",        22.00, "Polished Botswana agate slab. Concentric white-purple banding."),
    ("Agate (moss) polished slab",                        "crystal","small",  100,  "India",            18.00, "Polished moss agate slab. Translucent with green dendritic inclusions."),
    ("Agate (blue lace) polished slab",                   "crystal","small",  100,  "Namibia",         28.00, "Polished blue lace agate slab. Delicate blue-white lace patterns."),
    ("Agate (fire) polished cab",                         "crystal","small",  5,    "USA",            145.00, "Polished fire agate cabochon. Translucent with iridescent red-orange flash."),
    ("Jasper (ocean) polished slab",                      "crystal","small",  150,  "Madagascar",       22.00, "Polished ocean jasper slab. Multi-color orbicular patterns."),
    ("Jasper (polychrome polished palm stone)",            "crystal","medium", 250,  "Madagascar",       35.00, "Polished polychrome jasper palm stone. Multiple colors and patterns."),
    ("Jasper (red) polished palm stone",                  "crystal","medium", 250,  "Brazil",             22.00, "Polished red jasper palm stone. Deep brick red."),
    ("Tiger's Eye (gold polished slab)",                  "crystal","small",  150,  "South Africa",    18.00, "Polished gold tiger's eye slab. Chatoyant gold-brown bands."),
    ("Tiger's Eye (blue polished slab)",                  "crystal","small",  150,  "South Africa",    28.00, "Polished blue (Hawk's Eye) tiger's eye slab. Chatoyant blue."),
    ("Tiger's Eye (red polished slab)",                   "crystal","small",  150,  "South Africa",    22.00, "Polished red (Bull's Eye) tiger's eye slab. Chatoyant red-brown."),
    ("Petrified Wood (polished slab)",                    "crystal","medium", 500,  "Madagascar",        35.00, "Polished petrified wood slab. Ancient wood replaced by silica, multi-color preserved."),
    ("Aventurine (green polished palm stone)",            "crystal","medium", 200,  "India",            22.00, "Polished green aventurine palm stone. Green quartz with mica inclusions."),
    ("Aventurine (blue polished palm stone)",             "crystal","medium", 200,  "India",            28.00, "Polished blue aventurine palm stone. Blue quartz with mica sparkles."),
    ("Obsidian (snowflake polished sphere)",              "crystal","medium", 400,  "Mexico",            38.00, "Polished snowflake obsidian sphere. Black with white snowflake-pattern inclusions."),
    ("Obsidian (Apache tear polished cab)",              "crystal","small",  5,    "USA",            12.00, "Polished Apache tear obsidian cabochon. Translucent black."),
    ("Obsidian (rainbow polished slab)",                  "crystal","small",  150,  "Mexico",           45.00, "Polished rainbow obsidian slab. Iridescent bands of purple-green-gold."),
    ("Onyx (black polished slab)",                        "crystal","small",  150,  "Brazil/Mexico",    18.00, "Polished black onyx slab. Solid black chalcedony."),
    ("Onyx (striped polished slab)",                      "crystal","small",  150,  "Brazil/Mexico",    22.00, "Polished striped onyx slab. Black and white parallel bands."),
    ("Bloodstone (polished cab)",                         "crystal","small",  10,   "India",            28.00, "Polished bloodstone cabochon. Dark green jasper with red iron-oxide spots."),
    ("Sodalite (raw polished)",                           "crystal","small",  200,  "Brazil",            18.00, "Polished sodalite specimen. Deep blue with white calcite veining."),
    ("Phenakite (facet rough)",                            "crystal","small",  1,    "Madagascar",      980.00, "Facetable phenakite rough. Extremely rare beryllium silicate."),
    ("Phenakite (polished cab)",                           "crystal","small",  2,    "Madagascar",     1480.00, "Polished phenakite cabochon. Extremely rare collector piece."),
    ("Fluorite (YAG - synthetic for comparison)",                  "crystal","small",  5,    "lab",            18.00, "Synthetic yttrium aluminum garnet. Reference sample for collectors."),
    ("Calcite (honey onyx geode)",                        "geode", "medium",  1500, "Pakistan",       220.00, "Honey onyx calcite geode. Translucent amber interior."),
    ("Quartz geode (clear Arkansas)",                     "geode", "medium",  800,  "USA",            145.00, "Arkansas clear quartz geode. Crystals lining a hollow center."),
    ("Agate geode (Brazilian)",                            "geode", "small",   400,  "Brazil",         65.00, "Brazilian agate geode. Concentric bands of microcrystalline quartz."),
    ("Agate geode (Uruguayan, large)",                    "geode", "large",   3000, "Uruguay",       380.00, "Large Uruguayan agate geode. Multi-band concentric agate."),
    ("Septarian nodule (dragon)",                                     "geode","medium",  2000, "USA",            180.00, "Septarian nodule - calcite/aragonite concretion with yellow calcite and grey limestone."),
    ("Pyrite geode (Spanish)",                             "geode","medium",  1500, "Spain",        145.00, "Pyrite geode from Navajun, Spain. Cubic pyrite crystals lining hollow."),
    ("Celestite geode (Madagascar)",                       "geode","medium",  1200, "Madagascar",    110.00, "Celestite geode. Pale blue strontium sulfate crystals."),
    ("Amethyst geode (single half, mini)",                  "geode","small",   100,  "Brazil",         28.00, "Single half mini amethyst geode. Druzy purple interior."),
    ("Amethyst geode (single half, medium)",                "geode","medium",  500,  "Brazil",         85.00, "Single half medium amethyst geode. Visible druzy crystals."),
    ("Amethyst geode (single half, large)",                 "geode","large",   2000, "Brazil",        245.00, "Single half large amethyst geode. Museum-quality druzy."),
    ("Geode (chalcedony rose - rare)",                       "geode","medium",  400,  "Argentina",     145.00, "Pink chalcedony rose geode. Rose-shaped crystalline formation."),
    ("Agate nodule (Thunder Egg, raw)",                     "geode","medium",  300,  "USA",            45.00, "Thunder egg agate nodule. Hollow volcanic agate formation from Oregon."),
    ("Scolecite crystal cluster",                          "crystal","small",   50,  "India",         35.00, "Scolecite crystal cluster. Acicular white natrolite-family zeolite."),
    ("Apophyllite crystal cluster (green)",                 "crystal","small",   80,  "India",         65.00, "Green apophyllite crystal cluster. Stunning clarity and color."),
    ("Apophyllite crystal cluster (clear)",                  "crystal","small",   80,  "India",         45.00, "Clear apophyllite crystal cluster. Glassy transparent crystals."),
    ("Stilbite crystal cluster",                            "crystal","small",   60,  "India",         28.00, "Stilbite crystal cluster. Peach-blush sheaf-like crystals."),
    ("Heulandite crystal cluster",                          "crystal","small",   50,  "India",         35.00, "Heulandite crystal cluster. Colorless to green platy crystals."),
    ("Cavansite crystal cluster",                            "crystal","small",   30,  "India",         85.00, "Cavansite crystal cluster. Vivid electric-blue radiating crystals."),
    ("Pentagonite crystal cluster",                            "crystal","small",   20,  "India",        145.00, "Pentagonite crystal cluster. Deep blue sister mineral to cavansite, very rare."),
    ("Stilbite cobaltoan calcite",                          "crystal","small",   80,  "DRC",          145.00, "Cobaltoan calcite. Hot pink cobalt-bearing calcite."),
    ("Smithsonite (pink polished)",                         "crystal","small",   30,  "Namibia",       85.00, "Polished pink smithsonite cabochon. Botryoidal habit."),
    ("Adamite (yellow crystal cluster)",                    "crystal","small",   40,  "Mexico",        45.00, "Adamite crystal cluster. Yellow-green zinc arsenate."),
    ("Vanadinite crystal cluster",                           "crystal","small",   30,  "Morocco",       65.00, "Vanadinite crystal cluster. Bright red-orange hexagonal crystals on matrix."),
    ("Wulfenite crystal cluster",                            "crystal","small",   40,  "China",         85.00, "Wulfenite crystal cluster. Orange-yellow tabular crystals."),
    ("Dioptase crystal cluster",                            "crystal","small",   30,  "DRC",         220.00, "Dioptase crystal cluster. Vivid emerald-green copper cyclosilicate."),
    ("Azurite crystal cluster",                             "crystal","small",   50,  "Morocco",       38.00, "Azurite crystal cluster. Deep blue copper carbonate."),
    ("Malachite (botryoidal polished)",                     "crystal","small",   80,  "DRC",          28.00, "Polished botryoidal malachite specimen. Grape-cluster formation."),
    ("Chrysocolla polished slab",                           "crystal","small",  150,  "Peru",           35.00, "Polished chrysocolla slab. Sky-blue to teal copper silicate."),
    ("Shattuckite polished cab",                            "crystal","small",   10,  "DRC",          145.00, "Polished shattuckite cabochon. Vivid blue copper silicate, rare."),
    ("Grandidierite polished cab",                          "crystal","small",    3,  "Madagascar",  1480.00, "Polished grandidierite cabochon. Turquoise-blue, among the rarest gemstones."),
    ("Jeremejevite facet rough",                            "crystal","small",    1,  "Namibia",      980.00, "Facetable jeremejevite rough. Pale blue, extremely rare collector gem."),
    ("Painite facet rough",                                  "crystal","small",    1,  "Myanmar",     88000.00, "Facetable painite rough. Rarest gem mineral on Earth."),
    ("Benitoite polished cab",                              "crystal","small",    5,  "California",  580.00, "Polished benitoite cabochon. Vivid blue California state gem."),
    ("Sugilite (gemmy polished)",                            "crystal","small",    5,  "South Africa", 285.00, "Gem-quality polished sugilite cabochon. Deep magenta-purple, rare."),
    ("Rhodizite polished",                                    "crystal","small",    3,  "Madagascar",  85.00, "Polished rhodizite. Yellow boron-beryllium silicate, rare."),
    ("Pollucite (cesium-bearing)",                                  "crystal","small",    5,  "Canada",       45.00, "Pollucite specimen. Cesium-rich zeolite, rare collector mineral."),
    ("Dumortierite polished cab",                            "crystal","small",   10,  "USA",         35.00, "Polished dumortierite cabochon. Blue fibrous aluminum borosilicate."),
    ("Prehnite (epimorph) cluster",                         "crystal","small",   40,  "USA",         28.00, "Prehnite epimorph cluster. Prehnite overgrowing another mineral."),
    ("Stibiotantalite polished",                             "crystal","small",    5,  "Mozambique", 285.00, "Polished stibiotantalite. Tantalum-niobium antimony oxide, very rare."),
    ("Red Beryl (facet rough)",                              "crystal","small",    1,  "USA",        1980.00, "Facetable red beryl (bixiehellium) rough. Among the rarest gemstones."),
    ("Imperial Topaz (polished)",                            "crystal","small",    5,  "Ouro Preto", 480.00, "Polished imperial topaz cabochon. Rare peach-orange-gold."),
    ("Ametrine (polished)",                                  "crystal","small",   10,  "Bolivia",    65.00, "Polished ametrine cabochon. Bicolor amethyst-citrine from Bolivia."),
    ("Grape Agate (polished)",                                "crystal","small",   30,  "Indonesia",  45.00, "Polished grape agate specimen. Botryoidal purple chalcedony."),
    ("Ocean Jasper (polished)",                              "crystal","small",   80,  "Madagascar",  38.00, "Polished ocean jasper specimen. Multi-color orbicular patterns."),
    ("K2 Jasper (polished slab)",                            "crystal","small",  100,  "Pakistan",    22.00, "Polished K2 jasper slab. Granite with azurite blue spots."),
    ("Crazy Lace Agate (polished slab)",                     "crystal","small",  150,  "Mexico",      22.00, "Polished crazy lace agate slab. Complex swirling patterns."),
    ("Laguna Lace Agate (polished slab)",                    "crystal","small",  150,  "Mexico",      28.00, "Polished Laguna lace agate slab. Multi-color lace patterns."),
    ("Pink Botswana Agate (polished)",                       "crystal","small",  150,  "Botswana",    28.00, "Polished pink Botswana agate slab. Soft pink banded."),
    ("Black Tourmaline (polished point)",                    "crystal","small",   30,  "Brazil",     22.00, "Polished black tourmaline point. Classic protection stone."),
    ("Staurolite (fairy cross, natural twin)",                "crystal","small",   10,  "Russia",      28.00, "Staurolite fairy cross. Natural twinned 60-degree cross."),
    ("Faden Quartz (with phantom line)",                     "crystal","small",   60,  "Pakistan",   35.00, "Faden quartz point with growth-line phantoms."),
    ("Lemurian Quartz (polished)",                             "crystal","medium",  100,  "Brazil",      38.00, "Lemurian seed quartz point. Horizontal striations, classic metaphysical crystal."),
    ("Herkimer Diamond (quartz, AA polished)",                "crystal","small",    2,  "USA",        18.00, "AA Herkimer diamond. Water-clear double-terminated quartz from NY."),
    ("Tibetan Quartz (polished)",                             "crystal","medium",  200,  "Tibet",      65.00, "Tibetan quartz cluster on matrix. Remote high-altitude quartz."),
    ("Garden Quartz (lodolite) polished slab",               "crystal","small",  150,  "Brazil",     85.00, "Polished garden quartz slab. Quartz with green chlorite garden inclusions."),
    ("Lithium Quartz (polished)",                             "crystal","small",   50,  "Brazil",     28.00, "Polished lithium quartz. Quartz with lavender to pink lithium inclusions."),
    ("Azeztulite (polished)",                                  "crystal","small",   20,  "USA",        85.00, "Polished azeztulite specimen. Named Azez mineral, marketed as a high-vibration stone."),
    ("Natrolite crystal cluster",                              "crystal","small",   30,  "USA",        22.00, "Natrolite crystal cluster. Acicular white zeolite."),
    ("Mesolite crystal cluster",                               "crystal","small",   25,  "USA",        28.00, "Mesolite crystal cluster. White acicular zeolite."),
    ("Thomsonite polished cab",                                "crystal","small",    5,  "USA",        35.00, "Polished thomsonite cabochon. Pink zeolite with concentric eyes."),
    ("Prehnite with epidote cluster",                           "crystal","small",   60,  "Pakistan",   28.00, "Prehnite with epidote crystal cluster. Green and pistachio."),
    ("Actinolite (polished specimen)",                          "crystal","small",   80,  "Russia",      18.00, "Polished actinolite specimen. Dark green fibrous amphibole."),
    ("Nephrite jade (polished)",                                "crystal","small",   50,  "Russia",      28.00, "Polished nephrite jade specimen. Tremolite-actinolite jade."),
    ("Jadeite jade (polished AA)",                              "crystal","small",    3,  "Burma",      1480.00, "AA polished jadeite jade cabochon. Imperial jade green."),
    ("Kunzite (facet rough AA)",                                "crystal","small",    5,  "Afghanistan", 485.00, "Facetable AA kunzite rough. Vivid pink spodumene."),
    ("Hiddenite (facet rough AA)",                              "crystal","small",    3,  "Afghanistan", 1480.00, "Facetable AA hiddenite rough. Vivid green spodumene, very rare."),
    ("Precious Coral (polished cab)",                            "crystal","small",    3,  "Italy",       180.00, "Polished precious coral cabochon. Red Mediterranean coral, gem-quality."),
    ("Ammolite (polished cab)",                                  "crystal","small",    3,  "Canada",      220.00, "Polished ammolite cabochon. Iridescent fossilized ammonite shell."),
    ("Dinosaur Bone (polished slab, agatized)",                  "crystal","small",  100,  "USA",        85.00, "Polished agatized dinosaur bone slab. Multi-color fossil replacement."),
    ("Trilobite fossil (polished)",                              "crystal","small",   30,  "Morocco",    65.00, "Polished trilobite fossil specimen. Phacops species."),
    ("Coprolite (polished, dino dung)",                           "crystal","small",   40,  "USA",        38.00, "Polished coprolite. Fossilized dinosaur excrement, novelty specimen."),
    ("Whale bone (fossilized, polished slab)",                    "crystal","small",  150,  "USA",        45.00, "Polished fossilized whale bone slab."),
    ("Ammonite fossil (whole, polished)",                          "crystal","medium", 200,  "Madagascar",  85.00, "Polished whole ammonite fossil. Sliced and polished to show chambers."),
    ("Turquoise (polished cab, AA)",                              "crystal","small",    5,  "USA",        145.00, "Polished AA turquoise cabochon. Robin's egg blue with matrix."),
    ("Turquoise (raw nugget)",                                    "crystal","small",   20,  "USA",        38.00, "Raw turquoise nugget. Natural blue-green with host rock."),
    ("Lapis (AA polished slab)",                                   "crystal","small",  150,  "Afghanistan", 65.00, "Polished AA lapis lazuli slab. Deep blue, minimal calcite veining."),
    ("Coral (polished branch, red)",                               "crystal","small",   80,  "Italy",      45.00, "Polished red coral branch. Mediterranean precious coral."),
    ("Pearl (freshwater, AA polished)",                             "crystal","small",    2,  "China",       35.00, "Polished AA freshwater pearl. High luster, near-round."),
    ("Pearl (Mabe, polished, AAA)",                                 "crystal","small",    5,  "Japan",      85.00, "Polished AAA Mabe pearl. Cultured blister pearl."),
    ("South Sea Pearl (polished, AAA)",                              "crystal","small",    2,  "Australia", 580.00, "Polished AAA South Sea pearl. Large white/golden cultured pearl."),
    ("Tahitian Black Pearl (polished, AA)",                          "crystal","small",    2,  "French Polynesia",285.00, "Polished AA black Tahitian pearl. Cultured black-lipped oyster."),
    ("Abalone Shell (polished, iridescent)",                          "crystal","small",   30,  "New Zealand", 22.00, "Polished iridescent abalone shell. Paua shell, rainbow colors."),
    ("Ammolite Specimen (rough, iridescent)",                          "crystal","small",   50,  "Canada",      85.00, "Rough iridescent ammolite specimen."),
    ("Fossil Fern (polished slab)",                                     "crystal","small",  150,  "USA",        28.00, "Polished fossil fern slab. Carboniferous-era plant fossils in shale."),
    ("Stromatolite (polished slab)",                                    "crystal","small",  150,  "USA",        38.00, "Polished stromatolite slab. Ancient cyanobacteria fossils, layered."),
    ("Ammonite Cleoniceras (cleaved pair)",                            "crystal","medium", 200,  "Madagascar", 65.00, "Cleaved Cleoniceras ammonite pair. Both halves showing chambers."),
    ("Petrified Palm Root (polished slab)",                              "crystal","small",  150,  "USA",        45.00, "Polished petrified palm root slab. Multi-color preserved palm tree root."),
    ("Gibeon Meteorite (slice, polished)",                              "crystal","small",   30,  "Namibia",    85.00, "Polished Gibeon meteorite slice. Widmanstätten pattern from iron-nickel meteorite."),
    ("Seymchan Meteorite (slice, polished)",                             "crystal","small",   30,  "Russia",    145.00, "Polished Seymchan meteorite slice. Pallasite with olivine crystals."),
    ("Moldavite (small natural)",                                       "crystal","small",    1,  "Czech",      85.00, "Small natural moldavite. Translucent green tektite, classic size."),
    ("Indigo Gabbro (polished sphere)",                                 "crystal","medium", 400,  "Madagascar",  38.00, "Polished indigo gabbro sphere. Black with indigo blue patches."),
    ("Ruby in Zoisite (anyolite) polished",                              "crystal","medium", 250,  "Tanzania",  48.00, "Polished ruby-in-zoisite (anyolite). Green with ruby crystals."),
    ("Ruby in Fuchsite polished",                                        "crystal","medium", 250,  "India",     45.00, "Polished ruby-in-fuchsite. Green with ruby spots."),
    ("Stromatolite (cabochon, polished)",                                "crystal","small",   10,  "USA",        28.00, "Polished stromatolite cabochon. Layered ancient fossils."),
    ("Turritella Agate (polished slab)",                                 "crystal","small",  150,  "USA",        22.00, "Polished turritella agate slab. Embedded fossil snail shells."),
    ("Dendritic Agate (polished cab)",                                   "crystal","small",    5,  "India",      18.00, "Polished dendritic agate cabochon. Translucent with black tree-like inclusions."),
    ("Enhydro Agate (polished)",                                          "crystal","small",   50,  "Brazil",     38.00, "Polished enhydro agate. Quartz geode with trapped water bubble."),
    ("Phantom Quartz (polished)",                                         "crystal","small",   50,  "Brazil",     28.00, "Polished phantom quartz. Clear quartz with internal ghost crystal."),
    ("Tourmalinated Quartz (polished)",                                    "crystal","small",   50,  "Brazil",     32.00, "Polished tourmalinated quartz. Black tourmaline needles in clear quartz."),
    ("Rutilated Quartz (polished, golden)",                                "crystal","small",   80,  "Brazil",     45.00, "Polished golden rutilated quartz. Gold rutile needles in clear quartz."),
    ("Rutilated Quartz (polished, silver)",                                 "crystal","small",   80,  "Brazil",     48.00, "Polished silver rutilated quartz. Silver rutile needles in clear quartz."),
    ("Hematite Quartz (polished)",                                          "crystal","small",   80,  "Brazil",     28.00, "Polished hematite quartz. Hematite-included quartz, deep red."),
    ("Strawberry Quartz (polished)",                                         "crystal","small",   60,  "Russia",     28.00, "Polished strawberry quartz. Pink hematite-included quartz."),
    ("Blue Quartz (polished, cabochon)",                                    "crystal","small",    5,  "Brazil",     22.00, "Polished blue quartz cabochon. Dumortierite-included blue quartz."),
    ("Aqua Aura Quartz (polished cluster)",                                  "crystal","small",   80,  "USA",        35.00, "Polished aqua aura quartz cluster. Quartz bonded with gold/platinum for iridescent blue."),
    ("Rainbow Aura Quartz (polished cluster)",                                 "crystal","small",   80,  "USA",        38.00, "Polished rainbow aura quartz cluster. Iridescent titanium coating."),
    ("Opal Aura Quartz (polished cluster)",                                     "crystal","small",   80,  "USA",        35.00, "Polished opal aura quartz cluster. Opalescent rainbow aura."),
    ("Sulfur (natural yellow crystals)",                                       "crystal","small",  100,  "Sicily",      22.00, "Natural sulfur crystals. Bright yellow, classic mineral specimen."),
    ("Bismuth (crystal ingot AA)",                                              "crystal","medium", 250, "USA",         28.00, "AA bismuth crystal ingot. Famous iridescent hopper-crystal staircase."),
    ("Realgar (natural crystal)",                                                 "crystal","small",   50,  "China",       38.00, "Natural realgar crystal cluster. Deep red arsenic sulfide."),
    ("Orpiment (natural crystal)",                                                "crystal","small",   50,  "China",       35.00, "Natural orpiment crystal cluster. Golden yellow arsenic sulfide, classic mineral."),
    ("Stibnite (natural crystal cluster)",                                       "crystal","medium", 200,  "China",       45.00, "Natural stibnite crystal cluster. Metallic grey-bladed antimony sulfide."),
    ("Galena (natural cube)",                                                     "crystal","small",  100,  "USA",         28.00, "Natural galena cube. Lead sulfide with metallic silver-grey lustre."),
    ("Pyrrhotite (polished slab)",                                                "crystal","small",  100,  "China",       28.00, "Polished pyrrhotite slab. Bronze-colored iron sulfide, weakly magnetic."),
    ("Bornite (peacock ore) polished",                                            "crystal","small",   80,  "Mexico",      38.00, "Polished bornite specimen. Tarnishes to iridescent peacock colors."),
    ("Chalcopyrite (peacock ore) polished",                                        "crystal","small",   80,  "Mexico",      32.00, "Polished chalcopyrite specimen. Iridescent tarnish, classic ore."),
    ("Covellite polished",                                                          "crystal","small",   50,  "Italy",       45.00, "Polished covellite specimen. Deep purple-blue iridescent copper sulfide."),
    ("Chalcocite polished",                                                          "crystal","small",   50,  "USA",         32.00, "Polished chalcocite specimen. Dark grey copper sulfide."),
    ("Molybdenite polished",                                                         "crystal","small",   20,  "Australia",   28.00, "Polished molybdenite specimen. Lead-grey molybdenum sulfide."),
    ("Wolframite polished",                                                          "crystal","small",  100,  "China",       32.00, "Polished wolframite specimen. Iron-manganese tungstate, tungsten ore."),
    ("Cassiterite polished",                                                         "crystal","small",   80,  "Bolivia",     38.00, "Polished cassiterite specimen. Tin oxide ore, black crystal."),
    ("Magnetite polished",                                                          "crystal","small",  100,  "USA",         22.00, "Polished magnetite specimen. Magnetic iron oxide ore."),
    ("Hematite polished",                                                            "crystal","small",  100,  "Brazil",      18.00, "Polished hematite specimen. Iron oxide ore, metallic grey."),
    ("Goethite polished",                                                            "crystal","small",   80,  "Morocco",     28.00, "Polished goethite specimen. Iron oxyhydroxide, iridescent."),
    ("Limonite polished",                                                            "crystal","small",  100,  "USA",         22.00, "Polished limonite specimen. Hydrated iron oxide, ochre-yellow."),
    ("Malachite (matrix specimen)",                                                  "crystal","small",  200,  "DRC",        28.00, "Malachite matrix specimen. Massive botryoidal malachite."),
    ("Chrysocolla in matrix specimen",                                              "crystal","small",  150,  "USA",         35.00, "Chrysocolla in matrix specimen. Blue-green copper silicate with quartz."),
    ("Petrified Dinosaur Bone (polished slab)",                                  "crystal","small",  150,  "USA",         85.00, "Polished agatized dinosaur bone slab. Multi-color fossil."),
    ("Stibnite (cabinet specimen, large)",                                          "crystal","large",  600,  "China",      145.00, "Large cabinet-grade stibnite crystal cluster. Long metallic blades."),
    ("Fluorite (YAG - synthetic comparison)",                                       "crystal","small",    5,  "lab",         18.00, "Synthetic YAG. Reference specimen."),
    ("Citrine (natural AAA polished)",                                                "crystal","medium", 250,  "Brazil",     145.00, "AAA natural untreated citrine polished specimen. Rare."),
    ("Spodumene (kunzite polished cabochon AAA)",                                  "crystal","small",    5,  "Afghanistan",285.00, "AAA polished kunzite cabochon. Vivid pink, top gem."),
    ("Alexandrite (polished cab, AA)",                                                  "crystal","small",    5,  "Brazil",   1980.00, "AA polished alexandrite cabochon. Color-change green to red."),
    ("Pezzottaite (polished cab)",                                                       "crystal","small",    3,  "Madagascar",1480.00, "Polished pezzottaite cabochon. Pink-red beryl, very rare."),
    ("Rhodolite Garnet (facet rough)",                                                  "crystal","small",    3,  "Tanzania",  85.00, "Facetable rhodolite garnet rough. Pink-red almandine-pyrope."),
    ("Demantoid Garnet (facet rough AA)",                                                "crystal","small",    2,  "Russia",   1480.00, "Facetable AA demantoid garnet rough. Green andradite with horsetail inclusions."),
    ("Tsavorite Garnet (facet rough AA)",                                                 "crystal","small",    2,  "Tanzania", 1980.00, "Facetable AA tsavorite garnet. Vivid green grossular garnet."),
    ("Star Ruby polished",                                                                 "crystal","small",    5,  "Sri Lanka", 680.00, "Polished star ruby cabochon. Six-ray star, deep color."),
    ("Star Sapphire (polished)",                                                              "crystal","small",    5,  "Sri Lanka", 480.00, "Polished star sapphire cabochon. Six-ray star, blue."),
    ("Cat's Eye Chrysoberyl polished",                                                        "crystal","small",    3,  "Sri Lanka", 380.00, "Polished cat's eye chrysoberyl cabochon. Sharp chatoyant band."),
    ("Cat's Eye Tourmaline polished",                                                          "crystal","small",    5,  "Brazil",  145.00, "Polished cat's eye tourmaline cabochon. Multi-color chatoyancy."),
    ("Hawk's Eye Cabochon",                                                                    "crystal","small",    5,  "South Africa", 18.00, "Polished Hawk's Eye (blue tiger's eye) cabochon. Chatoyant blue."),
    ("Pietersite polished cabochon",                                                            "crystal","small",    5,  "Namibia",  85.00, "Polished pietersite cabochon. Multi-hued chatoyant crocidolite."),
    ("Tanzanite Cabochon (polished AA)",                                                       "crystal","small",    5,  "Tanzania", 480.00, "AA polished tanzanite cabochon. Violet-blue color."),
    ("Maw Sit Sit (polished cabochon)",                                                         "crystal","small",    5,  "Burma",   485.00, "Polished maw sit sit cabochon. Multi-color jade-related, rare."),
    ("Chrysoprase Cabochon (AA polished)",                                                    "crystal","small",    5,  "Australia", 145.00, "AA polished chrysoprase cabochon. Apple green, translucent."),
    ("Sugilite Cabochon (AA polished)",                                                       "crystal","small",    3,  "South Africa", 285.00, "AA polished sugilite cabochon. Deep magenta-purple, rare."),
    ("Larimar Cabochon (polished AAA)",                                                        "crystal","small",    5,  "DR",     280.00, "AAA polished larimar cabochon. Caribbean blue with white."),
    ("Prehnite Cabochon (polished)",                                                            "crystal","small",    5,  "Australia",  22.00, "Polished prehnite cabochon. Pale green translucent."),
    ("Stichtite (cabochon polished)",                                                          "crystal","small",    3,  "Tasmania", 145.00, "Polished stichtite cabochon. Purple serpentine-carbonate."),
    ("Charoite Cabochon (polished AA)",                                                         "crystal","small",    5,  "Russia",  220.00, "AA polished charoite cabochon. Purple with black and white swirls."),
    ("Pietersite Cabochon (AA polished)",                                                        "crystal","small",    5,  "Namibia", 145.00, "AA polished pietersite cabochon. Vivid multi-hued chatoyant."),
    ("Sugilite Cabochon (AA polished deep)",                                                       "crystal","small",    3,  "South Africa", 480.00, "AA deep color sugilite cabochon. Vivid magenta-purple, top gem."),
    ("Stichtite Cabochon (polished AA)",                                                          "crystal","small",    3,  "Tasmania", 245.00, "AA polished stichtite cabochon. Vivid purple serpentine."),
    ("Vesuvianite (Idocrase) Cabochon",                                                          "crystal","small",    5,  "Italy",   28.00, "Polished vesuvianite (idocrase) cabochon. Green calcium silicate."),
    ("Epidote Cabochon (polished)",                                                                "crystal","small",    5,  "Pakistan", 22.00, "Polished epidote cabochon. Pistachio-green colored."),
    ("Clinozoisite Cabochon",                                                                       "crystal","small",    5,  "Pakistan",  22.00, "Polished clinozoisite cabochon. Green calcium-aluminum silicate."),
    ("Petrified Fern (polished, AAA)",                                                              "crystal","small",  150,  "USA",        38.00, "Polished AAA fossil fern slab."),
    ("Copal Amber (polished, AAA)",                                                                 "crystal","small",   20,  "Madagascar", 65.00, "Polished AAA copal amber. Young amber with insects sometimes preserved."),
    ("Dominican Blue Amber (polished AAA)",                                                       "crystal","small",    5,  "Dominican Rep.", 145.00, "Polished AAA blue amber. Rare blue fluorescent amber."),
    ("Baltic Amber (polished cabochon)",                                                          "crystal","small",    5,  "Russia",    45.00, "Polished Baltic amber cabochon. Ancient amber with insects possible."),
    ("Mexican Amber (polished cabochon AA)",                                                      "crystal","small",    5,  "Mexico",    28.00, "Polished AA Mexican amber cabochon. Clear to cognac amber."),
    ("Amber (Burmese) cabochon",                                                                     "crystal","small",    5,  "Burma",     85.00, "Polished Burmese amber cabochon. Rare cretaceous amber."),
    ("Jet (polished AA Victorian style)",                                                            "crystal","small",    5,  "England",  85.00, "Polished Victorian-style jet cabochon. Black fossilized wood."),
    ("Bog Oak (polished specimen)",                                                                  "crystal","small",   30,  "Ireland",   45.00, "Polished bog oak specimen. Black fossilized wood."),
    ("Tektite (general)",                                                                              "crystal","small",    2,  "Vietnam",   18.00, "Natural tektite specimen. Glassy meteorite-impact stone."),
    ("Libyan Desert Glass (polished)",                                                                "crystal","small",    5,  "Libya",    85.00, "Polished Libyan desert glass. Yellow-green silica glass from meteorite impact."),
    ("Darwin Glass (polished)",                                                                       "crystal","small",    5,  "Tasmania", 65.00, "Polished Darwin glass. Green silica glass from meteorite impact."),
    ("Aouelloul Glass",                                                                                "crystal","small",    5,  "Mauritania",38.00, "Polished Aouelloul glass. Silica glass from meteorite impact."),
    ("Wabar Glass",                                                                                     "crystal","small",    3,  "Saudi Arabia",145.00, "Polished Wabar glass. Rare impact glass from Wabar crater."),
    ("Pallasite (Seymchan) polished slab",                                                            "crystal","small",   50,  "Russia",    285.00, "Polished Seymchan pallasite slab. Olivine crystals in iron-nickel matrix."),
    ("Iron Meteorite (Gibeon) polished slice",                                                         "crystal","small",   30,  "Namibia",    85.00, "Polished Gibeon iron meteorite slice. Widmanstätten pattern etched."),
    ("Chondrite Meteorite (whole, polished)",                                                          "crystal","small",   30,  "Morocco",    45.00, "Polished chondrite meteorite specimen."),
    ("Bezoar (animal concretion, polished)",                                                          "crystal","small",   20,  "antiquarian", 145.00, "Polished bezoar. Concretion from animal digestive tract. Historical curiosity."),
    ("Kidney Stone (human, polished antique specimen)",                                                "crystal","small",    5,  "antiquarian", 245.00, "Polished antique human kidney stone. Historical pathology specimen."),
    ("Gout Stone (human, polished)",                                                                    "crystal","small",    2,  "antiquarian",285.00, "Polished human gout stone specimen. Urate crystal."),
    ("Gallstone (polished human specimen)",                                                              "crystal","small",    2,  "antiquarian",220.00, "Polished human gallstone specimen. Cholesterol stone."),
    ("Bladder Stone (animal, polished)",                                                                 "crystal","small",    5,  "antiquarian", 95.00, "Polished animal bladder stone specimen."),
    ("Phlebolite (vein stone, polished)",                                                                 "crystal","small",    2,  "antiquarian", 185.00, "Polished phlebolite (vein stone) specimen."),
    ("Salivary Stone (polished)",                                                                       "crystal","small",    2,  "antiquarian", 145.00, "Polished salivary stone specimen."),
    ("Quartz with petroleum inclusion",                                                                  "crystal","small",    5,  "Pakistan",  220.00, "Polished quartz with natural petroleum inclusion. Hydrocarbon trapped in crystal."),
    ("Enhydro Quartz (with water bubble)",                                                               "crystal","small",    5,  "Brazil",   145.00, "Polished enhydro quartz. Water bubble trapped for millions of years."),
]


# ============================================================
# BUILD CATALOG
# ============================================================
catalog = []
seen_skus = set()

# Elements
for symbol, atomic, name, form, price, desc in PERIODIC:
    if price is None:
        continue  # SKIP radioactive/synthetic
    safe_name = name.lower().replace(" ", "-").replace("/", "-").replace(",", "").replace("(", "").replace(")", "")
    sku = f"element-{symbol.lower()}-{safe_name}"
    if sku in seen_skus: continue
    seen_skus.add(sku)
    pricing = cp(price)
    catalog.append({
        "sku": sku,
        "category": "element",
        "atomic_number": atomic,
        "element": symbol,
        "name": f"{name} ({symbol})",
        "form": form,
        "wholesale_usd": pricing["wholesale_usd"],
        "customer_usd": pricing["customer_usd"],
        "description": desc,
        "availability": "in_stock",
        "is_element": True,
    })

# Crystals/Geodes
for name, cat, size, weight, origin, price, desc in CRYSTALS:
    safe = name.lower().replace(" ", "-").replace("/", "-").replace(",", "").replace("(", "").replace(")", "")
    sku_prefix = "geode" if cat == "geode" else "crystal"
    sku = f"{sku_prefix}-{safe[:50]}-{origin.lower()[:3]}"
    if sku in seen_skus: continue
    seen_skus.add(sku)
    pricing = cp(price)
    catalog.append({
        "sku": sku,
        "category": cat,
        "name": name,
        "size": size,
        "weight_grams": weight,
        "origin": origin,
        "wholesale_usd": pricing["wholesale_usd"],
        "customer_usd": pricing["customer_usd"],
        "description": desc,
        "availability": "in_stock",
        "is_element": False,
    })

# Sort by customer price
catalog.sort(key=lambda x: x["customer_usd"])

# Write
out_path = os.path.join(OUT_DIR, "dist-public-customer-pricing.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print(f"MASTER CATALOG BUILT")
print(f"{'='*70}")
print(f"Total SKUs: {len(catalog)}")
print(f"Elements: {sum(1 for c in catalog if c['is_element'])}")
print(f"Crystals: {sum(1 for c in catalog if c['category']=='crystal')}")
print(f"Geodes: {sum(1 for c in catalog if c['category']=='geode')}")

# Stats
prices = [c['customer_usd'] for c in catalog]
print(f"\nPrice range: ${min(prices):.2f} - ${max(prices):.2f}")
print(f"Average: ${sum(prices)/len(prices):.2f}")
print(f"Median: ${sorted(prices)[len(prices)//2]:.2f}")

# Categories breakdown
by_cat = {}
for c in catalog:
    by_cat[c['category']] = by_cat.get(c['category'], 0) + 1
print(f"\nBy category:")
for cat, count in sorted(by_cat.items()):
    print(f"  {cat}: {count}")

# Atomic number coverage
elements = [c for c in catalog if c.get('is_element')]
covered = sorted({c['atomic_number'] for c in elements})
print(f"\nElements covered: {len(covered)} of 118")
print(f"Atomic numbers: {covered}")

# Save to server.js path too (for the API)
output_path = r"C:\Users\KING\Projects\krysys-shop\server-data-catalog.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
print(f"\nMaster catalog: {out_path}")
print(f"API-ready copy: {output_path}")
print(f"File size: {os.path.getsize(out_path):,} bytes")