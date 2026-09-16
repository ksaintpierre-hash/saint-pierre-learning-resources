CREATE TABLE IF NOT EXISTS store_products(id TEXT PRIMARY KEY,title TEXT NOT NULL,price_cents INTEGER NOT NULL CHECK(price_cents>0),approved INTEGER NOT NULL DEFAULT 0,metadata TEXT NOT NULL,storage_key TEXT NOT NULL,ready INTEGER NOT NULL DEFAULT 0);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS store_orders(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,email TEXT NOT NULL,mode TEXT NOT NULL,request_key TEXT NOT NULL,paypal_id TEXT UNIQUE,capture_id TEXT UNIQUE,total_cents INTEGER NOT NULL,currency TEXT NOT NULL DEFAULT 'USD',status TEXT NOT NULL DEFAULT 'created',fulfillment TEXT NOT NULL DEFAULT 'waiting',created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,paid_at TEXT,lock_until INTEGER NOT NULL DEFAULT 0,UNIQUE(user_id,mode,request_key));
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS store_order_items(order_id TEXT NOT NULL,product_id TEXT NOT NULL,title TEXT NOT NULL,amount_cents INTEGER NOT NULL,PRIMARY KEY(order_id,product_id));
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS store_webhooks(id TEXT PRIMARY KEY,mode TEXT NOT NULL,event_type TEXT NOT NULL,resource_id TEXT,event_time TEXT,received_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,processed INTEGER NOT NULL DEFAULT 0);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS store_download_tokens(token_hash TEXT PRIMARY KEY,user_id TEXT NOT NULL,order_id TEXT NOT NULL,product_id TEXT NOT NULL,expires_at INTEGER NOT NULL,used_at TEXT);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS store_downloads(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,order_id TEXT NOT NULL,product_id TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS store_refunds(id TEXT PRIMARY KEY,order_id TEXT NOT NULL,amount_cents INTEGER NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS store_orders_customer ON store_orders(user_id,mode,created_at);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS store_downloads_customer ON store_downloads(user_id,created_at);
