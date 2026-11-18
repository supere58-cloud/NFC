"""Unit cost and selling price for the NFC e-ink phone tag.

Run:  python3 pricing/calc.py
Edit the numbers in COSTS / MODULES / CHANNELS, re-run, done.

Target: profit = 2 x landed cost (a 200 % markup), measured AFTER the
selling channel has taken its fees. That means price = 3 x cost before
fees, a 66.7 % gross margin. A literal "200 % margin" (profit / price)
cannot exist: margin tops out below 100 %.

All money in USD. Labour is NOT in the cost: the profit pays for your time.
"""
MARKUP = 2.0            # profit as a multiple of landed cost (2.0 = 200 %)
IMPORT_VAT = 0.20       # import VAT/duty on module + shipping you can't reclaim
                        # (0.0 if you are VAT-registered and reclaim it)
WASTE = 0.05            # spare for dead modules and failed prints

# Per-unit costs other than the module (USD)
COSTS = {
    "printed case (PETG, power, failed prints)": {"adhesive": 0.40, "magnet": 0.60},
    "mount hardware (gel pad / 4 x 5x1.5 mm N52 + glue)": {"adhesive": 0.30, "magnet": 0.35},
    "packaging (bag or box, insert card)": {"adhesive": 0.60, "magnet": 0.60},
}

# name: (unit price, inbound shipping per unit at ~10 pcs, case build)
MODULES = {
    "AliExpress 1.54in keychain (cheapest listing)": (10.91, 0.00, "new cradle, measure first"),
    "Good Display DMPL0154FN1 tag":                  (13.96, 2.50, "C"),
    "Good Display GDP0154NF2 tag (ultra-thin)":      (17.76, 2.50, "C, check thickness"),
    "Shellrus 4-colour bare module":                 (25.00, 2.00, "A"),
    "Waveshare 1.54in NFC e-Paper (G)":              (26.63, 2.00, "B"),
    # bare panel $5.85 (buyepaper listing) + your own NFC driver board,
    # ~$5 at 100 pcs assembled: ESTIMATE, not a quote
    "Own build: GDEM0154F51H panel + own NFC board": (10.85, 1.00, "A, after board design"),
}

# Retail prices to test in the reverse table
TARGET_PRICES = [29, 39, 49, 59, 69]

# name: (percentage fee, fixed fee per order)
CHANNELS = {
    "in person / cash":          (0.000, 0.00),
    "own shop, card payment":    (0.030, 0.30),
    "Etsy (fees + payment)":     (0.095, 0.45),
}


# ---- screenless "tap to share" tag (Build D) ------------------------------
TAP_COSTS = {
    "printed puck (PETG, power, failed prints)": {"adhesive": 0.10, "magnet": 0.35},
    "mount hardware (3M disc / 4 x 5x1.5 mm N52 + glue)": {"adhesive": 0.15, "magnet": 0.35},
    "packaging (small card + bag)": {"adhesive": 0.40, "magnet": 0.40},
}
# name: (unit price, inbound shipping per unit at ~100 pcs, chip note)
TAP_MODULES = {
    "NTAG213 30mm anti-metal (GoToTags, 100 pcs)": (0.48, 0.15, "144 B"),
    "NTAG215 30mm anti-metal (Tagstand)":          (0.85, 0.15, "504 B"),
    "NTAG216 30mm anti-metal (GoToTags, low tier)": (0.98, 0.15, "888 B"),
    "NTAG424 DNA anti-metal (SEKUREX, 10 pcs)":    (1.25, 0.15, "416 B, anti-clone"),
}
TAP_TARGET_PRICES = [5, 8, 10, 15, 20]


def landed_cost(price, ship, variant, costs=None):
    module = (price + ship) * (1 + IMPORT_VAT)
    extras = sum(c[variant] for c in (costs or COSTS).values())
    return (module + extras) * (1 + WASTE)


def selling_price(cost, pct, fixed):
    """Price at which (price - fees - cost) = MARKUP * cost."""
    return ((1 + MARKUP) * cost + fixed) / (1 - pct)


def table(title, modules, costs, targets):
    print(f"\n=== {title} ===")
    head = f"{'module':47s} {'note':26s} {'var':8s} {'cost':>7s}"
    head += "".join(f" {c[:22]:>23s}" for c in CHANNELS)
    print(head)
    print("-" * len(head))
    for name, (price, ship, build) in modules.items():
        for var in ("adhesive", "magnet"):
            c = landed_cost(price, ship, var, costs)
            row = f"{name:47s} {build:26s} {var:8s} {c:7.2f}"
            row += "".join(f" {selling_price(c, *fee):23.2f}"
                           for fee in CHANNELS.values())
            print(row)

    print("\nHighest landed cost per unit that still gives the target profit")
    head = f"{'retail price':>12s}" + "".join(f" {c[:22]:>23s}" for c in CHANNELS)
    print(head)
    print("-" * len(head))
    for p in targets:
        print(f"{p:12.2f}" + "".join(
            f" {(p * (1 - pct) - fixed) / (1 + MARKUP):23.2f}"
            for pct, fixed in CHANNELS.values()))


def main():
    table("1.54in e-ink image tag", MODULES, COSTS, TARGET_PRICES)
    table("Screenless tap-to-share tag", TAP_MODULES, TAP_COSTS,
          TAP_TARGET_PRICES)


if __name__ == "__main__":
    main()
