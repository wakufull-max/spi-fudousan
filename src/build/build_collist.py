# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX, DIAGNOSIS
IMG = json.load(open("images.json", encoding="utf-8"))
C = json.load(open("columns.json", encoding="utf-8"))
CIMG = {"東京23区":"tokyo","大阪市":"osaka","横浜市":"yokohama","福岡市":"fukuoka"}
for c in C: c["img"] = CIMG[c["city"]]
TOKYO_IMG = {"港区":"minato","千代田区":"chiyoda","渋谷区":"shibuya","目黒区":"meguro","世田谷区":"setagaya"}
for c in C:
    if c["ward"] in TOKYO_IMG and c["city"] == "東京23区": c["img"] = TOKYO_IMG[c["ward"]]

DATA = [{k: c[k] for k in ("slug","city","ward","title","lead","caution","img","areas")} for c in C]
CITIES = ["東京23区","大阪市","横浜市","福岡市"]
head = C[0]

body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>コラム</div>
<div class="wrap pg">
  <div class="eyebrow caps">Column</div>
  <h1 class="pt">エリア別 風水・地形ガイド</h1>
  <div class="pt-sub">高台・水系・街の成り立ちを読む</div>
  <p class="lead">東京23区・大阪市・横浜市・福岡市の全72区について、地形と水系、街の成り立ちを整理しました。
    形勢派風水の枠組みで読みつつ、洪水・内水・高潮・液状化の想定区域とは必ず照合しています。</p>
  <div class="stance">
    <div class="ic">土地の話</div>
    <p>ここに並ぶ記事は、生年月日や命星を使いません。誰が読んでも同じ、土地そのものの情報だけを扱います。
      あなたと土地の相性については、<a href="diagnosis.html" style="border-bottom:1px solid var(--rule)">風水診断</a>を別に用意しています。</p>
  </div>
  <div class="sbox" id="sbox">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
      <circle cx="11" cy="11" r="7"/><path d="M20 20l-4.3-4.3"/></svg>
    <input type="search" id="q" placeholder="区名・エリア名で検索（例：世田谷、帝塚山、青葉）" autocomplete="off">
    <button id="clr" aria-label="クリア">✕</button>
  </div>
  <div class="cfilter" id="filter"></div>
  <div class="wrap count" id="cnt" style="padding:0;margin-top:1.6rem"></div>
  <div class="ngrid" id="grid"></div>
  <div class="nempty" id="empty" style="display:none">該当する記事がありません。</div>
{LINEBOX}</div>
{DIAGNOSIS('エリア')}"""

js = "<script>const COLS=" + json.dumps(DATA, ensure_ascii=False, separators=(",",":")) \
   + ";\nconst IMG=" + json.dumps({k: IMG[k] for k in set(c["img"] for c in C)}, ensure_ascii=False) \
   + ";\nconst CITIES=" + json.dumps(CITIES, ensure_ascii=False) + ";</script>\n<script>" + """
let city="", q="";
const norm=s=>(s||"").replace(/[ぁ-ん]/g,c=>String.fromCharCode(c.charCodeAt(0)+0x60)).toLowerCase();
const hl=(s,t)=>t?s.replace(new RegExp(t.replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&"),"gi"),m=>`<mark>${m}</mark>`):s;
function chips(){
  const f=document.getElementById("filter");
  f.innerHTML=`<button class="fchip${city?"":" on"}" data-c="">すべて<em>${COLS.length}</em></button>`
   + CITIES.map(c=>`<button class="fchip${city===c?" on":""}" data-c="${c}">${c}<em>${COLS.filter(x=>x.city===c).length}</em></button>`).join("");
  f.querySelectorAll("button").forEach(b=>b.addEventListener("click",()=>{city=b.dataset.c;chips();draw();}));
}
function draw(){
  const t=q.trim(), n=norm(t);
  const L=COLS.filter(c=>(!city||c.city===city)&&(!t||norm(c.ward).includes(n)
    ||norm(c.title).includes(n)||norm(c.lead).includes(n)||c.areas.some(a=>norm(a).includes(n))));
  document.getElementById("cnt").textContent=`${L.length} 本の記事`;
  document.getElementById("sbox").classList.toggle("has",!!t);
  document.getElementById("empty").style.display=L.length?"none":"block";
  document.getElementById("grid").innerHTML=L.map(c=>`
   <a class="ncard" href="${c.slug}.html">
    <div class="ph" style="background-image:url(${IMG[c.img]})"></div>
    <div class="bd"><span class="ntag">${c.city==="東京23区"?c.ward:c.city+" "+c.ward}</span>
      <h3>${hl(c.title.split("｜")[0],t)}</h3>
      <p>${hl(c.lead,t)}</p>
      <div class="meta"><span class="av">ス</span><span>スピ不動産</span>
        <span class="dot"></span><span>地形・水系・地歴</span></div>
    </div></a>`).join("");
}
document.getElementById("q").addEventListener("input",e=>{q=e.target.value;draw();});
document.getElementById("clr").addEventListener("click",()=>{q="";document.getElementById("q").value="";draw();});
chips(); draw();
</script>"""

open(f"{OUT}/columns.html","w",encoding="utf-8").write(
  page("エリア別 風水・地形ガイド｜全72区の地形と住まい選び｜スピ不動産",
       "東京23区・大阪市・横浜市・福岡市の全72区について、地形・水系・街の成り立ちと住まい選びの確認点を解説します。",
       body, js))
print("columns.html")
