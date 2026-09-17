import { PREVIEW_MODE } from '../lib/preview-mode';
import type { Metadata } from "next";
import "./globals.css";
import "./portal.css";
import "./category.css";
import "./auth.css";
import "./commerce.css";
import "./previews.css";
import "./powerpoint-drafts.css";
import "./launch-fixes.css";

const baseMetadata: Metadata = {
  title: "Saint Pierre Learning Resources | Printable Teaching Resources",
  description: "Explore printable education resources and sample pages from Saint Pierre Learning Resources. Find focused school and introductory college practice with clear objectives, teacher guidance, and answer keys.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
  manifest: "/manifest.json",
  openGraph: {
    title: "Saint Pierre Learning Resources | Printable Teaching Resources",
    description: "Explore printable education resources and sample pages from Saint Pierre Learning Resources. Find focused school and introductory college practice with clear objectives, teacher guidance, and answer keys.",
    url: "https://saintpierreresources.com",
    siteName: "Saint Pierre Learning Resources",
    images: [
      {
        url: "https://saintpierreresources.com/brand/saint-pierre-logo.png",
        width: 512,
        height: 512,
        alt: "Saint Pierre Learning Resources logo",
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "Saint Pierre Learning Resources | Printable Teaching Resources",
    description: "Explore printable education resources and sample pages from Saint Pierre Learning Resources.",
    images: ["https://saintpierreresources.com/brand/saint-pierre-logo.png"],
  },
};

import { siteContent } from '../server/editor';
export async function generateMetadata():Promise<Metadata>{
  const site=await siteContent();
  const title=site.seoTitle||baseMetadata.title as string;
  const description=site.seoDescription||baseMetadata.description as string;
  return {
    ...baseMetadata,
    title,
    description,
    openGraph:{...baseMetadata.openGraph as object,title,description},
    twitter:{...baseMetadata.twitter as object,title,description},
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased"><a href="#main-content" className="skip-link">Skip to main content</a>{PREVIEW_MODE&&<div role="status" style={{background:"#fff0b5",color:"#163249",padding:"14px",textAlign:"center",fontSize:"16px"}}>Private staging preview — payments, sign-in, and messages are disabled.</div>}{children}</body>
    </html>
  );
}
