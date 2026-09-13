/* Minimal dependency-free SVG charts. Warm palette. */
const PAL = {wheat:'#b08d2f',sage:'#7c8b6e',terra:'#b25a3c',slate:'#5f7a86',plum:'#8a5f7a',ink:'#6b6355',line:'#e4dccd',grid:'#ece5d4'};
const PALETTE=[PAL.wheat,PAL.sage,PAL.terra,PAL.slate,PAL.plum,'#97753f','#6d8577','#a06a4f'];
function svgEl(tag,attrs){const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const k in attrs)e.setAttribute(k,attrs[k]);return e;}
function mount(id,svg){const el=document.getElementById(id);if(el){el.innerHTML='';el.appendChild(svg);}}
function niceTicks(min,max,n=5){const span=max-min||1;const step=Math.pow(10,Math.floor(Math.log10(span/n)))*[1,2,5,10].find(m=>span/(Math.pow(10,Math.floor(Math.log10(span/n)))*m)<=n)||1;const lo=Math.floor(min/step)*step,hi=Math.ceil(max/step)*step;const t=[];for(let v=lo;v<=hi+1e-9;v+=step)t.push(+v.toFixed(6));return t;}

function barChart(id,labels,values,{horizontal=false,color=PAL.wheat,xlabel='',w=560,h=300}={}){
  const svg=svgEl('svg',{viewBox:`0 0 ${w} ${h}`,width:'100%'});
  const m={t:14,r:14,b:38,l:horizontal?150:44},iw=w-m.l-m.r,ih=h-m.t-m.b;
  const max=Math.max(...values)*1.08;
  const g=svgEl('g',{});svg.appendChild(g);
  if(!horizontal){
    niceTicks(0,max).forEach(t=>{const y=m.t+ih-(t/max)*ih;
      g.appendChild(svgEl('line',{x1:m.l,y1:y,x2:w-m.r,y2:y,stroke:PAL.grid}));
      const tx=svgEl('text',{x:m.l-6,y:y+3,'text-anchor':'end'});tx.textContent=t;g.appendChild(tx);});
    const bw=iw/labels.length;
    labels.forEach((lb,i)=>{const bh=(values[i]/max)*ih;
      g.appendChild(svgEl('rect',{x:m.l+i*bw+bw*0.12,y:m.t+ih-bh,width:bw*0.76,height:bh,fill:Array.isArray(color)?color[i]:color,rx:3}));
      const tx=svgEl('text',{x:m.l+i*bw+bw/2,y:h-24,'text-anchor':labels.length>12?'end':'middle',
        transform:labels.length>12?`rotate(-45 ${m.l+i*bw+bw/2} ${h-24})`:''});tx.textContent=lb;g.appendChild(tx);
      const vt=svgEl('text',{x:m.l+i*bw+bw/2,y:m.t+ih-bh-4,'text-anchor':'middle','font-weight':'600'});vt.textContent=values[i];g.appendChild(vt);});
  }else{
    const bh=ih/labels.length;
    labels.forEach((lb,i)=>{const bwv=(values[i]/max)*iw;
      g.appendChild(svgEl('rect',{x:m.l,y:m.t+i*bh+bh*0.14,width:bwv,height:bh*0.72,fill:Array.isArray(color)?color[i]:color,rx:3}));
      const tx=svgEl('text',{x:m.l-6,y:m.t+i*bh+bh/2+4,'text-anchor':'end'});tx.textContent=lb;g.appendChild(tx);
      const vt=svgEl('text',{x:m.l+bwv+5,y:m.t+i*bh+bh/2+4});vt.textContent=values[i];g.appendChild(vt);});
  }
  if(xlabel){const tx=svgEl('text',{x:m.l+iw/2,y:h-6,'text-anchor':'middle'});tx.textContent=xlabel;g.appendChild(tx);}
  mount(id,svg);
}

function lineChart(id,series,{xlabel='',ylabel='',w=640,h=320,fill=false}={}){
  // series: [{name, pts:[[x,y],...], color}]
  const svg=svgEl('svg',{viewBox:`0 0 ${w} ${h}`,width:'100%'});
  const m={t:16,r:16,b:36,l:52},iw=w-m.l-m.r,ih=h-m.t-m.b;
  const allx=series.flatMap(s=>s.pts.map(p=>p[0])),ally=series.flatMap(s=>s.pts.map(p=>p[1]));
  const x0=Math.min(...allx),x1=Math.max(...allx),y1=Math.max(...ally)*1.06;
  const X=v=>m.l+((v-x0)/(x1-x0))*iw, Y=v=>m.t+ih-(v/y1)*ih;
  const g=svgEl('g',{});svg.appendChild(g);
  niceTicks(x0,x1,8).forEach(t=>{g.appendChild(svgEl('line',{x1:X(t),y1:m.t,x2:X(t),y2:m.t+ih,stroke:PAL.grid}));
    const tx=svgEl('text',{x:X(t),y:h-20,'text-anchor':'middle'});tx.textContent=t;g.appendChild(tx);});
  niceTicks(0,y1).forEach(t=>{g.appendChild(svgEl('line',{x1:m.l,y1:Y(t),x2:w-m.r,y2:Y(t),stroke:PAL.grid}));
    const tx=svgEl('text',{x:m.l-6,y:Y(t)+3,'text-anchor':'end'});tx.textContent=t;g.appendChild(tx);});
  series.forEach((s,si)=>{
    const d=s.pts.map((p,i)=>(i?'L':'M')+X(p[0]).toFixed(1)+' '+Y(p[1]).toFixed(1)).join(' ');
    if(fill){const area=d+`L${X(s.pts[s.pts.length-1][0])} ${Y(0)}L${X(s.pts[0][0])} ${Y(0)}Z`;
      g.appendChild(svgEl('path',{d:area,fill:s.color,opacity:0.15}));}
    g.appendChild(svgEl('path',{d,fill:'none',stroke:s.color,'stroke-width':2.2}));
    const lg=svgEl('text',{x:w-m.r-150,y:16+si*15});lg.textContent=s.name;g.appendChild(lg);
    g.appendChild(svgEl('rect',{x:w-m.r-165,y:8+si*15,width:10,height:3,fill:s.color}));});
  if(xlabel){const tx=svgEl('text',{x:m.l+iw/2,y:h-4,'text-anchor':'middle'});tx.textContent=xlabel;g.appendChild(tx);}
  if(ylabel){const tx=svgEl('text',{x:12,y:m.t+ih/2,'text-anchor':'middle',transform:`rotate(-90 12 ${m.t+ih/2})`});tx.textContent=ylabel;g.appendChild(tx);}
  mount(id,svg);
}

function scatterChart(id,pts,{xlabel='',ylabel='',w=640,h=380,colorFn=null,labelTop=0,labelFn=null}={}){
  // pts: [{x,y,...}]
  const svg=svgEl('svg',{viewBox:`0 0 ${w} ${h}`,width:'100%'});
  const m={t:16,r:16,b:38,l:56},iw=w-m.l-m.r,ih=h-m.t-m.b;
  const xs=pts.map(p=>p.x),ys=pts.map(p=>p.y);
  const x0=Math.min(...xs)-1,x1=Math.max(...xs)+1,y1=Math.max(...ys)*1.08;
  const X=v=>m.l+((v-x0)/(x1-x0))*iw, Y=v=>m.t+ih-(v/y1)*ih;
  const g=svgEl('g',{});svg.appendChild(g);
  niceTicks(x0,x1,8).forEach(t=>{g.appendChild(svgEl('line',{x1:X(t),y1:m.t,x2:X(t),y2:m.t+ih,stroke:PAL.grid}));
    const tx=svgEl('text',{x:X(t),y:h-22,'text-anchor':'middle'});tx.textContent=t;g.appendChild(tx);});
  niceTicks(0,y1).forEach(t=>{g.appendChild(svgEl('line',{x1:m.l,y1:Y(t),x2:w-m.r,y2:Y(t),stroke:PAL.grid}));
    const tx=svgEl('text',{x:m.l-6,y:Y(t)+3,'text-anchor':'end'});tx.textContent=t;g.appendChild(tx);});
  pts.forEach(p=>{g.appendChild(svgEl('circle',{cx:X(p.x),cy:Y(p.y),r:4.2,fill:colorFn?colorFn(p):PAL.wheat,opacity:0.75}));
    if(p.x||p.y){const t=svgEl('title',{});t.textContent=(p.name||'')+' ('+p.x+', '+p.y+')';g.lastChild.appendChild(t);}});
  if(labelTop&&labelFn){[...pts].sort((a,b)=>b.y-a.y).slice(0,labelTop).forEach(p=>{
    const tx=svgEl('text',{x:X(p.x)+7,y:Y(p.y)+3,'font-size':'10px'});tx.textContent=labelFn(p);g.appendChild(tx);});}
  const tx=svgEl('text',{x:m.l+iw/2,y:h-4,'text-anchor':'middle'});tx.textContent=xlabel;g.appendChild(tx);
  const ty=svgEl('text',{x:12,y:m.t+ih/2,'text-anchor':'middle',transform:`rotate(-90 12 ${m.t+ih/2})`});ty.textContent=ylabel;g.appendChild(ty);
  mount(id,svg);
}

function donutChart(id,parts,{w=340,h=280}={}){
  // parts: [{label,value,color}]
  const svg=svgEl('svg',{viewBox:`0 0 ${w} ${h}`,width:'100%'});
  const cx=110,cy=h/2,R=78,r=48,total=parts.reduce((a,p)=>a+p.value,0);
  let a0=-Math.PI/2;
  parts.forEach((p,i)=>{const a1=a0+(p.value/total)*2*Math.PI;
    const large=a1-a0>Math.PI?1:0;
    const d=`M ${cx+r*Math.cos(a0)} ${cy+r*Math.sin(a0)} L ${cx+R*Math.cos(a0)} ${cy+R*Math.sin(a0)} A ${R} ${R} 0 ${large} 1 ${cx+R*Math.cos(a1)} ${cy+R*Math.sin(a1)} L ${cx+r*Math.cos(a1)} ${cy+r*Math.sin(a1)} A ${r} ${r} 0 ${large} 0 ${cx+r*Math.cos(a0)} ${cy+r*Math.sin(a0)} Z`;
    svg.appendChild(svgEl('path',{d,fill:p.color||PALETTE[i%PALETTE.length]}));
    const ly=26+i*20;
    svg.appendChild(svgEl('rect',{x:210,y:ly-10,width:11,height:11,rx:2,fill:p.color||PALETTE[i%PALETTE.length]}));
    const tx=svgEl('text',{x:227,y:ly});tx.textContent=`${p.label} — ${p.value}`;svg.appendChild(tx);
    a0=a1;});
  mount(id,svg);
}

function worldDots(id,pts,{w=680,h=380}={}){
  // simple equirectangular scatter with graticule; pts:[{lat,lon,name,year,size}]
  const svg=svgEl('svg',{viewBox:`0 0 ${w} ${h}`,width:'100%'});
  const m={t:18,r:12,b:26,l:36},iw=w-m.l-m.r,ih=h-m.t-m.b;
  const X=lon=>m.l+((lon+180)/360)*iw, Y=lat=>m.t+((90-lat)/180)*ih;
  const g=svgEl('g',{});svg.appendChild(g);
  for(let lon=-180;lon<=180;lon+=30)g.appendChild(svgEl('line',{x1:X(lon),y1:m.t,x2:X(lon),y2:m.t+ih,stroke:PAL.grid}));
  for(let lat=-60;lat<=90;lat+=30)g.appendChild(svgEl('line',{x1:m.l,y1:Y(lat),x2:w-m.r,y2:Y(lat),stroke:PAL.grid}));
  [-150,-120,-90,-60,-30,0,30,60,90,120,150].forEach(lon=>{const t=svgEl('text',{x:X(lon),y:h-10,'text-anchor':'middle'});t.textContent=lon+'°';g.appendChild(t);});
  [-60,-30,0,30,60].forEach(lat=>{const t=svgEl('text',{x:m.l-5,y:Y(lat)+3,'text-anchor':'end'});t.textContent=lat+'°';g.appendChild(t);});
  pts.forEach(p=>{const c=svgEl('circle',{cx:X(p.lon),cy:Y(p.lat),r:p.hot?6:3.4,fill:p.hot?PAL.terra:PAL.wheat,opacity:p.hot?0.85:0.55,stroke:'#fff','stroke-width':0.8});
    const t=svgEl('title',{});t.textContent=`${p.name} (${p.year||'?'})`;c.appendChild(t);g.appendChild(c);});
  mount(id,svg);
}
