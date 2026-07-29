# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX, DIAGNOSIS
IMG = json.load(open("images.json", encoding="utf-8"))

# ══════════════════════════ 物件一覧
prop_body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>物件一覧</div>
<div class="wrap pg">
  <div class="eyebrow caps">Properties</div>
  <h1 class="pt">運の巡る、住まいたち</h1>
  <div class="pt-sub">条件だけでなく、土地の気まで見て選んだ物件</div>
  <p class="lead">龍脈・標高・地盤・地歴・方位を読み解いて選んだ住まいです。
    表示している点数は土地と建物そのものの見立てで、あなたの星との相性は含んでいません。
    相性まで含めた並びは、無料診断でご確認いただけます。</p>
  <div class="illus"><img src="{IMG['minato']}" alt="東京の街並み"></div>
</div>
<div class="sortbar" id="sortbar">
  <span class="lb">SORT</span>
  <button data-k="score" class="on">気の見立て ↓</button>
  <button data-k="elev">標高 ↓</button>
  <button data-k="year">築年 ↓</button>
</div>
<div class="wrap count" id="cnt">10 件を表示中</div>
<div id="list"></div>
<div class="wrap sec">
{LINEBOX}</div>
{DIAGNOSIS('物件')}"""

prop_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
const ST=["神谷町駅 徒歩2分","半蔵門駅 徒歩4分","白金高輪駅 徒歩5分","六本木駅 徒歩4分","大門駅 徒歩3分",
 "明治神宮前駅 徒歩7分","青山一丁目駅 徒歩6分","神谷町駅 徒歩6分","乃木坂駅 徒歩5分","六本木駅 徒歩8分"];
const P=Subjects.properties.map((p,i)=>({p,r:E.evaluate(p),st:ST[i],
  d:E.helpers.dirOf(p.building.facing).n}));
function draw(k){
  P.sort((a,b)=> k==="score" ? b.r.total-a.r.total
    : k==="elev" ? b.p.terrain.elevation-a.p.terrain.elevation
    : b.p.building.builtYear-a.p.building.builtYear);
  document.getElementById("list").innerHTML=P.map((o,i)=>`
   <a class="wrow" href="property-azabudai.html"><div class="in">
     <div class="h"><span class="rk">${String(i+1).padStart(2,"0")}</span>
       <span class="nm">${o.p.name}</span><span class="tg">${o.p.town}</span>
       <span class="tot"><i>${o.r.grade}</i><b>${o.r.total}</b></span></div>
     <div class="sgrid">
       <div class="sr"><span class="l">参考価格</span><span class="n">${o.p.price}</span></div>
       <div class="sr"><span class="l">最寄り</span><span class="n">${o.st}</span></div>
       <div class="sr"><span class="l">標高</span><span class="n">${o.p.terrain.elevation}m</span></div>
       <div class="sr"><span class="l">向き・築年</span><span class="n">${o.d}向き ／ ${o.p.building.builtYear}年</span></div>
     </div></div></a>`).join("");
}
document.querySelectorAll("#sortbar button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#sortbar button").forEach(x=>{x.classList.remove("on");
    x.textContent=x.textContent.replace(" ↓","");});
  b.classList.add("on");b.textContent+=" ↓";draw(b.dataset.k);}));
draw("score");
</script>"""
open(f"{OUT}/properties.html","w",encoding="utf-8").write(
  page("物件一覧｜運の巡る住まいたち｜スピ不動産",
       "龍脈・標高・地盤・地歴・方位から選んだ住まいの一覧です。", prop_body, prop_js))
print("properties.html")

# ══════════════════════════ コラム一覧
COLS = [
 ("引越し風水","2026.07.26","2026年 引越しに吉な月・方位まとめ【九星気学】",
  "九星気学では、動く月と方角で結果が変わるとされます。2026年の吉日と方位を命星別に整理しました。","meguro"),
 ("エリア風水","2026.07.24","麻布台ヒルズを風水で読む｜龍脈・気場・方位の完全分析",
  "標高30.4mの台地頂部。江戸城から伸びる龍脈の末端で、なぜ気が集まるのかを地形から読み解きます。","minato"),
 ("九星気学","2026.07.21","九星気学とは？命星の調べ方と住まい選びへの活かし方",
  "生まれ年から導く九つの星。名前は聞いたことがあっても、住まい選びにどう使うかは意外と知られていません。","setagaya"),
 ("地形検証","2026.07.18","「谷」がつく地名は、本当に低地なのか",
  "市ヶ谷・四谷・幡ヶ谷は標高30m超の台地上にあります。5つの地名を標高データで照合しました。","shibuya"),
 ("土地の記憶","2026.07.15","江戸切絵図で読む、あなたの街の来歴",
  "大名屋敷だったのか、町人地だったのか、湿地だったのか。300年前の用途が今の評価に効いています。","chiyoda"),
 ("防災","2026.07.11","浸水想定と風水の凶相は、どこまで一致するか",
  "古典が避けよと説く低地・旧河道・埋立地を、現行のハザードマップと重ねて検証しました。","tokyo"),
 ("元運","2026.07.08","八運から九運へ。2024年に入れ替わったもの",
  "2024年2月4日、三元九運は九運に入りました。離（南）の気が旺じる20年間の方位の変化を整理します。","kawasaki"),
 ("暮らしの工夫","2026.07.04","谷の土地でも大丈夫。家の中の気を整える5つの方法",
  "土地の弱さは、住まい方で半分以上補えると考えられてきました。今日からできる工夫をまとめます。","yokohama"),
]
rows = "".join(
 f'<a class="crow" href="#"><div class="ph" style="background-image:url({IMG[img]})"></div>'
 f'<div><span class="cat">{cat}</span><span class="dt" style="font-family:var(--lat);font-size:.82rem;'
 f'color:var(--ink-2);margin-left:.7rem">{d}</span><h4>{t}</h4>'
 f'<p style="font-size:.88rem;color:var(--ink-2);line-height:2.15;margin-top:.6rem">{ex}</p></div></a>'
 for cat, d, t, ex, img in COLS)

col_body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span>コラム</div>
<div class="wrap pg">
  <div class="eyebrow caps">Column</div>
  <h1 class="pt">風水をもっと知る</h1>
  <div class="pt-sub">土地の読み方を、公開データで検証する</div>
  <p class="lead">占いというより、昔の人が何百年もかけて見つけてきた土地の読み方です。
    地名の由来、標高、旧版地形図、ハザードマップ。使えるデータで確かめながら書いています。</p>
</div>
<div class="wrap sec" style="padding-top:1rem">
  <div style="border-top:1px solid var(--rule)">{rows}</div>
{LINEBOX}</div>
{DIAGNOSIS('住まい')}"""
open(f"{OUT}/columns.html","w",encoding="utf-8").write(
  page("風水コラム｜土地の読み方を公開データで検証｜スピ不動産",
       "地名の由来・標高・旧版地形図・ハザードマップから、土地の読み方を検証するコラムです。",
       col_body, ""))
print("columns.html")
