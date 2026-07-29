# -*- coding: utf-8 -*-
import json, subprocess
from common_v2 import *
from brand import LINEBOX, DIAGNOSIS
from ward_text import W
from spots_text import S
import json as _j
COLSLUG={c['ward']:c for c in _j.load(open('columns.json',encoding='utf-8')) if c['city']=='東京23区'}
import json as _json
BYW = _json.load(open('props_by_ward.json', encoding='utf-8'))

DATA = json.loads(subprocess.run(["node","-e","""
require('/mnt/user-data/outputs/fengshui-engine.js');
require('/mnt/user-data/outputs/subjects.js');
const E=FengshuiEngine;
console.log(JSON.stringify(Subjects.wards.map(w=>{const r=E.evaluate(w),f=E.deriveFortunes(r);
 return {id:w.id,en:w.en,name:w.name,total:r.total,grade:r.grade,
  f:f.map(x=>({l:x.label,s:x.score})),terrain:w.terrain,hist:w.history.formerUse,flood:w.environment.hazard.floodDepth,
  shrine:(w.environment.shrines[0]||{}), landslide:w.environment.hazard.landslide};})));
"""], capture_output=True, text=True).stdout)

RANK = sorted(DATA, key=lambda d: -d["total"])
FTOP = {k: max(DATA, key=lambda d: [x["s"] for x in d["f"] if x["l"]==k][0])["en"]
        for k in ["財運","仕事運","恋愛運","健康運"]}
VEIN = {"major":"大龍脈","middle":"中龍脈","minor":"小龍脈","none":"龍脈の外"}
LAND = {"plateau":"台地上","ridge":"尾根","slope":"斜面","plain":"平地","reclaimed":"埋立地"}

def cards(d):
    t, hist = d["terrain"], d["hist"]
    dv = t.get("dragonVein") or {}
    g, cont = VEIN.get(dv.get("grade"),"龍脈の外"), dv.get("continuity",0)
    src = dv.get("source") or "明確な主脈"
    ryu = (f"{src}を源とする{g}が区内を走ります。尾根線の連続性は{cont:.2f}で、"
      + ("気の通り道が途切れずに繋がっています。" if cont>=.8 else
         "おおむね繋がっていますが、途中に鞍部があります。" if cont>=.55 else
         "尾根が細かく分断され、気の流れは断続的です。")
      + ("台地の高まりがそのまま龍脈の道になっており、どの高台を選ぶかが評価を分けます。" if t["elevation"]>=20
         else "地形の起伏が乏しいぶん、龍脈より水系の巡りで気を読むことになります。"))
    chi = (f"平均標高{t['elevation']}m、地形分類は{LAND.get(t['landform'],'平地')}。周囲との比高は{t['relativeHeight']}m。"
      f"地盤は{t['ground']['classification']}で、液状化の可能性は「{t['ground']['liquefaction']}」区分です。"
      + ("洪水浸水想定は区域外か軽微で、地勢による減点はほとんどありません。" if d["flood"]<=.5
         else f"想定浸水深は{d['flood']}mで、低地側では階数と地盤資料の確認が前提になります。"))
    rek = f"江戸期の主用途は{hist}。" + {
      "大名屋敷":"台地の最も条件の良い区画が大名に割り当てられ、その格式が現在の地価にそのまま対応しています。",
      "武家屋敷":"武家地として選ばれた台地であり、地歴としては上位に位置します。",
      "寺社地":"寺社の境内地が広く、土地神の加護が長く続いた区画とされます。",
      "町人地":"商業と手工業が集積した町人地で、商いの気が何代にもわたり蓄積しています。",
      "田畑":"近世まで農地で、人の営みが穏やかに続いた土地です。急激な改変の履歴がありません。",
      "湿地":"近代まで居住に適さなかった土地で、地歴としては最も弱い分類にあたります。",
      "海・埋立":"近代以降の埋立地であり、地の気の蓄積は浅いと判断します。"}.get(hist,"")
    mizu = ("風水では、水は財を運び、山は人を養うとされます。"
      + (f"想定浸水深{d['flood']}mという数値が示すとおり、この区は水の影響を強く受ける低地です。"
         "水の気は濃いぶん財の巡りは速く、その反面で溜めにくい性質を持ちます。"
         if d["flood"] >= 2.0 else
         f"想定浸水深は{d['flood']}mで、水の力は穏やかに働きます。"
         "流れの速さより、水が土地を抱く形（環抱水）になっているかで評価が分かれます。"
         if d["flood"] >= 0.6 else
         "浸水想定はほぼ区域外で、水による減点は入りません。"
         "地表の川より、暗渠となった旧水路と崖線の湧水をどう読むかが要点になります。")
      + ("川のカーブでは、内側の区画が環抱水として加点、外側が反弓水として減点になります。"
         if t["landform"] in ("plain","reclaimed") else
         "崖線に沿う湧水は生気の湧く地点とされ、近接するほど評価が上がります。"))
    sh = d["shrine"]
    kiba = (f"区の主要鎮守は{sh.get('rank','村社')}格で、中心からおよそ{sh.get('distance',0)}mの位置にあります。"
      + {"官幣社":"最上位の社格を持ち、土地神の守りは都内でも最も強い部類です。",
         "府社":"高い社格を持ち、区全体の地運を支える拠り所になっています。",
         "郷社":"地域の要を押さえる社格で、周辺の地の気を安定させています。",
         "村社":"規模は大きくありませんが、土地神として長く祀られてきました。"}.get(sh.get("rank"),"")
      + ("加えて崩落の警戒区域を含むため、斜面地では地盤資料の確認が前提になります。"
         if d["landslide"] else
         "崩落の警戒区域は含まず、地盤面での不安要素は限定的です。"))
    return [("DRAGON VEIN","龍脈",ryu),("TOPOGRAPHY","地形",chi),("WATER","水気",mizu),
            ("HISTORY","歴史",rek),("QI FIELD","気場",kiba)]

for d in DATA:
    en, name = d["en"], d["name"]
    sub, desc, chips, areas = W[en]
    badge = next((f"{k} No.1" for k,v in FTOP.items() if v==en), f"総合 {RANK.index(d)+1}位 / 23区")
    fc = "".join(f'<article class="fcard"><div class="k">{k}</div><h3>{jp}</h3><hr><p>{t}</p></article>'
                 for k,jp,t in cards(d))
    ac = "".join(
      f'<a class="acard" href="{"area-azabudai.html" if a=="麻布台・六本木" else "areas.html"}">'
      f'<span class="wm">{gr}</span><div class="no">{i+1:02d}</div><h3>{a}</h3><hr><p>{ds}</p>'
      f'<div class="tot"><span class="l">Total</span><span class="g">{gr}</span>'
      f'<span class="s">{sc}</span><span class="ar">→</span></div></a>'
      for i,(a,ds,gr,sc) in enumerate(areas))
    sp = "".join(f'<div class="spot"><span class="n">{n}</span><span class="d">{loc}</span><p>{ds}</p></div>'
                  for n, loc, ds in S[en])
    wc = "".join(f'<a href="ward-{x["en"].lower()}.html">{x["name"]}</a>' for x in DATA if x["en"]!=en)

    body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水ガイド</a><span>/</span>{name}</div>
<div class="wrap pg">
  <div class="eyebrow">Ward Guide · {en}</div>
  <h1 class="pt">{name} <span style="font-size:.38em;color:var(--ink-2);letter-spacing:.06em">{badge}</span></h1>
  <div class="pt-sub">{sub}</div>
  <p class="lead">{desc}</p>
  <div class="chips">{"".join(f'<span class="chip">{c}</span>' for c in chips)}</div>
  <div id="panel"></div>
</div>
<div class="wrap sec"><div class="sec-hd"><h2>{name}の風水解説</h2><span class="en">Fengshui</span></div></div>
<div class="fcards">{fc}</div><div class="rail-hint">← スワイプで続きを読む</div>
<div class="wrap sec"><div class="sec-hd"><h2>{name}のエリアとスポット</h2><span class="en">{len(areas)} Areas</span>
  <p class="note">区の平均ではなく、町丁目まで下りると評価が変わります。</p></div></div>
<div class="rail">{ac}</div><div class="rail-hint">← スワイプで続きを見る</div>
<div class="wrap sec">
  <div class="sec-hd"><h2>{name}の開運スポット</h2><span class="en">Key Spots</span>
  <p class="note">気の集まる地点と、その理由。現地で確認できるものだけを挙げています。</p></div>
  <div class="spots">{sp}</div>
</div>
<div class="wrap sec"><div class="sec-hd"><h2>{name}の物件</h2><span class="en">Properties</span></div></div>
<div class="rail" id="prail"></div><div class="rail-hint">← スワイプで続きを見る</div>
<div class="wrap sec"><div class="center"><a class="obtn" href="properties.html">物件一覧をすべて見る →</a></div></div>
<div class="wrap sec">
  <div class="sec-hd"><h2>他エリアと比較する</h2><span class="en">Other Wards</span></div>
  <div class="wchips">{wc}</div>
</div>
{(lambda c: f"""<div class="wrap sec">
  <div class="sec-hd"><h2>{name}の風水コラム</h2><span class="en">Column</span></div>
  <a class="feat" href="{c['slug']}.html" style="grid-template-columns:1fr">
    <div class="rbd" style="padding:2rem 1.8rem">
      <div class="ren" style="color:var(--gold)">READ MORE</div>
      <h3 style="font-family:var(--min);font-weight:600;font-size:1.24rem;margin-top:.6rem;line-height:1.6">{c['title']}</h3>
      <hr style="border:none;border-top:1px solid var(--rule);margin:1.1rem 0">
      <p style="font-size:.92rem;color:var(--ink-2);line-height:2.3">{c['lead']}</p>
      <div class="rgo" style="color:var(--gold);margin-top:1.4rem"><span>記事を読む</span><span>→</span></div>
    </div></a>
</div>""" if c else "")(COLSLUG.get(name))}
<div class="wrap sec">{LINEBOX}</div>
{DIAGNOSIS(name)}"""

    plist = _json.dumps(BYW.get(name, []), ensure_ascii=False, separators=(",", ":"))
    js = f"""<script>
const E=FengshuiEngine,R=FengshuiRender;
const s=Subjects.byId("{d['id']}"),r=E.evaluate(s),f=E.deriveFortunes(r),AV=E.averageFortunes(Subjects.wards);
document.getElementById("panel").innerHTML=
  R.fortunePanel(r,f,AV,document.querySelector(".lead").textContent.trim(),"diagnosis.html");
const MYP={plist};
document.getElementById("prail").innerHTML= MYP.length ? MYP.map((x,i)=>`
 <a class="pcard" href="property.html?id=${{x.id}}"><span class="wm">${{x.total}}</span>
  <div class="top"><span class="no">${{String(i+1).padStart(2,"0")}}</span><span class="badge">売買</span></div>
  <div class="ar">${{x.ward}}</div><h3>${{x.name}}</h3><hr>
  <dl class="kv"><dt>売買</dt><dd>${{x.price}}</dd></dl>
  <div class="st">${{x.st}}駅 徒歩${{x.walk}}分　／　${{x.dir}}向き ／ ${{x.layout}} ${{x.area}}㎡</div>
  <div class="fs"><div class="l">気の見立て</div>
    <div class="row"><b>${{x.total}}</b><small>pt</small><span class="arw">→</span></div></div></a>`).join("")
  : '<div class="wrap" style="color:var(--ink-2);font-size:.9rem">この区の掲載物件は準備中です。</div>';
</script>"""
    open(f"{OUT}/ward-{en.lower()}.html","w",encoding="utf-8").write(
      page(f"{name}の風水｜{sub}｜スピ不動産",
           f"{name}の風水を龍脈・地形・地歴から読み解きます。{sub}。",
           body, js))
print("生成", len(DATA), "ページ")
