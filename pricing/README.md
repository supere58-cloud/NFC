# Product specs and pricing: NFC e-ink image tag

The product: a battery-free 1.54" colour e-ink tag in a printed case that
sticks or snaps magnetically onto a phone. The owner writes a photo to it from
a phone app over NFC; the image stays with no power.

Prices are USD, from public listings in November 2026. Re-check them before
ordering. Change any number in `calc.py` and run it again:

```bash
python3 pricing/calc.py
```

## Display (same for every option)

| Spec | Value |
|---|---|
| Size | 1.54" diagonal |
| Resolution | 200 x 200 px |
| Active (visible) area | 27.0 x 27.0 mm |
| Colours | Black, white, red, yellow |
| Power | None stored; harvested from the phone's NFC field |
| Refresh | about 15 s, phone held still |
| Phones | NFC-capable iPhone and Android; check each vendor's list, some Samsung and Google models are unsupported on Waveshare's sibling model |

## Finished product dimensions

Width x height x thickness in mm. Weights are estimates (PETG case + module +
magnets).

| Module | Case | Adhesive version | Magnet version | Est. weight |
|---|---|---|---|---|
| Good Display tag (DMPL0154FN1 / GDP0154NF2), 36.59 x 47.09 x 3.0 | Build C | 39.8 x 50.3 x 4.8 | 53.8 x 50.3 x 4.8 | 11-15 g |
| Bare module (Shellrus, or own build) | Build A | 35.5 x 42.8 x 4.3 | 49.5 x 42.8 x 4.3 | 8-11 g |
| Waveshare (G), 41.28 x 47.84 | Build B | 44.5 x 51.0 x 6.3 | 58.5 x 51.0 x 6.3 | 22-27 g |
| AliExpress keychain | none yet | measure first | measure first | - |

## Cost and selling price

Assumptions behind every row:

- **Target.** Profit is 2x the landed cost, after channel fees. That is a 200%
  markup, so the price is about 3x the cost and the gross margin is 66.7%.
- **Landed cost.** Module plus inbound shipping, with 20% import VAT you can't
  reclaim. Add the printed case, mount hardware and packaging ($1.30-1.55),
  then 5% for spoilage.
- **Not included.** Your labour (the profit pays for it) and outbound postage
  (charged to the buyer).

| Module | Landed cost | Price, in person | Price, own shop | Price, Etsy |
|---|---|---|---|---|
| AliExpress keychain ($10.91) | $15.1-15.4 | $45-46 | $47-48 | $51 |
| Own build: panel ($5.85) + own NFC board (~$5, estimate) | $16.3-16.6 | $49-50 | $51-52 | $55 |
| Good Display DMPL0154FN1 ($13.96) | $22.1-22.4 | $66-67 | $69 | $74-75 |
| Good Display GDP0154NF2 ($17.76) | $26.9-27.2 | $81 | $83-84 | $90-91 |
| Shellrus bare module ($25.00) | $35.4-35.7 | $106-107 | $110-111 | $118-119 |
| Waveshare (G) ($26.63) | $37.4-37.7 | $112-113 | $116-117 | $125 |

## The other direction: what a market price allows

Finished 1.54" NFC e-ink tags already sell for about $11-44 on AliExpress, and
Shellrus sells its designed tags at about $29.

| Retail price | Highest cost per unit, in person | Own shop | Etsy |
|---|---|---|---|
| $29 | $9.67 | $9.28 | $8.60 |
| $39 | $13.00 | $12.51 | $11.62 |
| $49 | $16.33 | $15.74 | $14.63 |
| $59 | $19.67 | $18.98 | $17.65 |
| $69 | $23.00 | $22.21 | $20.66 |

At $29, the target needs a landed cost under about $9, below the cheapest
ready-made module once import VAT is paid.

## Ways to get there

1. **Cheapest ready-made tag, priced at about $45-50.** Lowest effort. The
   price is above most finished tags, so the case design, personalisation and
   gift packaging have to carry it. You also need to test the AliExpress tag's
   quality before relying on it.
2. **Good Display tag at a volume price.** Ask Good Display for a 50-100 pcs
   quote. A module near $8-9 brings the price to about $39. The quote is
   unknown until you ask.
3. **Own NFC driver board plus the $5.85 bare panel.** This route has the
   lowest cost at volume (about $49 now, lower with a cheaper board). It means
   designing and testing a PCB, so it takes weeks, and the ~$5 board figure is
   my estimate, not a quote.
4. **Accept a lower markup.** At 100% markup (2x cost) the Good Display tag
   sells for about $44-49, which competes directly.

## Before you sell

- Phone fit and NFC: a tag left over the phone's NFC antenna can block
  contactless payments. Say so in the listing.
- Decorative shells shaped like a Game Boy, a Polaroid camera or the Windows
  interface use other companies' trademarks and trade dress. Your own shapes
  avoid that risk.
- If you sell in the EU you take on product-safety and labelling duties (CE /
  GPSR, small magnets warnings). Check them before the first sale.
