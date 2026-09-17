import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/owner',
          '/editor',
          '/api/',
          '/purchases',
          '/account',
          '/cart',
          '/order-confirmation',
        ],
      },
    ],
    sitemap: 'https://saintpierreresources.com/sitemap.xml',
  };
}
