# Vendors and substitutions

Notes on where parts come from and what to do when a line in `bom.csv` goes stale.

Rules (from the charter):

- Every line in `bom.csv` lists two vendors, or a note explaining why only one exists and what the fallback is.
- The `generic_spec` column is the real identity of the part. Vendor part numbers are conveniences that will rot.
- Prefer industrial suppliers and appliance repair-parts houses over marketplaces. Marketplace links are a third source only.
- Every line carries a `last_verified` date. Older than 12 months means unverified.
- Costs are indicative, dated, and in USD for this BOM.

## Which BOM file is which

- `bom.csv`: the chassis and the common power module. Everything every build needs.
- `bom-tiers.csv`: which lines belong to which control tier.
- `heat-electric-240.csv`, `heat-gas.csv`, `heat-heatpump.csv`: one file per heat module, as the charter asks (one BOM per optional module). The no-heat build has no file of its own; its blanking duct is a line in `bom.csv` marked "fit when no heat module is installed".
- Lines in `bom.csv` that belong to the heat-enable chain carry the note "omit only if a heat module will never be fitted".

## Sources used so far

(none yet)

## Known substitutions

(none yet)
