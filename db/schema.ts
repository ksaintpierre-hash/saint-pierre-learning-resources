import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";
import { sql } from "drizzle-orm";

const createdAt = () => text("created_at").notNull().default(sql`CURRENT_TIMESTAMP`);

export const profiles = sqliteTable("profiles", {
  userId: text("user_id").primaryKey(),
  email: text("email").notNull(),
  displayName: text("display_name"),
  createdAt: createdAt(),
});

export const followers = sqliteTable("followers", {
  userId: text("user_id").primaryKey(),
  email: text("email").notNull(),
  active: integer("active", { mode: "boolean" }).notNull().default(true),
  createdAt: createdAt(),
});

export const supportTickets = sqliteTable("support_tickets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id").notNull(),
  email: text("email").notNull(),
  subject: text("subject").notNull(),
  message: text("message").notNull(),
  status: text("status").notNull().default("open"),
  ownerReply: text("owner_reply"),
  createdAt: createdAt(),
  updatedAt: text("updated_at").notNull().default(sql`CURRENT_TIMESTAMP`),
});

export const resourceRequests = sqliteTable("resource_requests", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id").notNull(),
  email: text("email").notNull(),
  grade: text("grade").notNull(),
  subject: text("subject").notNull(),
  state: text("state"),
  details: text("details").notNull(),
  status: text("status").notNull().default("requested"),
  createdAt: createdAt(),
});

export const reviews = sqliteTable("reviews", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id").notNull(),
  email: text("email").notNull(),
  displayName: text("display_name").notNull(),
  productSlug: text("product_slug").notNull(),
  rating: integer("rating").notNull(),
  body: text("body").notNull(),
  status: text("status").notNull().default("pending"),
  ownerReply: text("owner_reply"),
  createdAt: createdAt(),
});

export const events = sqliteTable("events", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id"),
  eventType: text("event_type").notNull(),
  path: text("path").notNull(),
  productSlug: text("product_slug"),
  createdAt: createdAt(),
});

export const orders = sqliteTable("orders", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id"),
  customerEmail: text("customer_email").notNull(),
  providerOrderId: text("provider_order_id").notNull().unique(),
  productSlug: text("product_slug").notNull(),
  amountCents: integer("amount_cents").notNull(),
  status: text("status").notNull(),
  createdAt: createdAt(),
});

export const editorDocuments = sqliteTable("editor_documents", {
  id: text("id").primaryKey(),
  draft: text("draft").notNull(),
  live: text("live"),
  previous: text("previous"),
  revision: integer("revision").notNull().default(1),
  publishedRevision: integer("published_revision").notNull().default(0),
  updatedAt: text("updated_at").notNull(),
});
export const editorFiles = sqliteTable("editor_files", {
  id: text("id").primaryKey(), productId: text("product_id").notNull(),
  kind: text("kind").notNull(), storageKey: text("storage_key").notNull(),
  name: text("name").notNull(), contentType: text("content_type").notNull(),
  bytes: integer("bytes").notNull(), createdAt: text("created_at").notNull(),
});
