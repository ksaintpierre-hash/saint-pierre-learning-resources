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
};

import { siteContent } from '../server/editor';
export async function generateMetadata():Promise<Metadata>{const site=await siteContent();return {...baseMetadata,title:site.seoTitle||baseMetadata.title,description:site.seoDescription||baseMetadata.description};}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{PREVIEW_MODE&&<div role="status" style={{background:"#fff0b5",color:"#163249",padding:"14px",textAlign:"center",fontSize:"16px"}}>Private staging preview — payments, sign-in, and messages are disabled.</div>}{children}</body>
    </html>
  );
}
