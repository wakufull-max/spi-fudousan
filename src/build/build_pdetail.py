# -*- coding: utf-8 -*-
"""物件詳細ページ（1枚でURLパラメータから切り替え）"""
import json
from common_v2 import *
from brand import LINEBOX, DIAGNOSIS
IMG = json.load(open("images.json", encoding="utf-8"))
P = json.load(open("props_scored.json", encoding="utf-8"))
for p in P: p["ready"] = p["pref"] == "東京都"

KEEP = ("id","name","pref","city","ward","price","priceN","addr","st","walk","layout","area",
        "builtLabel","built","face","dir","sanju","url","img","total","grade","label","cov","era","tsubo","ready")
DATA = []
for p in P:
    d = {k: p[k] for k in KEEP}
    d["f"] = [[x["id"], x["l"], x["s"]] for x in p["f"]]
    DATA.append(d)

body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="properties.html">物件一覧</a><span>/</span><span id="bc">物件</span></div>
<div class="wrap pg">
  <div class="eyebrow" id="eyebrow">Property</div>
  <h1 class="pt" id="pname">—</h1>
  <div class="pt-ward" id="pward">—</div>
  <div class="pill-row" id="pills"></div>
  <div class="spec" id="spec"></div>
  <div id="panel"></div>
  <div class="center" style="margin-top:1.8rem"><a class="obtn" id="src" href="#" target="_blank" rel="noopener">掲載ページで詳細を見る →</a></div>
</div>
<div class="wrap sec"><div class="sec-hd"><h2>この物件の風水解説</h2><span class="en">Fengshui</span></div></div>
<div class="fgrid" id="fcards"></div><div class="rail-hint">← スワイプで続きを読む</div>
<div class="wrap sec"><div class="sec-hd"><h2>この物件の位置</h2><span class="en">Map</span></div><div id="map"></div></div>
<div class="wrap sec"><div class="sec-hd"><h2>同じエリアの物件</h2><span class="en">Nearby</span></div></div>
<div class="rail" id="prail"></div><div class="rail-hint">← スワイプで続きを見る</div>
<div class="wrap sec"><div class="center"><a class="obtn" href="properties.html">物件一覧をすべて見る →</a></div></div>
<div class="wrap sec">
  <p class="note" id="disc"></p>
{LINEBOX}</div>
{DIAGNOSIS('この物件')}"""

js = "<script>const PROPS=" + json.dumps(DATA, ensure_ascii=False, separators=(",",":")) + ";</script>\n<script>" + """
const E=FengshuiEngine,R=FengshuiRender;
const id=new URLSearchParams(location.search).get("id");
const p=PROPS.find(x=>x.id===id)||PROPS.find(x=>x.ready&&x.total>=80)||PROPS[0];
const AV=E.averageFortunes(Subjects.wards);

document.title=`${p.name}｜${p.ward}の物件｜スピ不動産`;
document.getElementById("bc").textContent=p.name;
document.getElementById("eyebrow").textContent=`Property · ${p.pref==="東京都"?p.ward:p.city+" "+p.ward}`;
document.getElementById("pname").textContent=p.name;
document.getElementById("pward").textContent=`${p.pref==="東京都"?"東京都 "+p.ward:p.pref+" "+p.city+p.ward}`;
document.getElementById("src").href=p.url;

document.getElementById("pills").innerHTML=[p.dir+"向き",p.layout,p.area+"㎡",p.builtLabel+"築",
  p.st+"駅 徒歩"+p.walk+"分"].map(t=>`<span class="pill-k">${t}</span>`).join("");
document.getElementById("spec").innerHTML=`<dl>
  <dt>販売価格</dt><dd>${p.price}</dd>
  <dt>所在地</dt><dd>${p.addr}</dd>
  <dt>最寄駅</dt><dd>${p.st} 徒歩${p.walk}分</dd>
  <dt>間取り</dt><dd>${p.layout}</dd>
  <dt>専有面積</dt><dd>${p.area}㎡（約${(p.area/3.30578).toFixed(2)}坪）</dd>
  <dt>坪単価</dt><dd>${p.tsubo?Math.round(p.tsubo/10000).toLocaleString()+"万円／坪":"—"}</dd>
  <dt>築年月</dt><dd>${p.builtLabel}（築${2026-p.built}年）</dd>
  <dt>坐向</dt><dd>${p.face}向き／二十四山では${p.sanju}向</dd>
</dl>`;

if(p.ready){
  const f=p.f.map(([id,l,s])=>({id,label:l,en:{wealth:"Wealth",career:"Career",romance:"Romance",vitality:"Vitality"}[id]||"",
    score:s,color:{wealth:"#8A6E3C",career:"#3B6BA5",romance:"#8E4A63",vitality:"#2F6B45"}[id]}));
  document.getElementById("panel").innerHTML=R.fortunePanel(
    {total:p.total,grade:p.grade,label:p.label}, f, AV,
    `${p.ward}の地相を土台に、${p.dir}向き・${p.builtLabel}築という建物固有の条件を重ねた見立てです。データ充足率は${p.cov}%です。`,
    "diagnosis.html");
}else{
  document.getElementById("panel").innerHTML=
   `<div class="panel"><section class="p-col">
      <div class="p-k">DIRECTION ONLY</div><h3 class="p-t">方位の見立て</h3>
      <div class="ov-main"><span class="ov-g">${p.era>=80?"吉":p.era>=55?"平":"弱"}</span>
        <span class="ov-n">${p.era}<small>/100</small></span></div>
      <span class="ov-pill">${p.dir}向き</span>
      <p class="ov-d">${p.city}${p.ward}は地相データが未整備のため、総合評価は出していません。
        表示しているのは三元九運（2024–2043）にもとづく方位の適合のみです。
        南が旺気、北が生気、南西が進気にあたる期間です。</p>
      <a class="ov-cta" href="diagnosis.html">あなたとの相性を診断する　→</a>
    </section></div>`;
}

const CARDS=[
 ["FACING","坐向",`正面方位は${p.face}（${p.dir}）。二十四山では${p.sanju}向にあたります。`
  +`三元九運は2024年2月4日から九運に入り、当令は九紫＝離＝南。`
  +`${p.dir}は${({南:"旺気",北:"生気",南西:"進気",北東:"退気（前運の余勢）",東:"平気",南東:"平気",西:"衰気",北西:"衰気"})[p.dir]}にあたります。`
  +`${p.built>=2024?"竣工が九運期に入ってからのため、当運の気を受けます。":p.built>=2004?"竣工は八運期です。2024年の九運入りで方位の吉凶が入れ替わっており、当時の評価をそのまま当てはめられません。":"竣工は七運以前です。"}`],
 ["SCALE","規模と間取り",`専有${p.area}㎡（約${(p.area/3.30578).toFixed(1)}坪）の${p.layout}。`
  +`${p.area>=120?"広い間取りは気が拡散しやすいため、居室ごとに用途を定めて気を留めるのが要点になります。":p.area>=80?"family向けの標準的な広さで、玄関から居室への動線を整えれば気が巡ります。":"気が凝縮しやすいコンパクトな間取りです。玄関・寝室・仕事場の方位を個別に整えると効果が出やすくなります。"}`
  +`坪単価は${p.tsubo?Math.round(p.tsubo/10000).toLocaleString()+"万円":"—"}です。`],
 ["ACCESS","立地",`${p.st}駅から徒歩${p.walk}分。`
  +`${p.walk<=3?"駅至近は人の気の流れが速く、商いや発信には向きますが、腰を据えるなら静穏さとの兼ね合いを見る必要があります。":p.walk<=7?"駅から適度に離れ、利便性と静穏さのバランスが取れる距離です。":"駅から離れるぶん気の流れが穏やかで、住まいとして落ち着きます。"}`
  +`所在は${p.addr}です。`]];
document.getElementById("fcards").innerHTML=CARDS.map(([k,jp,t])=>
  `<article class="fcard"><div class="k">${k}</div><h3>${jp}</h3><hr><p>${t}</p></article>`).join("");

document.getElementById("map").innerHTML=R.gmap(p.addr,p.name);

const near=PROPS.filter(x=>x.id!==p.id&&x.ward===p.ward&&x.city===p.city).slice(0,6);
const pool=near.length?near:PROPS.filter(x=>x.id!==p.id&&x.city===p.city).slice(0,6);
document.getElementById("prail").innerHTML=pool.map((x,i)=>`
 <a class="pcard" href="property.html?id=${x.id}"><span class="wm">${x.ready?x.total:x.era}</span>
  <div class="top"><span class="no">${String(i+1).padStart(2,"0")}</span><span class="badge">売買</span></div>
  <div class="ar">${x.ward}</div><h3>${x.name}</h3><hr>
  <dl class="kv"><dt>売買</dt><dd>${x.price}</dd></dl>
  <div class="st">${x.st}駅 徒歩${x.walk}分　／　${x.dir}向き</div>
  <div class="fs"><div class="l">${x.ready?"気の見立て":"方位の見立て"}</div>
    <div class="row"><b>${x.ready?x.total:x.era}</b><small>pt</small><span class="arw">→</span></div></div></a>`).join("");

document.getElementById("disc").textContent=
 `掲載情報はSUUMOの公開ページ（${p.url}）にもとづく参考値です。募集の有無・価格・条件は掲載元で必ずご確認ください。`
 +`気の見立ては当社独自の指標であり、物件の価値や資産性を保証するものではありません。`;
</script>"""

open(f"{OUT}/property.html","w",encoding="utf-8").write(
  page("物件詳細｜東京・横浜・大阪・福岡の高級物件｜スピ不動産",
       "物件ごとの価格・専有面積・間取り・方角・築年月に加えて、龍脈・地形・地歴から読んだ土地の気の見立てと、周辺の物件をご覧いただけます。", body, js))
print("property.html", round(len(open(f"{OUT}/property.html",encoding='utf-8').read())/1024), "KB")
