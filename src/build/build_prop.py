# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX as BRAND_LINEBOX, DIAGNOSIS as BRAND_DIAGNOSIS
from areas_data import AZABUDAI_SPOTS
LINE = json.load(open("images.json", encoding="utf-8"))
LINEBOX = BRAND_LINEBOX
DIAGNOSIS = BRAND_DIAGNOSIS('この物件')
illus = lambda k,a: f'<div class="illus"><img src="{LINE["tokyo"]}" alt="東京の街並み"></div>'





PR = [("DRAGON VEIN","龍脈","六本木台地の頂部に建ち、皇居から南西へ伸びる支脈の末端に位置します。尾根線の連続性0.95は都内でも最上位。高層階では東に皇居、南西に東京湾を同時に望み、背山面水の形が空中で成立します。台地の頂点で気が留まる龍穴の条件も満たしており、地形と方位の両面で加点が重なる稀な立地です。"),
      ("FACING","坐向","正面方位138°（南東向き）。二十四山では乾山巽向にあたり、朝日を受けて日中の採光が長く続く向きです。ただし2024年から始まった九運では当令が九紫＝離＝南にあたるため、南東は旺気ではなく平気の扱いになります。元運の適合は中位で、この物件の評価は方位ではなく地形と地歴が支えています。兼向（二十四山の境界±4.5°）にはかかっておらず、方位の判定自体は明確に確定します。"),
      ("SITE","敷地","前面道路は幅員11mで突き当たりを持たないため、形殺のなかで最も減点幅の大きい路冲に該当しません。カーブ外側でもなく反弓水の減点もなし。幹線道路まで120m、高架構造物まで640mと、いずれも影響が及ぶ距離ではありません。地盤は関東ローム層の台地で液状化可能性は低区分です。")]

fcards = "".join(f'<article class="fcard"><div class="k">{k}</div><h3>{jp}</h3><hr><p>{t}</p></article>' for k,jp,t in PR)
spots  = "".join(f'<div class="spot"><span class="n">{n}</span><span class="d">{d}</span><p>{p}</p></div>' for n,d,p in AZABUDAI_SPOTS)

body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水</a><span>/</span><a href="ward-minato.html">港区</a><span>/</span><a href="area-azabudai.html">麻布台・六本木</a><span>/</span>物件</div>
<div class="wrap pg">
  <div class="eyebrow">Property · 港区 麻布台・六本木</div>
  <h1 class="pt" id="pname">—</h1><div class="pt-ward" id="pvein">—</div>
  {illus('azabudai','麻布台・六本木の街並み')}
  <div class="pill-row" id="pills"></div>
  <div class="spec" id="spec"></div>
  <div id="panel"></div>
</div>
<div class="wrap sec"><div class="sec-hd"><h2>この物件の風水解説</h2><span class="en">Fengshui</span></div></div>
<div class="fcards">{fcards}</div><div class="rail-hint">← スワイプで続きを読む</div>
<div class="wrap sec">
  <div class="sec-hd"><h2>周辺の開運スポット</h2><span class="en">Key Spots</span>
  <p class="note">気の集まる地点と、その理由。現地で確認できるものだけを挙げています。</p></div>
  <div class="spots">{spots}</div>
</div>
<div class="wrap sec"><div class="sec-hd"><h2>この物件の位置</h2><span class="en">Map</span></div><div id="map"></div></div>
<div class="wrap sec"><div class="sec-hd"><h2>近隣の物件</h2><span class="en">Nearby Properties</span></div></div>
<div class="rail" id="prail"></div><div class="rail-hint">← スワイプで続きを見る</div>
<div class="wrap sec">
  <div class="sec-hd"><h2>あなたとの相性</h2><span class="en">Personal Fit</span></div>
  <div class="form">
    <div class="fld"><label for="bd">生年月日</label><input type="date" id="bd" value="1990-05-12"></div>
    <div class="fld"><label for="tm">出生時刻（任意）</label><input type="time" id="tm" value="14:30"></div>
    <div class="fld"><label for="gd">性別</label><select id="gd"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="fld"><label>&nbsp;</label><button class="btn" id="run">診断する</button></div>
  </div><div id="pout"></div>
{LINEBOX}</div>
{DIAGNOSIS}"""

js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
const s=Subjects.byId("prop-1"),r=E.evaluate(s),f=E.deriveFortunes(r),AV=E.averageFortunes(Subjects.wards);
const dir=E.helpers.dirOf(s.building.facing);
const sj=E.helpers.sanjuOf(s.building.facing), sit=E.helpers.sanjuOf(s.building.facing+180);
document.getElementById("pname").textContent=s.name;
document.getElementById("pvein").textContent=s.town+"／"+s.ward;
document.getElementById("pills").innerHTML=["龍脈","龍穴","台地","大名屋敷",dir.n+"向き","浸水想定外"]
  .map(t=>`<span class="pill-k">${t}</span>`).join("");
document.getElementById("spec").innerHTML=`<dl>
  <dt>参考価格</dt><dd>${s.price}</dd>
  <dt>所在</dt><dd>${s.ward} ${s.town}</dd>
  <dt>標高</dt><dd>${s.terrain.elevation}m ／ 周囲との比高 ${s.terrain.relativeHeight}m</dd>
  <dt>坐向</dt><dd>${s.building.facing}°（${dir.n}向き）／ ${sit.name}山 ${sj.name}向</dd>
  <dt>竣工</dt><dd>${s.building.builtYear}年（築${2026-s.building.builtYear}年）</dd>
  <dt>地盤</dt><dd>${s.terrain.ground.classification} ／ 液状化 ${s.terrain.ground.liquefaction}</dd>
  <dt>前面道路</dt><dd>幅員 ${s.environment.roads.frontWidth}m ／ 幹線まで ${s.environment.roads.arterialDistance}m</dd>
</dl>`;
document.getElementById("panel").innerHTML=
  R.fortunePanel(r,f,AV,"標高30.4mの台地頂部に建つ、区内で最も気の密度が高い立地です。前面道路に突き当たりがなく形殺の減点もありません。南東向きは九運では平気にあたり、方位よりも地形と地歴が評価を支えています。","#run");
document.getElementById("map").innerHTML=R.gmap("東京都港区麻布台1丁目 麻布台ヒルズ",s.name);
const ST=["神谷町駅 徒歩2分","六本木駅 徒歩4分","乃木坂駅 徒歩5分","青山一丁目駅 徒歩6分","白金高輪駅 徒歩5分","半蔵門駅 徒歩4分"];
document.getElementById("prail").innerHTML=Subjects.properties.filter(p=>p.id!=="prop-1").slice(0,6).map((p,i)=>{
  const rr=E.evaluate(p);
  return `<a class="pcard" href="#"><span class="wm">${rr.total}</span>
   <div class="top"><span class="no">${String(i+1).padStart(2,"0")}</span><span class="badge">売買</span></div>
   <div class="ar">${p.town}</div><h3>${p.name}</h3><hr>
   <dl class="kv"><dt>売買</dt><dd>${p.price}</dd></dl>
   <div class="st">${ST[i%ST.length]}</div>
   <div class="fs"><div class="l">Feng Shui</div>
     <div class="row"><b>${rr.total}</b><small>pt</small><span class="arw">→</span></div></div></a>`;
}).join("");
document.getElementById("run").addEventListener("click",function(){
  const p=E.evaluatePersonal(s,{birth:document.getElementById("bd").value,
    time:document.getElementById("tm").value||null,gender:document.getElementById("gd").value,lng:139.6917});
  const c=E.combine(r,p),k=p.kyusei,q=p.shichu.pillars;
  document.getElementById("pout").innerHTML=`
   <div class="comb"><span>この物件 <b>${c.baseTotal}</b></span>
     <span class="op">${c.adjust>=0?"+":""}${c.adjust}</span>
     <span>相性込み <b class="big">${c.personalTotal}</b> <em>${c.grade}</em></span></div>
   <div class="brk">
     <div class="brow"><div class="brow-h"><span class="bn">九星気学</span><span class="bv">${p.parts[0]?p.parts[0].score:"—"}</span></div>
       <p class="brk-note">${k.starName}／本命卦は${k.ka}（${k.groupJP}）。吉方位は${k.goodDirections.join("・")}。この物件は${dir.n}向きです。</p></div>
     <div class="brow"><div class="brow-h"><span class="bn">四柱推命</span><span class="bv">${p.parts[1]?p.parts[1].score:"—"}</span></div>
       <p class="brk-note">命式は ${q.year.stem}${q.year.branch}・${q.month.stem}${q.month.branch}・${q.day.stem}${q.day.branch}${q.hour?"・"+q.hour.stem+q.hour.branch:""}。日主は${p.shichu.dayMaster}（${p.shichu.dayElement}）の${p.shichu.strong?"身強":"身弱"}で、活かしたい五行は${p.shichu.yojin.join("・")}です。</p></div>
   </div>`;
});
</script>"""
open(f"{OUT}/property-azabudai.html","w",encoding="utf-8").write(
  page("麻布台ヒルズ 上層レジデンス｜物件の風水｜スピ不動産",
       "標高30.4m・尾根・南東向き。物件単位の風水スコアと地図、開運スポット、相性診断。", body, js))
print("property-azabudai.html")
