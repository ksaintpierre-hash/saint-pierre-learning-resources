"use client";
import { useEffect } from "react";
export default function VisitTracker({productId}:{productId?:string}){
  useEffect(()=>{fetch("/api/track",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({eventType:productId?'product_view':'page_view',path:location.pathname,productSlug:productId})}).catch(()=>{});},[productId]);
  return null;
}
