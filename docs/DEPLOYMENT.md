# Preview and live publishing

## Review workflow

1. Create a feature branch from main; preserve existing products and files.
2. Make changes and open a pull request. Run inventory, secret-pattern, type, commerce/editor and preview-build checks.
3. Run `pnpm preview:safe` locally. Review desktop/mobile layouts, product descriptions, covers, navigation and cart. Preview authentication, messages, checkout and file delivery are intentionally inactive.
4. Review the diff and successful Actions checks before merging. Branch review is a documented process; no paid GitHub branch-protection feature is assumed.
5. Publish separately through the existing Sites project only after the preview is approved. GitHub pushes are backups and checks, not live publishing.

## Existing production deployment

The existing `.openai/hosting.json` identifies Sites project `appgprj_6aa5f6efc9d881919133029e9364265a`, database binding `DB` and private storage binding `PAID_FILES`. Preserve that identity and the current domain. Do not create a replacement site, reset the database or overwrite hosted credentials.

Use the Sites building/hosting tools with authenticated project access to publish the reviewed source. Unset `VITE_STORE_PREVIEW` (or set it to `false`) and build production with `pnpm build`. Save/package the exact reviewed source and deploy its version through Sites. Confirm successful deployment and verify the existing domain, catalog, account flow and protected delivery. Do not run preview seed SQL against a remote database. Existing schema migrations must be reviewed against the current production schema before applying any new migration.

Live Supabase authentication and PayPal configuration remain managed in the existing hosting/account settings. `.env.example` contains placeholders only. Never commit real environment files, passwords, private keys, tokens or service-role keys. The repository secret check is a limited pattern/filename check, not a guarantee that every possible secret format can be detected.

## Recovery and limits

Keep the previous successful Sites deployment available for rollback. This repository preserves application source, current product binaries and catalog/homepage snapshots, but does not back up customer accounts, orders or the complete live database. Obtain protected database/storage backups through the existing providers when needed. Dashboard changes after September 16, 2026 need a new source/catalog/file snapshot before this archive can restore them.
