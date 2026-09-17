import { publicCatalog } from '../server/commerce';
import type { MetadataRoute } from 'next';

export const dynamic = 'force-dynamic';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = 'https://saintpierreresources.com';
  const products = await publicCatalog();

  const staticPages: MetadataRoute.Sitemap = [
    { url: base, lastModified: new Date(), changeFrequency: 'daily', priority: 1.0 },
    { url: `${base}/policies`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.5 },
    { url: `${base}/support`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.4 },
    { url: `${base}/requests`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.4 },
    { url: `${base}/reviews`, lastModified: new Date(), changeFrequency: 'weekly', priority: 0.4 },
  ];

  const productPages: MetadataRoute.Sitemap = products.map(p => ({
    url: `${base}/products/${p.id}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [...staticPages, ...productPages];
}
