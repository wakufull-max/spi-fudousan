# -*- coding: utf-8 -*-
from common_v2 import *

# ══════════════════════════════════════════════════
#  A. 評価コンソール（採点基準の全公開）
# ══════════════════════════════════════════════════
demo_body = """
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>採点基準・評価コンソール</div>
<div class="wrap pg">
  <div class="eyebrow caps">Scoring Engine v2.0</div>
  <h1 class="pt">採点基準の全公開</h1>
  <div class="pt-sub">22項目を、根拠つきで開示します</div>
  <p class="lead">総合点は22の評価モジュールの加重平均です。各項目が何点で、なぜその点になり、
    どのデータを根拠にしたのかをすべて開示します。評価対象を切り替えると、
    区・町丁目・建物のどの階層でも同じエンジンが動くことが確認できます。
    階層が細かいほど判定できる項目が増え、データ充足率が上がります。</p>

  <div class="form">
    <div class="fld" style="grid-column:span 2">
      <label for="subj">評価対象</label>
      <select id="subj"></select>
    </div>
    <div class="fld"><label for="bd">生年月日（相性）</label><input type="date" id="bd" value="1990-05-12"></div>
    <div class="fld"><label for="tm">出生時刻（任意）</label><input type="time" id="tm" value="14:30"></div>
    <div class="fld"><label for="gd">性別</label><select id="gd"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="fld"><label>&nbsp;</label><button class="btn" id="run" style="width:100%">評価する</button></div>
  </div>

  <div id="out"></div>
</div>
"""

demo_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
const list=[].concat(
  Subjects.wards.map(w=>({v:w.id,t:"【区】"+w.name})),
  [{v:"town-azabudai",t:"【町丁目】麻布台・六本木"}],
  Subjects.properties.map(p=>({v:p.id,t:"【建物】"+p.name})),
  [{v:"bldg-hamarikyu",t:"【建物・対比】浜離宮 ザ・タワー（低地／形殺あり）"}]
);
const sel=document.getElementById("subj");
sel.innerHTML=list.map(o=>`<option value="${o.v}">${o.t}</option>`).join("");
sel.value="prop-1";

function run(){
  const s=Subjects.byId(sel.value); if(!s)return;
  const r=E.evaluate(s);
  let personal=null,comb=null;
  const bd=document.getElementById("bd").value;
  if(bd && s.building){
    personal=E.evaluatePersonal(s,{birth:bd,time:document.getElementById("tm").value||null,
      gender:document.getElementById("gd").value,lng:139.6917});
    comb=E.combine(r,personal);
  }
  document.getElementById("out").innerHTML =
     R.scoreHeader(r)
   + '<div class="sec"><div class="sec-hd"><h2>分類別</h2><span class="en">By Category</span></div></div>'
   + R.categories(r)
   + '<div class="sec"><div class="sec-hd"><h2>強みと弱み</h2><span class="en">Strengths & Weaknesses</span></div></div>'
   + R.highlights(r)
   + '<div class="sec"><div class="sec-hd"><h2>全22項目の内訳</h2><span class="en">All Modules</span>'
   + '<p class="note">各項目をタップすると、判定理由と根拠データ・出典が開きます。</p></div></div>'
   + R.modules(r)
   + (personal ? '<div class="sec"><div class="sec-hd"><h2>居住者との相性</h2><span class="en">Personal Fit</span>'
       + '<p class="note">九星気学と四柱推命による別レイヤーの評価です。物件固有スコアには合算しません。</p></div></div>'
       + R.personal(personal,comb) : '');
}
document.getElementById("run").addEventListener("click",run);
sel.addEventListener("change",run);
run();
</script>"""

open(f"{OUT}/score-demo.html","w",encoding="utf-8").write(
  page("採点基準の全公開｜風水評価エンジン v2.0｜龍脈",
       "22項目の評価モジュールを根拠つきで開示。区・町丁目・建物の各階層で同じエンジンが動きます。",
       demo_body, demo_js))
print("score-demo.html")

# ══════════════════════════════════════════════════
#  B. 区一覧
# ══════════════════════════════════════════════════
areas_body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>エリア風水ガイド</div>
<div class="wrap pg">
  <div class="eyebrow caps">Tokyo · Ward Feng Shui Guide</div>
  <h1 class="pt">東京エリア一覧</h1>
  <div class="pt-sub">23区を、同じ基準で採点する</div>
  <p class="lead">龍脈・地形・標高・地盤・地歴・災害履歴を評価モジュールにかけ、区ごとの総合点を算出しました。
    区単位で判定できるのは22項目のうち8項目で、道路形状や建物の向きは町丁目・建物単位でないと判定できません。
    そのためデータ充足率は各区とも45%前後です。数値は「その階層でわかる範囲の評価」であり、
    実際の住まい選びでは町丁目まで下りて確認してください。</p>
  <div class="plate"><img src="{IMG['tokyo']}" alt=""></div>
</div>

<div class="sortbar" id="sortbar">
  <span class="lb">SORT</span>
  <button data-k="total" class="on">総合 ↓</button>
  <button data-k="terrain">地形・自然</button>
  <button data-k="history">歴史・土地</button>
  <button data-k="environment">周辺環境</button>
</div>
<div class="wrap count">23 区を表示中</div>
<div id="list"></div>

<div class="wrap sec">
  <div class="sec-hd"><h2>採点基準について</h2><span class="en">Methodology</span></div>
  <p class="note">総合点は22の評価モジュールの加重平均です。各項目の配点・判定理由・根拠データはすべて公開しています。</p>
  <div class="center"><a class="obtn" href="score-demo.html">評価コンソールで内訳を見る →</a></div>
</div>
"""

areas_js = """<script>
const E=FengshuiEngine;
const CAT=["terrain","history","environment"];
const rows=Subjects.wards.map(w=>{
  const r=E.evaluate(w);
  const c={};r.categories.forEach(x=>c[x.id]=x.score);
  return {w,r,c};
});
function draw(k){
  rows.sort((a,b)=>(k==="total"?b.r.total-a.r.total:(b.c[k]??-1)-(a.c[k]??-1)));
  document.getElementById("list").innerHTML=rows.map((o,i)=>{
    const href=o.w.id==="ward-minato"?"ward-minato.html":"#";
    const bars=o.r.categories.map(x=>`<div class="mrow"><div class="t"><span>${x.label}</span>
      <b>${x.score??"—"}</b></div>${FengshuiRender.bar(x.score||0,
        x.score==null?"":x.score>=70?"up":x.score<50?"down":"")}</div>`).join("");
    return `<a class="wrow" href="${href}"><div class="in">
      <div class="h"><span class="rk">${String(i+1).padStart(2,"0")}</span>
        <span class="nm">${o.w.name}</span><span class="tg">${o.w.tagline}</span>
        <span class="tot"><i>${o.r.grade}</i><b>${o.r.total}</b></span></div>
      <div class="g">${bars}</div></div></a>`;}).join("");
}
document.querySelectorAll("#sortbar button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#sortbar button").forEach(x=>{x.classList.remove("on");
    x.textContent=x.textContent.replace(" ↓","");});
  b.classList.add("on");b.textContent+=" ↓";draw(b.dataset.k);}));
draw("total");
</script>"""

open(f"{OUT}/areas.html","w",encoding="utf-8").write(
  page("東京エリア一覧｜23区を同じ基準で採点｜龍脈",
       "龍脈・地形・標高・地盤・地歴・災害履歴から東京23区を採点。分類別の強み弱みで並べ替えできます。",
       areas_body, areas_js))
print("areas.html")

# ══════════════════════════════════════════════════
#  C. 区ページ（港区）
# ══════════════════════════════════════════════════
MINATO_AREAS = [
 ("麻布台・六本木","area-azabudai.html","六本木台地の頂部。標高30m超の高台に大龍脈が通り、区内で最も気の密度が高い。"),
 ("南青山","#","明治神宮の社叢から続く緑の帯。台地上で南東に開ける。"),
 ("白金・白金台","#","目黒台の丘陵に載る住宅地。標高は高いが幹線道路の近接で減点が入る。"),
 ("赤坂・乃木坂","#","台地の縁と谷が交互に走る。区画ごとの標高差が評価を分ける。"),
 ("虎ノ門・愛宕","#","愛宕山という独立丘を抱える。周囲より20m以上高く龍穴の条件を満たす。"),
 ("高輪","#","高輪台の斜面。海へ下る傾斜が背山面水の形をつくる。"),
 ("三田・田町","#","台地と埋立の境界線上。数百mで評価が反転する。"),
 ("浜松町・大門","#","旧海面の埋立地。地勢点が伸びず、形殺の減点も重なる。"),
]
acards = "".join(
 f'<a class="wrow" href="{h}" style="border:1px solid var(--rule);margin-bottom:.6rem">'
 f'<div class="in" style="padding:1.1rem 1.2rem">'
 f'<div class="h"><span class="rk">{i+1:02d}</span><span class="nm" style="font-size:1.15rem">{n}</span></div>'
 f'<p style="font-size:.84rem;color:var(--ink-2);margin-top:.4rem">{p}</p></div></a>'
 for i,(n,h,p) in enumerate(MINATO_AREAS))

ward_body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水ガイド</a><span>/</span>港区</div>
<div class="wrap pg">
  <div class="eyebrow">Ward Guide · MINATO</div>
  <h1 class="pt">港区</h1>
  <div class="pt-sub">台地・水辺・国際の気</div>
  <div class="plate"><img src="{IMG['minato']}" alt="港区"></div>
  <p class="lead">麻布・白金・高輪の台地と、芝浦・港南の埋立低地が同居する区です。
    平均標高は21.4mですが区内の標高差は30m以上あり、同じ港区でも町丁目によって地勢の評価が大きく動きます。
    江戸期に大名屋敷が台地へ、漁村と海が低地へ置かれた構造が、そのまま現在の評価差として残っています。</p>
  <div class="chips"><span class="chip">大龍脈</span><span class="chip">台地・ローム</span>
    <span class="chip">大名屋敷</span><span class="chip">液状化・低</span></div>
  <div id="out"></div>
</div>

<div class="wrap sec">
  <div class="sec-hd"><h2>港区のエリア</h2><span class="en">16 Areas</span>
  <p class="note">区の平均値ではなく、町丁目まで下りると判定できる項目が増えます。</p></div>
  <div style="margin-top:1.2rem">{acards}</div>
  <div class="center"><a class="obtn" href="areas.html">他の区と比べる →</a></div>
</div>
"""
ward_js = """<script>
const E=FengshuiEngine,R=FengshuiRender,s=Subjects.byId("ward-minato"),r=E.evaluate(s);
document.getElementById("out").innerHTML =
   R.scoreHeader(r)
 + '<div class="sec"><div class="sec-hd"><h2>分類別</h2><span class="en">By Category</span></div></div>'
 + R.categories(r)
 + '<div class="sec"><div class="sec-hd"><h2>強みと弱み</h2><span class="en">Strengths & Weaknesses</span></div></div>'
 + R.highlights(r)
 + '<div class="sec"><div class="sec-hd"><h2>評価項目の内訳</h2><span class="en">All Modules</span>'
 + '<p class="note">タップすると判定理由と根拠データが開きます。区単位では判定できない項目は「階層対象外」と表示されます。</p></div></div>'
 + R.modules(r);
</script>"""

open(f"{OUT}/ward-minato.html","w",encoding="utf-8").write(
  page("港区の風水｜龍脈・地形・地歴から採点｜龍脈",
       "港区の風水を22項目の評価モジュールで採点。判定理由と根拠データをすべて公開しています。",
       ward_body, ward_js))
print("ward-minato.html")

# ══════════════════════════════════════════════════
#  D. 町エリアページ（麻布台・六本木）
# ══════════════════════════════════════════════════
area_body = """
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水ガイド</a><span>/</span><a href="ward-minato.html">港区</a><span>/</span>麻布台・六本木</div>
<div class="wrap pg">
  <div class="eyebrow">Area Guide · 港区</div>
  <h1 class="pt">麻布台・六本木</h1>
  <div class="pt-ward">港区</div>
  <p class="lead">六本木台地の最高点。標高30.4m、周囲の古川低地との比高は26mあり、
    江戸城から南西に伸びる副龍脈の末端にあたります。尾根線の連続性は0.95で、
    大龍脈のなかでも途切れのない区間です。</p>
  <div class="chips"><span class="chip">大龍脈</span><span class="chip">龍穴</span>
    <span class="chip">尾根</span><span class="chip">大名屋敷</span><span class="chip">浸水想定外</span></div>

  <div class="sec"><div class="sec-hd"><h2>評価の階層を切り替える</h2><span class="en">Evaluation Level</span>
    <p class="note">同じエンジンで、町丁目単位と建物単位の両方を評価できます。階層が下がるほど判定項目が増えます。</p></div></div>
  <div class="form" style="grid-template-columns:1fr">
    <div class="fld"><label for="lv">評価対象</label><select id="lv">
      <option value="town-azabudai">【町丁目】麻布台・六本木（道路・建物の項目は判定不可）</option>
      <option value="bldg-azabudai-residence" selected>【建物】麻布台ヒルズ レジデンス（全22項目）</option>
    </select></div>
  </div>
  <div id="out"></div>

  <div class="sec"><div class="sec-hd"><h2>居住者との相性</h2><span class="en">Personal Fit</span>
    <p class="note">生年月日から九星気学の本命卦と、四柱推命の日主・用神を算出し、この立地との相性を判定します。
      出生時刻を入れると時柱まで求まり精度が上がります。真太陽時（経度差＋均時差）は自動補正します。</p></div></div>
  <div class="form">
    <div class="fld"><label for="bd">生年月日</label><input type="date" id="bd" value="1990-05-12"></div>
    <div class="fld"><label for="tm">出生時刻（任意）</label><input type="time" id="tm" value="14:30"></div>
    <div class="fld"><label for="gd">性別</label><select id="gd"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="fld"><label>&nbsp;</label><button class="btn" id="run" style="width:100%">相性を判定する</button></div>
  </div>
  <div id="pout"></div>
</div>
"""
area_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
function drawBase(){
  const s=Subjects.byId(document.getElementById("lv").value), r=E.evaluate(s);
  document.getElementById("out").innerHTML =
     R.scoreHeader(r)
   + '<div class="sec"><div class="sec-hd"><h2>分類別</h2><span class="en">By Category</span></div></div>'
   + R.categories(r)
   + '<div class="sec"><div class="sec-hd"><h2>強みと弱み</h2><span class="en">Strengths & Weaknesses</span></div></div>'
   + R.highlights(r)
   + '<div class="sec"><div class="sec-hd"><h2>評価項目の内訳</h2><span class="en">All Modules</span></div></div>'
   + R.modules(r);
  document.getElementById("pout").innerHTML="";
}
function drawPersonal(){
  const s=Subjects.byId(document.getElementById("lv").value);
  if(!s.building){document.getElementById("pout").innerHTML=
    '<p class="note">建物の向きが確定していないため、相性判定には建物単位を選んでください。</p>';return;}
  const p=E.evaluatePersonal(s,{birth:document.getElementById("bd").value,
    time:document.getElementById("tm").value||null,gender:document.getElementById("gd").value,lng:139.6917});
  document.getElementById("pout").innerHTML=R.personal(p,E.combine(E.evaluate(s),p));
}
document.getElementById("lv").addEventListener("change",drawBase);
document.getElementById("run").addEventListener("click",drawPersonal);
drawBase();
</script>"""

open(f"{OUT}/area-azabudai.html","w",encoding="utf-8").write(
  page("麻布台・六本木の風水｜港区エリアガイド｜龍脈",
       "麻布台・六本木を22項目で採点。町丁目単位と建物単位を切り替えて内訳と根拠を確認できます。",
       area_body, area_js))
print("area-azabudai.html")
