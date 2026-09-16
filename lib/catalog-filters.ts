export type CatalogItem = {
  thumbnailSrc?: string; id: string; title: string; level: string; subject: string; standard: string;
  description: string; priceCents: number; ready: boolean; resourceType: string;
  formats: string[]; pages: number; included: string[]; minutes: string; source: string;
  collections?: string[]; grades?: string[]; states?: string[]; audience?: string;
};
const tags: Record<string, string[]> = {
  'ca-grade4-multidigit': ['Worksheets','Classwork','Independent Work','Exit Tickets'],
  'fl-grade5-theme': ['Worksheets','Classwork','Homework','Exit Tickets'],
  'tx-grade7-elements-compounds': ['Worksheets','Small-Group Work','Exit Tickets'],
  'college-composition-claims': ['College Resources','Worksheets'],
  'college-algebra-linear': ['College Resources','Worksheets','Independent Work'],
  'college-biology-membranes': ['College Resources','Worksheets'],
  'college-psych-research': ['College Resources','Worksheets'],
  'spanish101-campus': ['College Resources','World Languages'],
  'college-accounting-cycle': ['College Resources','CTE & Career'],
  'college-programming-python': ['College Resources','CTE & Career'],
};
export const collectionsFor = (p: CatalogItem): string[] => p.collections || tags[p.id] || (p.formats?.includes('PPTX') ? ['PowerPoints'] : []);
export const gradesFor = (p: CatalogItem): string[] => p.grades || [p.level.split('•')[0].trim()];
export function matchesFilters(p: CatalogItem, f: {grade: string; state: string; subject: string; collection: string; query: string}) {
  const parts = p.level.split('•').map(s=>s.trim());
  const text = [p.title,p.level,p.subject,p.standard,p.description,p.resourceType,...collectionsFor(p)].join(' ').toLowerCase();
  const aliases: Record<string,string[]> = {Math:['mathematics'],Writing:['writing','composition'],Science:['science','biology'],CTE:['business','computer science'],Spanish:['spanish']};
  return (f.grade==='All Levels'||gradesFor(p).includes(f.grade))
    && (f.state==='All States'||(p.states||parts).includes(f.state))
    && (f.subject==='All Subjects'||(aliases[f.subject]||[f.subject.toLowerCase()]).some(s=>text.includes(s)))
    && (f.collection==='All Resources'||collectionsFor(p).includes(f.collection))
    && f.query.trim().toLowerCase().split(/\s+/).every(s=>text.includes(s));
}
