# Screenless tap-to-share NFC tag: specs and pricing

A plain passive NFC tag in a thin printed puck that sticks or snaps onto the
back of a phone. Someone taps their phone on it and gets a link: a contact
page, Instagram, a menu, Wi-Fi details. It has no battery and no screen; the
reading phone powers the chip for the moment of the tap.

Prices are USD from public listings in November 2026. Run
`python3 pricing/calc.py` after changing any number.

## Chip options

| Chip | User memory | What fits | NFC type | Price (30 mm anti-metal) |
|---|---|---|---|---|
| NTAG213 | 144 bytes | One URL up to about 130 characters | Forum Type 2 | $0.48 at 100 pcs |
| NTAG215 | 504 bytes | Long URL, short vCard (name, phone, email) | Forum Type 2 | $0.82-0.85 |
| NTAG216 | 888 bytes | Fuller vCard, no photo | Forum Type 2 | $0.98-1.39 |
| NTAG424 DNA | 416 bytes (vendor figure) | URL that changes on every tap, so the tag can't be copied | Forum Type 4 | $1.25 at 10 pcs, $0.99 at 500 |

Common to all: 13.56 MHz, ISO/IEC 14443-A, no battery, rewritable until you
lock it. NTAG21x can also be write-protected with a password. NXP rates the
NTAG213F/216F for 10 years data retention and 100,000 write cycles at 22 °C
(datasheet Rev. 3.6, Table 31); the plain NTAG213/215/216 is expected to match
but its datasheet hasn't been checked here. Read distance with a phone
is about 1-4 cm and depends on the reading phone.

**My recommendation: NTAG213 holding a URL to a profile page you host.** The
customer edits the page, not the tag. It reads on both iPhone and Android with
no app, and it is the cheapest chip. A vCard written straight onto the tag is
handled inconsistently on iPhone.

## The tag must be "anti-metal"

A normal sticker on a phone back does not work, because the battery and metal
frame kill the signal. Buy tags with a ferrite layer (sold as "anti-metal" or
"on-metal"), and fit them ferrite side towards the phone. The ferrite also
mostly stops the owner's own phone from reading its tag. Test that on the
phones you sell for.

## Finished product dimensions

Build D in `cases/`. Diameter x thickness in mm; weight is an estimate.

| Version | Tag | Size | Weight |
|---|---|---|---|
| Adhesive puck | 25 mm | 29.1 x 1.7 | ~1.5 g |
| Adhesive puck | 30 mm | 34.1 x 1.7 | ~1.5 g |
| Magnet puck (MagSafe ring) | 30 mm | 58.0 x 2.7 | ~9 g |

There is 0.6 mm of plastic over the antenna. Make it thicker and the read
range drops. Tag thickness is set to 1.0 mm (`TapTag.tag_t`); measure your
tags and change it.

## Cost and price for 2x profit (200% markup)

The same assumptions as the e-ink sheet apply: 20% import VAT you can't
reclaim, 5% spoilage, labour not included, postage charged to the buyer.

| Chip | Cost per unit (adhesive / magnet) | In person | Own shop | Etsy |
|---|---|---|---|---|
| NTAG213 | $1.48 / $1.95 | $4.43 / $5.85 | $4.88 / $6.34 | $5.39 / $6.96 |
| NTAG215 | $1.94 / $2.42 | $5.83 / $7.25 | $6.32 / $7.78 | $6.94 / $8.50 |
| NTAG216 | $2.11 / $2.58 | $6.32 / $7.74 | $6.82 / $8.28 | $7.48 / $9.05 |
| NTAG424 DNA | $2.45 / $2.92 | $7.34 / $8.76 | $7.88 / $9.34 | $8.61 / $10.17 |

These are minimums. Reaching 2x profit is easy here; the risk runs the other
way. A pack of 20 blank 25 mm stickers sells for about $7, so the product has
to be more than the chip: the puck design, programming it for the customer,
and the profile page.

| Retail price | Highest cost per unit, in person | Own shop | Etsy |
|---|---|---|---|
| $5 | $1.67 | $1.52 | $1.36 |
| $8 | $2.67 | $2.49 | $2.26 |
| $10 | $3.33 | $3.13 | $2.87 |
| $15 | $5.00 | $4.75 | $4.38 |
| $20 | $6.67 | $6.37 | $5.88 |

## Pricing options

1. **Low price, about $8-10.** Easy to sell in person or in bundles. Etsy
   postage will often cost more than the tag.
2. **Programmed and personalised, about $15-20.** You write the customer's
   link and lock the tag. The puck carries their colour or initials. The profit
   is several times the 2x target.
3. **Tag plus a hosted profile page, as a subscription.** The most profit
   over time, but you run a website and keep it online. It is also what the
   established brands sell, so you compete with them directly.

## Before selling

- A tag over the phone's own NFC antenna can interfere with contactless
  payments. Place it low on the back. On iPhone the antenna is at the top edge.
- Locked tags can't be changed later. Offer locking, don't do it by default,
  unless the link points to a page you control.
- A URL you host must stay online for as long as the tags are in use.

## Actual tag dimensions

Vendors don't agree on thickness and rarely say whether "30 mm" is the
sticker or the antenna. Measure a sample before printing.

| Tag | Outer size | Antenna | Thickness | Source |
|---|---|---|---|---|
| Anti-metal sticker, 25 mm | 25 mm round | - | 0.3 mm (total, "ultra-thin") | Amazon listing |
| Anti-metal sticker, 30 mm (ZipNFC) | 30 mm round | 25 mm | ferrite layer alone 0.2 mm; total not stated | ZipNFC |
| On-metal PVC disc, 30 mm (Seritag) | 30 mm round | - | 1.0 mm | Seritag |
| NFC business card (ISO ID-1, credit-card size) | 85.60 x 53.98 mm | - | 0.76 mm standard, 0.84 mm common for PVC NFC cards | ISO/IEC 7810 (from memory) |

Build D defaults to a 1.0 mm pocket. For 0.3 mm stickers set
`TapTag.tag_t = 0.3` and re-run, or the tag sits loose under the pad.

## Images, PDFs and company cards

No NFC tag holds a usable image or PDF.

| Chip | Memory | Holds |
|---|---|---|
| NTAG213 / 215 / 216 | 144 / 504 / 888 bytes | Link, or a short contact card |
| MIFARE DESFire EV3 8K (card) | 8 KB | Thumbnail-size JPEG at best, ~$1.80-3.35 per card |
| ST25DV64K (chip, needs your own antenna board) | 8 KB | Same, ~$0.85 per chip |

A phone photo is 2-5 MB, about 500 times more than the largest tag. Phones
also don't show an image or PDF stored on a tag when tapped. iPhone background
reading only opens a web link.

What works:
1. **Link to a hosted page, image or PDF.** Any NTAG213 is enough. It works
   on every phone, and you can change the content without touching the tag.
   This is how every "digital business card" product works.
2. **Credit-card-size NFC business card** with a printed logo, holding that
   same link. That is the "company card" format.
3. **An e-ink NFC tag** if the image has to be visible without a phone (the
   1.54" modules in `pricing/README.md`).
4. **Contact card stored on the tag itself** (NTAG216, no photo). It works
   offline, but iPhones handle it inconsistently.

## Chip package dimensions: NTAG213F / NTAG216F

Source: NXP NTAG213F/216F product data sheet, Rev. 3.6 (28 Sep 2015),
Fig 23, package outline SOT1312AB2 (HXSON4), page 48.

This is the packaged chip you solder onto your own antenna PCB. It is the
"F" (field-detect) variant: NTAG213F = 144 bytes, NTAG216F = 888 bytes, and
there is no NTAG215F. Ready-made stickers use the plain NTAG213/215/216 as a
bare die bonded straight onto the antenna, which this datasheet doesn't cover.

Order codes: NT2H1311F0DTL (NTAG213F), NT2H1611F0DTL (NTAG216F).

| Dimension | Symbol | Min | Nom | Max (mm) |
|---|---|---|---|---|
| Body length | E | 1.90 | 2.00 | 2.10 |
| Body width | D | 1.40 | 1.50 | 1.60 |
| Height | A | 0.47 | 0.49 | 0.50 |
| Standoff | A1 | 0.00 | - | 0.05 |
| Terminal thickness | A3 | 0.050 | - | 0.152 |
| Terminal width | b | 0.20 | 0.25 | 0.30 |
| Terminal length | L | 0.30 | 0.35 | 0.40 |
| Terminal pitch | e | - | 0.5 | - |
| Exposed pad length | Eh | 0.75 | 0.80 | 0.85 |
| Exposed pad width | Dh | 0.95 | 1.00 | 1.05 |
| Pad to terminal gap | K | 0.20 | - | - |

Note 1 of the drawing: plastic or metal protrusions of up to 0.075 mm per side
are not included.

Pins: 1 GND, 2 LB (antenna), 3 FD (field detect), 4 LA (antenna). NXP
recommends leaving the central pad floating. Input capacitance 50 pF.
Operating distance "up to 100 mm" depending on the antenna and reader; a
phone reading a 25-30 mm antenna gets a few centimetres.
