# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX, DIAGNOSIS
from ward_text import W
IMG = json.load(open("images.json", encoding="utf-8"))

# 検索対象にエリア名を含める
AREA_MAP = {en: [a[0] for a in v[3]] for en, v in W.items()}
SUB_MAP  = {en: v[0] for en, v in W.items()}

body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>エリア一覧</div>
<div class="wrap pg">
  <div class="eyebrow caps">Tokyo · Area Guide</div>
  <h1 class="pt">東京エリア一覧</h1>
  <div class="pt-sub">23区を、同じ目で比べる</div>
  <p class="lead">龍脈・地形・水気・地歴から23区を読み解きました。財運・仕事運・恋愛運・健康運の4カテゴリで
    各区の特性を比べられます。ただし区の平均は、あくまで目安です。同じ区でも町丁目によって評価は大きく動きます。
    気になる街が見つかったら、そこから先はご相談ください。</p>
  <div class="keys">
    <div class="key"><b style="background:#8A6E3C"></b>WEALTH <span>財運</span></div>
    <div class="key"><b style="background:#3B6BA5"></b>CAREER <span>仕事運</span></div>
    <div class="key"><b style="background:#8E4A63"></b>ROMANCE <span>恋愛運</span></div>
    <div class="key"><b style="background:#2F6B45"></b>VITALITY <span>健康運</span></div>
  </div>
  <div class="sbox" id="sbox">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
      <circle cx="11" cy="11" r="7"/><path d="M20 20l-4.3-4.3"/></svg>
    <input type="search" id="q" placeholder="区名・エリア名で検索（例：世田谷、麻布、二子玉川）" autocomplete="off">
    <button id="clr" aria-label="クリア">✕</button>
  </div>
  <p class="shint" id="hint"></p>
</div>
<div class="sortbar" id="sortbar">
  <span class="lb">SORT</span>
  <button data-k="total" class="on">総合 ↓</button>
  <button data-k="wealth">財運</button><button data-k="career">仕事運</button>
  <button data-k="romance">恋愛運</button><button data-k="vitality">健康運</button>
</div>
<div class="wrap count" id="cnt">23 区を表示中</div>
<div id="list"></div>
<div class="wrap sec">
  <div class="sec-hd"><h2>スコアについて</h2><span class="en">About the Score</span></div>
  <p class="note">龍脈・龍穴・尾根谷・標高・水脈・暗渠・湧水・地盤・地歴・神社仏閣との位置関係・災害履歴・
    道路の気の流れ・建物の向きなどを総合して算出しています。配点の詳細は非公開です。
    数字はきっかけに過ぎません。あなたの星と合うかどうかは、診断してはじめてわかります。</p>
{LINEBOX}</div>
{DIAGNOSIS('エリア')}"""

js = "<script>\nconst AREA_MAP=" + json.dumps(AREA_MAP, ensure_ascii=False) + \
     ";\nconst SUB_MAP=" + json.dumps(SUB_MAP, ensure_ascii=False) + """;
const E=FengshuiEngine;
const rows=Subjects.wards.map(w=>{const r=E.evaluate(w),f=E.deriveFortunes(r);
  const m={};f.forEach(x=>m[x.id]=x.score);
  return {w,r,f,m,areas:AREA_MAP[w.en]||[],sub:SUB_MAP[w.en]||w.tagline};});
let key="total", q="";
const norm=s=>s.replace(/[ぁ-ん]/g,c=>String.fromCharCode(c.charCodeAt(0)+0x60)).toLowerCase();
const hl=(s,t)=>t? s.replace(new RegExp(t.replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&"),"gi"),m=>`<mark>${m}</mark>`):s;

function draw(){
  const t=q.trim();
  let list=rows.slice().sort((a,b)=>key==="total"?b.r.total-a.r.total:(b.m[key]||0)-(a.m[key]||0));
  if(t){
    const n=norm(t);
    list=list.filter(o=>norm(o.w.name).includes(n)||norm(o.sub).includes(n)
      ||o.areas.some(a=>norm(a).includes(n))||norm(o.w.en).includes(n));
  }
  document.getElementById("cnt").textContent=`${list.length} 区を表示中`;
  const hint=document.getElementById("hint");
  if(t){
    const hits=list.flatMap(o=>o.areas.filter(a=>norm(a).includes(norm(t))));
    hint.innerHTML = list.length
      ? `<b>${t}</b> の検索結果：${list.length}区` + (hits.length?`／該当エリア ${hits.slice(0,4).join("・")}${hits.length>4?" ほか":""}`:"")
      : `<b>${t}</b> に一致する区・エリアは見つかりませんでした。`;
  } else hint.textContent="";
  document.getElementById("sbox").classList.toggle("has", !!t);
  document.getElementById("list").innerHTML=list.map((o,i)=>{
    const star=n=>{const s=n>=90?5:n>=80?4:n>=70?3:n>=60?2:1;return "★".repeat(s)+`<i>${"★".repeat(5-s)}</i>`;};
    const cells=o.f.map(x=>`<div class="sr${x.id===key?" top":""}">
      <span class="l" style="color:${x.color}">${x.label}</span>
      <span class="st" style="color:${x.color}">${star(x.score||0)}</span>
      <span class="n">${x.score??"—"}</span></div>`).join("");
    const hitArea=t? o.areas.filter(a=>norm(a).includes(norm(t))).slice(0,3):[];
    return `<a class="wrow" href="ward-${o.w.en.toLowerCase()}.html"><div class="in">
      <div class="h"><span class="rk">${String(i+1).padStart(2,"0")}</span>
        <span class="nm">${hl(o.w.name,t)}</span>
        <span class="tg">${hitArea.length? hitArea.map(a=>hl(a,t)).join("・") : o.w.areaCount+" エリア"}</span>
        <span class="tot"><i>${o.r.grade}</i><b>${o.r.total}</b></span></div>
      <div class="sgrid">${cells}</div></div></a>`;}).join("")
    || '<div class="wrap" style="padding:3rem 0;text-align:center;color:var(--ink-2)">条件に合う区がありません。</div>';
}
document.querySelectorAll("#sortbar button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#sortbar button").forEach(x=>{x.classList.remove("on");
    x.textContent=x.textContent.replace(" ↓","");});
  b.classList.add("on");b.textContent+=" ↓";key=b.dataset.k;draw();}));
document.getElementById("q").addEventListener("input",e=>{q=e.target.value;draw();});
document.getElementById("clr").addEventListener("click",()=>{
  q="";document.getElementById("q").value="";draw();document.getElementById("q").focus();});
draw();
</script>"""

open(f"{OUT}/areas.html","w",encoding="utf-8").write(
  page("東京エリア一覧｜23区を同じ目で比べる｜スピ不動産",
       "龍脈・地形・地歴から東京23区を読み解き、財運・仕事運・恋愛運・健康運で比較できます。区名・エリア名で検索できます。",
       body, js))
print("areas.html")
