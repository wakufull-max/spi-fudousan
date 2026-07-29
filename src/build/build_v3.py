# -*- coding: utf-8 -*-
from common_v2 import *

# ══════════════════════════════════════════════════
#  A. 区一覧
# ══════════════════════════════════════════════════
areas_body = """
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>エリア風水ガイド</div>
<div class="wrap pg">
  <div class="eyebrow caps">Tokyo · Ward Feng Shui Guide</div>
  <h1 class="pt">東京エリア一覧</h1>
  <div class="pt-sub">23区を、同じ基準で比べる</div>
  <p class="lead">龍脈・地形・標高・地盤・地歴・災害履歴を読み解き、区ごとの運気を財運・仕事運・恋愛運・健康運の
    4つに整理しました。区の平均値は目安です。実際の住まい選びでは町丁目まで下りてご確認ください。</p>
  <div class="illus" id="illus"></div>
</div>
<div class="sortbar" id="sortbar">
  <span class="lb">SORT</span>
  <button data-k="total" class="on">総合 ↓</button>
  <button data-k="wealth">財運</button>
  <button data-k="career">仕事運</button>
  <button data-k="romance">恋愛運</button>
  <button data-k="vitality">健康運</button>
</div>
<div class="wrap count">23 区を表示中</div>
<div id="list"></div>
<div class="wrap sec">
  <div class="sec-hd"><h2>スコアについて</h2><span class="en">About the Score</span></div>
  <p class="note">龍脈・龍穴・尾根谷・標高・水脈・暗渠・湧水・地盤・地歴（江戸切絵図／明治・昭和の古地図／旧航空写真／旧土地利用）・
    神社仏閣との位置関係・災害履歴・道路の気の流れ・建物の向きなどを総合して算出しています。
    配点の詳細は非公開です。個別のご相談では、どの要素がどう効いているかを口頭でお伝えします。</p>
</div>
"""
areas_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
document.getElementById("illus").innerHTML=Illustrations.get("chiyoda");
const AVG=E.averageFortunes(Subjects.wards);
const rows=Subjects.wards.map(w=>{const r=E.evaluate(w);const f=E.deriveFortunes(r);
  const m={};f.forEach(x=>m[x.id]=x.score);return {w,r,f,m};});
const IL={"ward-minato":"minato","ward-chiyoda":"chiyoda","ward-shibuya":"shibuya",
  "ward-meguro":"meguro","ward-setagaya":"setagaya","ward-chuo":"chuo"};
function draw(k){
  rows.sort((a,b)=>k==="total"?b.r.total-a.r.total:(b.m[k]||0)-(a.m[k]||0));
  document.getElementById("list").innerHTML=rows.map((o,i)=>{
    const href=o.w.id==="ward-minato"?"ward-minato.html":"#";
    const cells=o.f.map(x=>`<div class="mrow"><div class="t"><span style="color:${x.color}">${x.label}</span>
      <b>${x.score??"—"}</b></div>${R.bar(x.score||0,x.score>=78?"up":x.score<55?"down":"")}</div>`).join("");
    return `<a class="wrow" href="${href}"><div class="in">
      <div class="h"><span class="rk">${String(i+1).padStart(2,"0")}</span>
        <span class="nm">${o.w.name}</span>
        <span class="tot"><i>${o.r.grade}</i><b>${o.r.total}</b></span>
        <span class="tg">${o.w.tagline}</span></div>
      <div class="g">${cells}</div></div></a>`;}).join("");
}
document.querySelectorAll("#sortbar button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#sortbar button").forEach(x=>{x.classList.remove("on");
    x.textContent=x.textContent.replace(" ↓","");});
  b.classList.add("on");b.textContent+=" ↓";draw(b.dataset.k);}));
draw("total");
</script>"""
open(f"{OUT}/areas.html","w",encoding="utf-8").write(
  page("東京エリア一覧｜23区の風水を比べる｜龍脈",
       "龍脈・地形・地歴・災害履歴から東京23区の運気を財運・仕事運・恋愛運・健康運で比較できます。",
       areas_body, areas_js))
print("areas.html")

# ══════════════════════════════════════════════════
#  B. 区ページ（港区）
# ══════════════════════════════════════════════════
MINATO_AREAS = [
 ("麻布台・六本木","area-azabudai.html","六本木台地の頂部。標高30m超の高台に龍脈が通り、区内で最も気の密度が高い。"),
 ("南青山","#","明治神宮の社叢から続く緑の帯。台地上で南東に開ける。"),
 ("白金・白金台","#","目黒台の丘陵に載る住宅地。標高は高いが幹線道路が近い。"),
 ("赤坂・乃木坂","#","台地の縁と谷が交互に走る。区画ごとの標高差が評価を分ける。"),
 ("虎ノ門・愛宕","#","愛宕山という独立丘を抱える。周囲より20m以上高い。"),
 ("高輪","#","高輪台の斜面。海へ下る傾斜が背山面水の形をつくる。"),
 ("三田・田町","#","台地と埋立の境界線上。数百mで評価が反転する。"),
 ("浜松町・大門","#","旧海面の埋立地。地勢の弱さを水勢と方位で補う構造。"),
]
alist = "".join(
 f'<a class="aitem" href="{h}"><div class="t"><span class="n">{i+1:02d}</span>'
 f'<span class="nm">{n}</span><span class="ar">→</span></div><p>{p}</p></a>'
 for i,(n,h,p) in enumerate(MINATO_AREAS))

ward_body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水ガイド</a><span>/</span>港区</div>
<div class="wrap pg">
  <div class="eyebrow">Ward Guide · MINATO</div>
  <h1 class="pt">港区</h1>
  <div class="pt-sub">台地・水辺・国際の気</div>
  <div class="illus" id="illus"></div>
  <p class="lead">麻布・白金・高輪の台地と、芝浦・港南の埋立低地が同居する区です。
    平均標高は21.4mですが区内の標高差は30m以上あり、同じ港区でも町丁目によって評価が大きく動きます。
    江戸期に大名屋敷が台地へ、漁村と海が低地へ置かれた構造が、そのまま現在の差として残っています。</p>
  <div class="chips"><span class="chip">龍脈</span><span class="chip">台地</span>
    <span class="chip">大名屋敷</span><span class="chip">水辺</span></div>
  <div id="out"></div>
  <a class="cta-dark" href="index.html#diagnose">無料で相性を診断する　→</a>
</div>
<div class="wrap sec">
  <div class="sec-hd"><h2>港区のエリア</h2><span class="en">16 Areas</span>
  <p class="note">区の平均ではなく、町丁目まで下りると評価が変わります。</p></div>
  <div class="alist">{alist}</div>
  <div class="center"><a class="obtn" href="areas.html">他の区と比べる →</a></div>
</div>
<div class="wrap sec">
  <div class="sec-hd"><h2>港区の位置</h2><span class="en">Map</span></div>
  <div id="map"></div>
</div>
"""
ward_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
document.getElementById("illus").innerHTML=Illustrations.get("minato");
const s=Subjects.byId("ward-minato"),r=E.evaluate(s),f=E.deriveFortunes(r);
document.getElementById("out").innerHTML =
   R.fortuneRadar(f,E.averageFortunes(Subjects.wards),r.grade,r.label)
 + R.fortuneRows(f)
 + '<div class="sec"><div class="sec-hd"><h2>この土地の読み方</h2><span class="en">Reading</span></div></div>'
 + R.publicSummary(r);
document.getElementById("map").innerHTML=R.gmap("東京都港区","港区");
</script>"""
open(f"{OUT}/ward-minato.html","w",encoding="utf-8").write(
  page("港区の風水｜龍脈・地形・地歴から読む｜龍脈",
       "港区の風水を龍脈・地形・地歴から読み解き、財運・仕事運・恋愛運・健康運の4軸で示します。",
       ward_body, ward_js))
print("ward-minato.html")

# ══════════════════════════════════════════════════
#  C. 町エリアページ（麻布台・六本木）
# ══════════════════════════════════════════════════
area_body = """
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水ガイド</a><span>/</span><a href="ward-minato.html">港区</a><span>/</span>麻布台・六本木</div>
<div class="wrap pg">
  <div class="eyebrow">Area Guide · 港区</div>
  <h1 class="pt">麻布台・六本木</h1>
  <div class="pt-ward">港区</div>
  <div class="illus" id="illus"></div>
  <p class="lead">六本木台地の最高点。標高30.4m、周囲の低地との比高は26mあり、
    江戸城から南西へ伸びる龍脈の末端にあたります。尾根の連なりは途切れがなく、
    東に皇居、南西に東京湾を望む背山面水の形が高層から成立します。</p>
  <div class="chips"><span class="chip">龍脈</span><span class="chip">龍穴</span>
    <span class="chip">尾根</span><span class="chip">大名屋敷</span><span class="chip">浸水想定外</span></div>
  <div id="out"></div>
</div>

<div class="wrap sec">
  <div class="sec-hd"><h2>このエリアの位置</h2><span class="en">Map</span></div>
  <div id="map"></div>
</div>

<div class="wrap sec">
  <div class="sec-hd"><h2>このエリアの物件</h2><span class="en">Properties</span></div>
  <div id="props"></div>
</div>

<div class="wrap sec">
  <div class="sec-hd"><h2>あなたとの相性</h2><span class="en">Personal Fit</span>
  <p class="note">生年月日から九星気学の本命卦と四柱推命の命式を割り出し、この土地との相性をお伝えします。
    出生時刻を入れると精度が上がります。</p></div>
  <div class="form">
    <div class="fld"><label for="bd">生年月日</label><input type="date" id="bd" value="1990-05-12"></div>
    <div class="fld"><label for="tm">出生時刻（任意）</label><input type="time" id="tm" value="14:30"></div>
    <div class="fld"><label for="gd">性別</label><select id="gd"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="fld"><label>&nbsp;</label><button class="btn" id="run">診断する</button></div>
  </div>
  <div id="pout"></div>
</div>
"""
area_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
document.getElementById("illus").innerHTML=Illustrations.get("azabudai");
const s=Subjects.byId("bldg-azabudai-residence"),r=E.evaluate(s),f=E.deriveFortunes(r);
document.getElementById("out").innerHTML =
   R.fortuneRadar(f,E.averageFortunes(Subjects.wards),r.grade,r.label)
 + R.fortuneRows(f)
 + '<div class="sec"><div class="sec-hd"><h2>この土地の読み方</h2><span class="en">Reading</span></div></div>'
 + R.publicSummary(r);
document.getElementById("map").innerHTML=R.gmap("東京都港区麻布台1丁目","麻布台・六本木");

const HERE=Subjects.properties.filter(p=>p.town==="麻布台・六本木");
document.getElementById("props").innerHTML='<div class="alist">'+HERE.map((p,i)=>{
  const rr=E.evaluate(p),dir=E.helpers.dirOf(p.building.facing).n;
  return `<a class="aitem" href="#"><div class="t"><span class="n">${String(i+1).padStart(2,"0")}</span>
    <span class="nm">${p.name}</span><span class="ar">${rr.grade} ${rr.total}</span></div>
    <p>${p.price}　／　標高 ${p.terrain.elevation}m　／　${dir}向き　／　${p.building.builtYear}年竣工</p></a>`;
}).join("")+'</div>';

function personal(){
  const p=E.evaluatePersonal(s,{birth:document.getElementById("bd").value,
    time:document.getElementById("tm").value||null,gender:document.getElementById("gd").value,lng:139.6917});
  const c=E.combine(r,p);const k=p.kyusei,q=p.shichu.pillars;
  document.getElementById("pout").innerHTML=`
   <div class="comb"><span>この土地 <b>${c.baseTotal}</b></span>
     <span class="op">${c.adjust>=0?"+":""}${c.adjust}</span>
     <span>あなたとの相性込み <b class="big">${c.personalTotal}</b> <em>${c.grade}</em></span></div>
   <div class="frows">
     <div class="frow"><div class="fr-h"><span class="fr-n">九星気学</span>
       <span class="fr-s">${p.parts[0]?p.parts[0].score:"—"}</span></div>
       <div class="fr-l">${k.starName}／本命卦は${k.ka}（${k.groupJP}）。吉方位は${k.goodDirections.join("・")}。
       この土地は${E.helpers.dirOf(s.building.facing).n}向きです。</div></div>
     <div class="frow"><div class="fr-h"><span class="fr-n">四柱推命</span>
       <span class="fr-s">${p.parts[1]?p.parts[1].score:"—"}</span></div>
       <div class="fr-l">命式は ${q.year.stem}${q.year.branch}・${q.month.stem}${q.month.branch}・${q.day.stem}${q.day.branch}${q.hour?"・"+q.hour.stem+q.hour.branch:""}。
       日主は${p.shichu.dayMaster}（${p.shichu.dayElement}）の${p.shichu.strong?"身強":"身弱"}で、活かしたい五行は${p.shichu.yojin.join("・")}です。</div></div>
   </div>
   <p class="hl-note">相性は土地そのものの評価には含めていません。土地の評価は誰が見ても同じ値であるべきだからです。
     より詳しい鑑定はLINEからご相談ください。</p>`;
}
document.getElementById("run").addEventListener("click",personal);
</script>"""
open(f"{OUT}/area-azabudai.html","w",encoding="utf-8").write(
  page("麻布台・六本木の風水｜港区エリアガイド｜龍脈",
       "麻布台・六本木の風水を龍脈・標高・地歴から読み解きます。物件・地図・相性診断つき。",
       area_body, area_js))
print("area-azabudai.html")
