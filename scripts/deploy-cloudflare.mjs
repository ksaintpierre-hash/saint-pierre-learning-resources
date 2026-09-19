#!/usr/bin/env node
// Standalone Cloudflare Workers deployment, independent of the OpenAI "Sites"
// platform this project was originally hosted through. Builds the app, then
// patches the build's auto-generated wrangler config with this project's real
// Worker name, D1 database, and R2 bucket before deploying.
//
// Requires (all set as environment variables, never hardcoded here):
//   CLOUDFLARE_API_TOKEN   - a scoped token (Workers Scripts:Edit, D1:Edit, R2:Edit)
//   CF_WORKER_NAME         - the Worker's name, e.g. "saint-pierre-learning-resources"
//   CF_D1_DATABASE_ID      - from `wrangler d1 create <name>` (prints the id)
//   CF_D1_DATABASE_NAME    - the D1 database's name
//   CF_R2_BUCKET_NAME      - from `wrangler r2 bucket create <name>`
//
// One-time setup (run these yourself, or hand this script the resulting ids):
//   wrangler login
//   wrangler d1 create saint-pierre-learning-resources-db
//   wrangler r2 bucket create saint-pierre-learning-resources-files
//   # then apply the schema migrations to the new database:
//   wrangler d1 execute <db-name> --remote --file=drizzle/0000_lean_leader.sql
//   wrangler d1 execute <db-name> --remote --file=drizzle/0001_secure_checkout.sql
//   wrangler d1 execute <db-name> --remote --file=drizzle/0002_clumsy_warlock.sql
//
// Usage:
//   CLOUDFLARE_API_TOKEN=... CF_WORKER_NAME=... CF_D1_DATABASE_ID=... \
//     CF_D1_DATABASE_NAME=... CF_R2_BUCKET_NAME=... node scripts/deploy-cloudflare.mjs

import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const required = ['CLOUDFLARE_API_TOKEN', 'CF_WORKER_NAME', 'CF_D1_DATABASE_ID', 'CF_D1_DATABASE_NAME', 'CF_R2_BUCKET_NAME'];
const missing = required.filter((k) => !process.env[k]);
if (missing.length) {
  console.error('Missing required environment variables: ' + missing.join(', '));
  console.error('See the comment block at the top of this script for what each one is and how to get it.');
  process.exit(1);
}

function run(cmd, args) {
  console.log('$ ' + cmd + ' ' + args.join(' '));
  const result = spawnSync(cmd, args, { stdio: 'inherit', env: process.env });
  if (result.status !== 0) process.exit(result.status ?? 1);
}

console.log('Building production bundle...');
run('pnpm', ['build']);

const configPath = 'dist/server/wrangler.json';
const config = JSON.parse(readFileSync(configPath, 'utf8'));
config.name = process.env.CF_WORKER_NAME;
config.topLevelName = process.env.CF_WORKER_NAME;
config.d1_databases = [{ binding: 'DB', database_name: process.env.CF_D1_DATABASE_NAME, database_id: process.env.CF_D1_DATABASE_ID }];
config.r2_buckets = [{ binding: 'PAID_FILES', bucket_name: process.env.CF_R2_BUCKET_NAME }];
writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log('Patched ' + configPath + ' with real Worker name and resource ids.');

console.log('Deploying to Cloudflare Workers...');
run('npx', ['wrangler', 'deploy', '--config', configPath]);
console.log('Deployed. Point saintpierreresources.com\'s DNS at this Worker (Cloudflare custom domain) if you have not already.');
