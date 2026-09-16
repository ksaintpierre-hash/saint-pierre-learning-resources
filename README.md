# Saint Pierre Learning Resources

Private source archive and staging workflow for https://saintpierreresources.com.

## Preserved store

The September 16, 2026 snapshot includes the existing design, routes, homepage, navigation, owner/editor dashboard, accounts, cart, checkout and protected download implementation. `snapshots/` contains the current 133-product catalog and homepage configuration. `product-files/` contains all 133 current customer downloads with byte counts and SHA-256 checksums in `snapshots/product-files-manifest.json`.

`resources/`, `private-downloads/`, `data/`, and `server/` preserve the original products, covers, presentations, draft materials and product ideas. `output/` and `tmp/` preserve existing visual QA artifacts. Six novel-workbook ideas remain ideas with no completed delivery files; this archive does not represent those as finished products.

Customer records, passwords, live database contents, payment credentials and hosted secrets are deliberately excluded. Database schemas and migrations are included. Future dashboard edits and uploads require a fresh snapshot; GitHub does not automatically synchronize the live database or storage.

## Safe preview

Use Node.js 24 and pnpm 11.25.0:

```sh
pnpm install --frozen-lockfile
pnpm check:secrets
pnpm verify:inventory
pnpm test:store
pnpm preview:safe
```

Open http://127.0.0.1:4175. The preview uses a fresh local database seeded from the catalog snapshot. Payments, authentication and mutations are disabled. Do not add production credentials to a preview. `pnpm preview:build` only builds the review artifact.

GitHub Actions checks the main/staging branches and pull requests, then retains a private preview artifact for seven days. It never deploys the live site. Review changes on a branch and inspect the preview before merging or publishing. See [deployment instructions](docs/DEPLOYMENT.md).

## Provenance

Copied from the current Sites working project, based on commit `7607e4bb2b0a6e6d18b7107afba2f0a4eefedad8` (live version 31), including the pending fix that preserves editor-uploaded file pointers and prices during catalog initialization. This repository also adds isolated staging controls, portable test dependencies, inventories and documentation. Those additions are not automatically published to the live website. The original source folder and live store were not replaced.

Original framework documentation is retained in [STARTER-README.md](docs/STARTER-README.md).
