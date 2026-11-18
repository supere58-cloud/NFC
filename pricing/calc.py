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


def landed_cost(price, ship, variant):
    module = (price + ship) * (1 + IMPORT_VAT)
    extras = sum(c[variant] for c in COSTS.values())
    return (module + extras) * (1 + WASTE)


def selling_price(cost, pct, fixed):
    """Price at which (price - fees - cost) = MARKUP * cost."""
    return ((1 + MARKUP) * cost + fixed) / (1 - pct)


def main():
    head = f"{'module':47s} {'build':26s} {'var':8s} {'cost':>7s}"
    head += "".join(f" {c[:22]:>23s}" for c in CHANNELS)
    print(head)
    print("-" * len(head))
    for name, (price, ship, build) in MODULES.items():
        for var in ("adhesive", "magnet"):
            c = landed_cost(price, ship, var)
            row = f"{name:47s} {build:26s} {var:8s} {c:7.2f}"
            row += "".join(f" {selling_price(c, *fee):23.2f}"
                           for fee in CHANNELS.values())
            print(row)

    print("\nHighest landed cost per unit that still gives the target profit")
    head = f"{'retail price':>12s}" + "".join(f" {c[:22]:>23s}" for c in CHANNELS)
    print(head)
    print("-" * len(head))
    for p in TARGET_PRICES:
        print(f"{p:12.2f}" + "".join(
            f" {(p * (1 - pct) - fixed) / (1 + MARKUP):23.2f}"
            for pct, fixed in CHANNELS.values()))


if __name__ == "__main__":
    main()
