import {ChevronDown} from 'lucide-react';
import dailyHub from '../../data/daily-hub.json';
const todayLabel=new Date().toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'}).toUpperCase();
export default function DailyLearningHub(){return <section className="faq-section" id="daily"><p className="eyebrow">DAILY LEARNING HUB · {todayLabel}</p><h2>Make learning visible</h2>
 {dailyHub.items.map((item,i)=><details key={i} open={i===0}>
   <summary>{item.summary}<ChevronDown/></summary>
   {item.body.split('\n\n').map((para,j)=><p key={j}>{para}{item.linkUrl&&j===0&&<> <a href={item.linkUrl} target="_blank" rel="noreferrer">{item.linkText}</a></>}</p>)}
 </details>)}
 </section>}
