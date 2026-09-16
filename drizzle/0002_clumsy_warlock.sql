CREATE TABLE `editor_documents` (
	`id` text PRIMARY KEY NOT NULL,
	`draft` text NOT NULL,
	`live` text,
	`previous` text,
	`revision` integer DEFAULT 1 NOT NULL,
	`published_revision` integer DEFAULT 0 NOT NULL,
	`updated_at` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `editor_files` (
	`id` text PRIMARY KEY NOT NULL,
	`product_id` text NOT NULL,
	`kind` text NOT NULL,
	`storage_key` text NOT NULL,
	`name` text NOT NULL,
	`content_type` text NOT NULL,
	`bytes` integer NOT NULL,
	`created_at` text NOT NULL
);
