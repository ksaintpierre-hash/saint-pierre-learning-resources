ALTER TABLE `students` ADD `aig_identified` integer DEFAULT false NOT NULL;--> statement-breakpoint
ALTER TABLE `students` ADD `has_504_plan` integer DEFAULT false NOT NULL;--> statement-breakpoint
ALTER TABLE `students` ADD `has_ec_iep` integer DEFAULT false NOT NULL;--> statement-breakpoint
ALTER TABLE `students` ADD `extended_time` integer DEFAULT false NOT NULL;--> statement-breakpoint
ALTER TABLE `students` ADD `accommodation_notes` text DEFAULT '' NOT NULL;