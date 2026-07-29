# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX as BRAND_LINEBOX, DIAGNOSIS as BRAND_DIAGNOSIS
from areas_data import MINATO_AREAS, MINATO_SPOTS, AZABUDAI_SPOTS
LINE = json.load(open("/home/claude/build/images.json", encoding="utf-8"))
illus = lambda k, a: f'<div class="illus"><img src="{LINE["tokyo"]}" alt="東京の街並み"></div>'

WARDS22 = ["千代田区","中央区","渋谷区","新宿区","文京区","目黒区","大田区","世田谷区","豊島区",
           "台東区","墨田区","品川区","江東区","中野区","杉並区","北区","江戸川区","板橋区",
           "荒川区","足立区","練馬区","葛飾区"]

def LINEBOX(*a):
    return BRAND_LINEBOX

def OTHERWARDS(cur):
    chips = "".join(f'<a href="#">{w}</a>' for w in WARDS22 if w != cur)
    return f'''<div class="wrap sec">
  <div class="sec-hd"><h2>他エリアと比較する</h2><span class="en">Other Wards</span></div>
  <div class="wchips">{chips}</div>
</div>'''

def DIAGNOSIS(sc):
    return BRAND_DIAGNOSIS(sc)

def SPOTS(title, items):
    rows = "".join(
      f'<div class="spot"><span class="n">{n}</span><span class="d">{d}</span><p>{p}</p></div>'
      for n, d, p in items)
    return f'''<div class="wrap sec">
  <div class="sec-hd"><h2>{title}</h2><span class="en">Key Spots</span>
  <p class="note">気の集まる地点と、その理由。現地で確認できるものだけを挙げています。</p></div>
  <div class="spots">{rows}</div>
</div>'''

def FCARDS(items):
    cards = "".join(
      f'<article class="fcard"><div class="k">{k}</div><h3>{jp}</h3><hr><p>{t}</p></article>'
      for k, jp, t in items)
    return f'<div class="fcards">{cards}</div><div class="rail-hint">← スワイプで続きを読む</div>'

# ═══════════════ 町エリアページ
AZ_FENG = [
 ("DRAGON VEIN","龍脈","六本木台地の最高点にあたり、皇居から南西へ伸びる支脈の末端で気が最も高密度に凝縮する。尾根線の連続性は0.95。東に皇居、南西に東京湾という配置が背山面水を高層から成立させ、財運・名声・健康の三方向を一点で受ける稀な条件が揃う。"),
 ("TOPOGRAPHY","地形","標高30.4m、台地頂部。周囲の古川低地との比高は26m以上あり、浸水想定区域には含まれない。前面道路はいずれも突き当たりを持たず、路冲・反弓水・天斬殺のいずれにも該当しない。幹線道路まで120mあり、近接による減点は最小限に留まる。"),
 ("HISTORY","歴史","江戸期は島津家・毛利家の上屋敷が置かれた格式地。明治以降は各国公使館が集積し、国際性の気が重なった。2023年の再開発で現代最大級の聚気点が生まれ、300年分の蓄積の上に新しい商業財気が載る構造になっている。"),
]
AZ_DESC = "麻布台・六本木は六本木台地の最高点にあたり、標高30.4m、周囲の低地との比高は26mあります。江戸城から南西へ伸びる龍脈の末端で、尾根の連なりは途切れがありません。東に皇居、南西に東京湾を望む背山面水の形が高層から成立する、区内で最も気の密度が高いエリアです。"

area_body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="areas.html">エリア風水ガイド</a><span>/</span><a href="ward-minato.html">港区</a><span>/</span>麻布台・六本木</div>
<div class="wrap pg">
  <div class="eyebrow">Area Guide · 港区</div>
  <h1 class="pt">麻布台・六本木</h1>
  <div class="pt-ward">港区</div>
  {illus('azabudai','麻布台・六本木の街並み')}
  <p class="lead">{AZ_DESC}</p>
  <div class="chips"><span class="chip">龍脈</span><span class="chip">龍穴</span>
    <span class="chip">尾根</span><span class="chip">大名屋敷</span><span class="chip">浸水想定外</span></div>
  <div id="panel"></div>
</div>

<div class="wrap sec"><div class="sec-hd"><h2>麻布台・六本木の風水解説</h2><span class="en">Fengshui</span></div></div>
{FCARDS(AZ_FENG)}

{SPOTS('麻布台・六本木の開運スポット', AZABUDAI_SPOTS)}
<div class="wrap sec"><div class="sec-hd"><h2>麻布台・六本木の物件</h2><span class="en">Properties</span></div></div>
<div class="rail" id="prail"></div>
<div class="rail-hint">← スワイプで続きを見る</div>
<div class="wrap sec"><div class="center"><a class="obtn" href="index.html#props">物件一覧をすべて見る →</a></div></div>

<div class="wrap sec">
  <div class="sec-hd"><h2>あなたとの相性</h2><span class="en">Personal Fit</span>
  <p class="note">生年月日から九星気学の本命卦と四柱推命の命式を割り出し、この土地との相性をお伝えします。</p></div>
  <div class="form">
    <div class="fld"><label for="bd">生年月日</label><input type="date" id="bd" value="1990-05-12"></div>
    <div class="fld"><label for="tm">出生時刻（任意）</label><input type="time" id="tm" value="14:30"></div>
    <div class="fld"><label for="gd">性別</label><select id="gd"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="fld"><label>&nbsp;</label><button class="btn" id="run">診断する</button></div>
  </div>
  <div id="pout"></div>
{LINEBOX('麻布台・六本木')}</div>
{DIAGNOSIS('麻布台・六本木')}
"""
area_js = """<script>
const E=FengshuiEngine,R=FengshuiRender;
const s=Subjects.byId("bldg-azabudai-residence"),r=E.evaluate(s),f=E.deriveFortunes(r),AV=E.averageFortunes(Subjects.wards);
document.getElementById("panel").innerHTML=
  R.fortunePanel(r,f,AV,document.querySelector(".lead").textContent.trim(),"#run");
const ST=["神谷町駅 徒歩2分","六本木駅 徒歩4分","乃木坂駅 徒歩5分","青山一丁目駅 徒歩6分"];
const P=Subjects.properties.filter(p=>["麻布台・六本木","赤坂・六本木","南青山・青山","赤坂・乃木坂"].includes(p.town));
document.getElementById("prail").innerHTML=P.map((p,i)=>{
  const rr=E.evaluate(p);
  return `<a class="pcard" href="property-azabudai.html"><span class="wm">${rr.total}</span>
   <div class="top"><span class="no">${String(i+1).padStart(2,"0")}</span><span class="badge">売買</span></div>
   <div class="ar">${p.town}</div><h3>${p.name}</h3><hr>
   <dl class="kv"><dt>売買</dt><dd>${p.price}</dd></dl>
   <div class="st">${ST[i%ST.length]}</div>
   <div class="fs"><div class="l">Feng Shui</div>
     <div class="row"><b>${rr.total}</b><small>pt</small><span class="arw">→</span></div></div></a>`;
}).join("");
function personal(){
  const p=E.evaluatePersonal(s,{birth:document.getElementById("bd").value,
    time:document.getElementById("tm").value||null,gender:document.getElementById("gd").value,lng:139.6917});
  const c=E.combine(r,p),k=p.kyusei,q=p.shichu.pillars;
  document.getElementById("pout").innerHTML=`
   <div class="comb"><span>この土地 <b>${c.baseTotal}</b></span>
     <span class="op">${c.adjust>=0?"+":""}${c.adjust}</span>
     <span>相性込み <b class="big">${c.personalTotal}</b> <em>${c.grade}</em></span></div>
   <div class="brk">
     <div class="brow"><div class="brow-h"><span class="bn">九星気学</span><span class="bv">${p.parts[0]?p.parts[0].score:"—"}</span></div>
       <p class="brk-note">${k.starName}／本命卦は${k.ka}（${k.groupJP}）。吉方位は${k.goodDirections.join("・")}。この土地は${E.helpers.dirOf(s.building.facing).n}向きです。</p></div>
     <div class="brow"><div class="brow-h"><span class="bn">四柱推命</span><span class="bv">${p.parts[1]?p.parts[1].score:"—"}</span></div>
       <p class="brk-note">命式は ${q.year.stem}${q.year.branch}・${q.month.stem}${q.month.branch}・${q.day.stem}${q.day.branch}${q.hour?"・"+q.hour.stem+q.hour.branch:""}。日主は${p.shichu.dayMaster}（${p.shichu.dayElement}）の${p.shichu.strong?"身強":"身弱"}で、活かしたい五行は${p.shichu.yojin.join("・")}です。</p></div>
   </div>`;
}
document.getElementById("run").addEventListener("click",personal);
</script>"""
open(f"{OUT}/area-azabudai.html","w",encoding="utf-8").write(
  page("麻布台・六本木の風水｜港区エリアガイド｜スピ不動産",
       "麻布台・六本木の風水を龍脈・標高・地歴から読み解きます。物件一覧と相性診断つき。",
       area_body, area_js))
print("area-azabudai.html")
