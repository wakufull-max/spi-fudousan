# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX
IMG = json.load(open("images.json", encoding="utf-8"))

body = f"""
<section class="dhero"><div class="wrap">
  <h1>吉方位の無料診断</h1>
  <div class="bar"></div>
  <p>あなたの星は、生まれた年で決まります。<br>
     昔の人が引っ越しの方角を気にしたのは、この星のこと。<br>
     どこが追い風で、どこが向かい風か。まずはそこからお伝えします。</p>
  <ul>
    <li><i>✓</i>あなたの命星と、追い風になる方位</li>
    <li><i>✓</i>財運・仕事運・恋愛運・健康運・安定運の巡り</li>
    <li><i>✓</i>星に合う東京のエリアと、実際の物件</li>
  </ul>
  <p class="fn">5つの質問に答えるだけ。1分ほどで終わります。</p>
</div></section>

<section class="wiz" id="wiz"><div class="wrap">
  <div class="prog"><span id="pstep">STEP 1 / 5</span><span id="ppct">20%</span></div>
  <div class="pbar"><i id="pfill" style="width:20%"></i></div>
  <div class="qcard" id="q"></div>
  <a class="wback" id="back" href="#" style="display:none">← 前の質問に戻る</a>
</div></section>

<div id="result" style="display:none">
  <section class="rhero"><div class="bgimg" style="background-image:url({IMG['setagaya']})"></div>
    <div class="in wrap">
      <div class="k">あなたの星は</div>
      <div class="star" id="rStar">—</div>
      <div class="bar"></div>
      <div class="meta" id="rMeta">—</div>
    </div></section>

  <div class="wrap" style="padding-top:clamp(2rem,7vw,3rem)">
    <div class="share">
      <a href="#" id="shX">𝕏　結果をシェア</a>
      <a href="#" id="shT">＠　Threadsでシェア</a>
    </div>
  </div>

  <div class="wrap sec">
    <div class="sec-hd"><h2>五つの運気の巡り</h2><span class="en">Fortune Balance</span></div>
    <div class="fscore" id="fscore"></div>
    <p class="note">※ 点数は命星の性質と入力内容から出した目安です。土地そのものの評価とは別の指標で、当たり外れを保証するものではありません。</p>
    <div class="compass" id="compass"></div>
  </div>

  <div class="wrap sec"><div class="sec-hd"><h2 id="areaTitle">相性のよいエリア</h2><span class="en">Areas For You</span></div></div>
  <div class="rail" id="arail"></div><div class="rail-hint">← スワイプで続きを見る</div>

  <div class="wrap sec" style="padding-top:2rem">{LINEBOX}</div>

  <div class="wrap sec"><div class="sec-hd"><h2>星に合う住まい</h2><span class="en">Homes For You</span></div></div>
  <div class="rail" id="prail"></div><div class="rail-hint">← スワイプで続きを見る</div>
  <div class="wrap sec" style="padding-top:0"><div class="center"><a class="obtn" href="properties.html">全物件を見る →</a></div></div>

  <div class="wrap sec">
    <div class="snat" id="snat"></div>
    <div class="snat" id="advice"></div>
    <div class="snat" id="work"></div>
    <div class="snat" id="family"></div>
  </div>

  <div class="wrap sec">
    <div class="sec-hd"><h2>土地そのものを読む</h2><span class="en">Column</span>
      <p class="note">ここまでは、あなたの星から見た相性でした。
        土地の側の話、つまり地形・水系・地歴については、生年月日を使わない別の記事にまとめています。
        両方を重ねると、判断の精度が上がります。</p></div>
    <div id="cols"></div>
    <div class="center"><a class="obtn" href="columns.html">コラム一覧を見る →</a></div>
  </div>
</div>"""

IMGL = {k: IMG[k] for k in ["minato","meguro","setagaya"]}
TOPREAL = json.load(open("diag_props.json", encoding="utf-8"))
js = ("<script>const IMG_LOCAL=" + json.dumps(IMGL, ensure_ascii=False)
      + ";\nconst REALP=" + json.dumps(TOPREAL, ensure_ascii=False, separators=(",",":"))
      + ";</script>\n<script>") + """
const E=FengshuiEngine;
const STARS={
 1:{n:"一白水星",el:"水行",dir:"北",avoid:"南（対冲）",
   nat:"柔軟・思慮深さ・人脈の星。水のように形を変えながら、人と人のあいだを流れて縁を運ぶ。表に立つより、要所を押さえて動かす力に長ける。",
   tags:["柔軟性","深い洞察","人脈をつなぐ力"],base:[76,74,84,72,70]},
 2:{n:"二黒土星",el:"土行",dir:"南西",avoid:"北東（鬼門）",
   nat:"育成・堅実・母性の星。大地のように受けとめ、時間をかけて確かなものを積み上げる。派手さより継続で結果を出す。",
   tags:["堅実さ","面倒見の良さ","継続する力"],base:[78,76,72,80,86]},
 3:{n:"三碧木星",el:"木行",dir:"東",avoid:"西（対冲）",
   nat:"行動・挑戦・突破力の星。若木が伸びるように、思い立ったらまず動く。発信と初動の速さが道をひらく。",
   tags:["行動力","発信する力","若さと勢い"],base:[74,86,78,84,70]},
 4:{n:"四緑木星",el:"木行",dir:"南東",avoid:"北西（対冲）",
   nat:"調和・信頼・縁の星。風が四方へ渡るように、人と情報を運び、信頼で結びつける。整った関係のなかで力を発揮する。",
   tags:["社交性","厚い信頼","良縁を引く力"],base:[76,78,88,78,76]},
 5:{n:"五黄土星",el:"土行",dir:"中宮（定位なし）",avoid:"鬼門・裏鬼門",
   nat:"カリスマ・支配力・強烈な個性の星。中心に位置する最強の星で、その人の周囲に強い影響を与える。良くも悪くも動かす力が大きい。",
   tags:["カリスマ性","強いリーダーシップ","変革する力"],base:[90,84,70,76,75]},
 6:{n:"六白金星",el:"金行",dir:"北西",avoid:"南東（対冲）",
   nat:"主導・完璧・天の星。高いところから全体を見わたし、筋を通して統べる。責任を引き受けるほど運が開く。",
   tags:["統率力","強い責任感","向上心"],base:[86,90,68,74,78]},
 7:{n:"七赤金星",el:"金行",dir:"西",avoid:"東（対冲）",
   nat:"喜び・弁舌・実りの星。人を楽しませ、場を和ませながら、自然と実利を引き寄せる。愛嬌が資産になる。",
   tags:["社交性","愛嬌","金運の強さ"],base:[88,76,86,72,70]},
 8:{n:"八白土星",el:"土行",dir:"北東",avoid:"南西（裏鬼門）",
   nat:"変革・継承・山の星。動かざること山のごとく、しかし変わるときは一気に変わる。受け継ぎ、次へ渡す役割を担う。",
   tags:["忍耐力","蓄積する力","転換の才"],base:[80,80,70,78,84]},
 9:{n:"九紫火星",el:"火行",dir:"南",avoid:"北（対冲）",
   nat:"情熱・名誉・美の星。火のように明るく照らし、見抜き、名を高める。表舞台で輝くほど本領を発揮する。",
   tags:["鋭い直感","美意識","名誉運"],base:[78,88,82,70,68]}};
const FL=[{k:"wealth",n:"財運",en:"Wealth",d:"お金の流れや稼ぐ力を示します"},
 {k:"career",n:"仕事運",en:"Career",d:"仕事での成果やキャリアを示します"},
 {k:"romance",n:"恋愛運",en:"Romance",d:"恋愛や人間関係の運勢を示します"},
 {k:"vitality",n:"健康運",en:"Vitality",d:"心身の健康状態や活力を示します"},
 {k:"stability",n:"安定運",en:"Stability",d:"生活の安定・精神的な安心感を示します"}];
const POOL=[
 ["千鳥ヶ淵・半蔵門","北","皇居の霊気と千鳥ヶ淵の水気。都内唯一「天の気」が下りる格別の地。","SS",97,"ward-chiyoda.html"],
 ["神楽坂・飯田橋","北","坂と路地が気を留める。文化と縁の蓄積が厚い一帯。","A",81,"ward-shinjuku.html"],
 ["日本橋・室町","北東","五街道の起点。江戸四百年の商業蓄積が生きる金の気の聖地。","A",83,"ward-chuo.html"],
 ["上野・谷中","北東","寛永寺と上野台。寺社の気が厚く、蓄積と継承に向く。","B+",78,"ward-taito.html"],
 ["麻布台・六本木","南東","六本木台地の頂部。標高30m超の高台に大龍脈が通る。","A+",86,"ward-minato.html"],
 ["南青山","南東","明治神宮の社叢から続く緑の帯。縁と感性の気が層を成す。","A",82,"ward-minato.html"],
 ["虎ノ門・愛宕","南","愛宕山という独立丘。周囲より20m以上高い龍穴の地。","B+",77,"ward-minato.html"],
 ["中目黒・青葉台","南","目黒川の水気と台地の対比。感性と変化の気が強い。","B+",78,"ward-meguro.html"],
 ["白金・白金台","南西","目黒台の丘陵に載る住宅地。自然教育園の緑が気を留める。","B+",76,"ward-minato.html"],
 ["赤坂・乃木坂","南西","台地の縁と谷が交互に走る。日枝神社が地運を支える。","B+",74,"ward-minato.html"],
 ["代官山・恵比寿","西","丘陵の起伏と緑。感性と社交の気が巡る。","A",81,"ward-shibuya.html"],
 ["広尾","西","有栖川宮記念公園の湧水と起伏。落ち着いた気の帯。","A",82,"ward-shibuya.html"],
 ["九段下・北の丸","北西","江戸城北の丸に接する武家地。格式と統率の気。","A",84,"ward-chiyoda.html"],
 ["市ヶ谷・四谷","北西","標高30m超の台地。地名に反して高燥で安定する。","B+",79,"ward-shinjuku.html"]];

function getsumei(y,m,d){
  const p=`${y}-${String(m).padStart(2,"0")}-${String(d).padStart(2,"0")}`;
  const sc=E.calendar.fourPillars(p,null,139.6917);
  const yb=sc.pillars.year.branch, mb=sc.pillars.month.branch;
  const B=["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"];
  const base=["子","午","卯","酉"].includes(yb)?8:["丑","辰","未","戌"].includes(yb)?5:2;
  let st=base-((B.indexOf(mb)-2+12)%12);
  while(st<1) st+=9; while(st>9) st-=9; return st;
}

const A={}; let step=1;
const YEARS=(()=>{const a=[];for(let y=2012;y>=1935;y--)a.push(y);return a;})();
const Q=[
 {t:"生まれ年を選んでください",s:"九星気学では生まれ年から命星が算出されます",key:"y",
  r:()=>`<select class="qsel" id="in"><option value="">選択してください</option>${YEARS.map(y=>`<option value="${y}">${y}年</option>`).join("")}</select>`,
  get:()=>+document.getElementById("in").value||0},
 {t:"生まれ月を選んでください",s:"月命星（補助星）の算出に使います",key:"m",
  r:()=>`<div class="ogrid c4">${[...Array(12)].map((_,i)=>`<button data-v="${i+1}">${i+1}月</button>`).join("")}</div>`},
 {t:"生まれ日を選んでください",s:"立春・節入りの境界を正しく判定するために使います",key:"d",
  r:()=>`<select class="qsel" id="in"><option value="">選択してください</option>${[...Array(31)].map((_,i)=>`<option value="${i+1}">${i+1}日</option>`).join("")}</select>`,
  get:()=>+document.getElementById("in").value||0},
 {t:"性別を選んでください",s:"八宅法では本命卦が性別で分かれます",key:"g",
  r:()=>`<div class="ogrid">${[["m","男性"],["f","女性"]].map(o=>`<button data-v="${o[0]}">${o[1]}</button>`).join("")}</div>`},
 {t:"いちばん高めたい運気は？",s:"おすすめエリアと物件の並びに反映します",key:"p",
  r:()=>`<div class="ogrid c4">${FL.slice(0,4).map(f=>`<button data-v="${f.k}">${f.n}</button>`).join("")}</div>`}];

function paint(){
  const q=Q[step-1];
  document.getElementById("pstep").textContent=`STEP ${step} / 5`;
  document.getElementById("ppct").textContent=`${step*20}%`;
  document.getElementById("pfill").style.width=`${step*20}%`;
  document.getElementById("q").innerHTML=`<h2>${q.t}</h2><div class="sub">${q.s}</div>${q.r()}`;
  document.getElementById("back").style.display=step>1?"block":"none";
  const sel=document.getElementById("in");
  if(sel){ if(A[q.key]) sel.value=A[q.key];
    sel.addEventListener("change",()=>{const v=q.get(); if(v){A[q.key]=v; next();}}); }
  document.querySelectorAll("#q .ogrid button").forEach(b=>{
    if(String(A[q.key])===b.dataset.v) b.classList.add("on");
    b.addEventListener("click",()=>{A[q.key]=isNaN(+b.dataset.v)?b.dataset.v:+b.dataset.v; next();});});
}
function next(){ if(step<5){step++;paint();
    window.scrollTo({top:document.getElementById("wiz").offsetTop-70,behavior:"smooth"});} else show(); }
document.getElementById("back").addEventListener("click",e=>{e.preventDefault(); if(step>1){step--;paint();}});
paint();

function show(){
  const date=`${A.y}-${String(A.m).padStart(2,"0")}-${String(A.d).padStart(2,"0")}`;
  const ky=E.calendar.kyusei(date,A.g);
  const st=ky.star, S=STARS[st], gm=getsumei(A.y,A.m,A.d), GS=STARS[gm];
  document.querySelector(".dhero").style.display="none";
  document.getElementById("wiz").style.display="none";
  document.getElementById("result").style.display="block";
  document.getElementById("rStar").textContent=S.n;
  document.getElementById("rMeta").textContent=`${S.el}・定位：${S.dir}`;

  const sc=S.base.map((v,i)=>{let x=v; if(FL[i].k===A.p) x+=4; if(gm===st) x+=2;
    return Math.max(40,Math.min(99,x));});
  const tot=Math.round(sc.reduce((a,b)=>a+b,0)/sc.length);
  const star5=n=>{const q=n>=90?5:n>=80?4:n>=70?3:n>=60?2:1;return "★".repeat(q)+`<i>${"★".repeat(5-q)}</i>`;};
  const lb=n=>n>=88?"非常に良い":n>=78?"良い":n>=70?"普通":n>=60?"やや低め":"低め";
  document.getElementById("fscore").innerHTML=
   `<div class="fs-top"><span class="fs-g">${E.gradeOf(tot)}</span>
     <span class="fs-n">${tot}<small>点</small></span><span class="fs-pill">${lb(tot)}</span></div>`
   + FL.map((f,i)=>`<div class="frow2">
       <div class="nm">${f.n}<em>${f.en}</em></div>
       <div class="rt"><span class="stars">${star5(sc[i])}</span>
         <span class="pt">${sc[i]}<small>点</small></span><br>
         <span class="tg${sc[i]>=88?" hi":""}">${lb(sc[i])}</span></div>
       <div class="ds">${f.d}</div></div>`).join("");

  document.getElementById("compass").innerHTML=
   `<h3>あなたの星と、方位</h3><div class="en">Star &amp; Compass</div>
    <div class="cgrid">
      <div><div class="lb">年命星（主星）</div><div class="vl">${S.n}</div></div>
      <div><div class="lb">月命星（補助星）</div><div class="vl">${GS.n}</div>
        <div class="ds">${GS.tags.join("・")}</div></div>
      <div><div class="lb">定位（本命星の座）</div><div class="vl sm">${S.dir}</div>
        <div class="ds">九星気学で本命星が納まる方位</div></div>
      <div><div class="lb">四吉方（八宅）</div><div class="vl sm">${(ky.goodDirections||[]).join("・")||"—"}</div>
        <div class="ds">本命卦は${ky.ka}（${ky.groupJP}）</div></div>
    </div>
    <p class="note" style="margin-top:1.2rem">※ 九星気学では毎年の盤によって五黄殺・暗剣殺・歳破などの凶方が変わります。
       ここに示しているのは年によって動かない定位と、八宅法による四吉方です。
       引っ越しの方位取りは、その年の盤を見て個別に判断する必要があります。</p>`;

  document.getElementById("areaTitle").textContent=`${S.n}と相性のよいエリア`;
  let areas = S.dir.startsWith("中宮") ? POOL.slice().sort((a,b)=>b[4]-a[4])
    : POOL.filter(p=>p[1]===S.dir).concat(POOL.filter(p=>p[1]!==S.dir).sort((a,b)=>b[4]-a[4]));
  document.getElementById("arail").innerHTML=areas.slice(0,5).map((a,i)=>`
   <a class="acard" href="${a[5]}"><span class="wm">${a[3]}</span>
    <div class="no">${String(i+1).padStart(2,"0")}</div><h3>${a[0]}</h3><hr><p>${a[2]}</p>
    <div class="tot"><span class="l">Total</span><span class="g">${a[3]}</span>
      <span class="s">${a[4]}</span><span class="ar">→</span></div></a>`).join("");

  const good=ky.goodDirections||[];
  const props=REALP.map(p=>({p,fit:good.includes(p.dir)}))
    .sort((a,b)=>(b.fit-a.fit)||b.p.total-a.p.total).slice(0,6);
  document.getElementById("prail").innerHTML=props.map((o,i)=>`
   <a class="pcard" href="property.html?id=${o.p.id}"><span class="wm">${o.p.total}</span>
    <div class="top"><span class="no">${String(i+1).padStart(2,"0")}</span><span class="badge">売買</span></div>
    <div class="ar">${o.p.ward}</div><h3>${o.p.name}</h3><hr>
    <dl class="kv"><dt>売買</dt><dd>${o.p.price}</dd></dl>
    <div class="st">${o.p.st}駅 徒歩${o.p.walk}分　／　${o.p.dir}向き${o.fit?"（あなたの四吉方）":""}</div>
    <div class="st">${o.p.layout}／${o.p.area}㎡　${o.p.builtLabel}築</div>
    <div class="fs"><div class="l">気の見立て</div>
      <div class="row"><b>${o.p.total}</b><small>pt</small><span class="arw">→</span></div></div></a>`).join("");

  document.getElementById("snat").innerHTML=
   `<h3>命星の特性</h3><div class="en">Star Nature</div><p>${S.nat}</p>
    <div class="pills">${S.tags.map(t=>`<span>${t}</span>`).join("")}</div>`;
  document.getElementById("advice").innerHTML=
   `<h3>これからの動き方</h3><div class="en">Advice</div>
    <p>命星の吉方位（${S.dir}）、月命星${GS.n}の補助、そして土地そのものの気。この三つを重ねて判断すると、運気の取りこぼしが減ります。
    ${S.dir.startsWith("中宮")?"五黄土星は中宮に納まり定位を持たないため、八宅では男性が坤（南西）、女性が艮（北東）を代用します。方位より土地そのものの格を優先して選ぶのが実務的です。"
      :`まずは八宅の四吉方にあたるエリアから当たり、定位の対冲（${S.avoid}）は優先度を下げてください。`}</p>`;
  const wm={"金行":"西・北西向きの物件が金の気を強め、財運を支えます。","木行":"東・南東向きの物件が活性気を招き、仕事運・財運を高めます。",
   "水行":"北向き・水辺に近い物件が流れを生み、人脈から仕事につながります。","火行":"南向きの物件が名声の気を強め、表に立つ仕事を後押しします。",
   "土行":"高台・台地の物件が安定した財を育てます。低地より標高を優先してください。"}[S.el];
  document.getElementById("work").innerHTML=
   `<h3>仕事と財を後押しする住まい</h3><div class="en">Work &amp; Money</div>
    <p>${wm}高層階から見渡しの利く物件は視野を広げ、判断の精度を上げるとされます。玄関は明るく保ち、
    ${S.dir.startsWith("中宮")?"家の中心":S.dir}にあたる部屋を仕事場にすると気が乗ります。</p>`;
  document.getElementById("family").innerHTML=
   `<h3>暮らし方に合わせて</h3><div class="en">Living Style</div>
    <p>一人暮らしなら、気が凝縮しやすいコンパクトな間取りが向きます。玄関・寝室・仕事スペースの方位をそれぞれ整えると、
    生活のすべての面で効果が出やすくなります。ご家族なら、リビングを家の中心近くに置き、
    ${S.dir.startsWith("中宮")?"四方に均等に":"四吉方側に"}開口を取る間取りが理想です。</p>`;

  const COLS=[["エリア風水","麻布台ヒルズを風水で読む｜龍脈・気場・方位の完全分析","minato"],
    ["引越し風水","2026年 引越しに吉な月・方位まとめ【九星気学】","meguro"],
    ["九星気学","九星気学とは？命星の調べ方と住まい選びへの活かし方","setagaya"]];
  document.getElementById("cols").innerHTML=COLS.map(c=>`
   <a class="crow" href="columns.html"><div class="ph" style="background-image:url(${IMG_LOCAL[c[2]]})"></div>
    <div><span class="cat">${c[0]}</span><h4>${c[1]}</h4></div></a>`).join("");

  const txt=encodeURIComponent(`私の命星は${S.n}でした。定位は${S.dir}。#スピ不動産`);
  document.getElementById("shX").href=`https://twitter.com/intent/tweet?text=${txt}`;
  document.getElementById("shT").href=`https://www.threads.net/intent/post?text=${txt}`;
  window.scrollTo({top:0,behavior:"smooth"});
}
</script>"""

open(f"{OUT}/diagnosis.html","w",encoding="utf-8").write(
  page("吉方位の無料診断｜あなたの星と相性のよいエリア｜スピ不動産",
       "生まれた年から命星と本命卦を割り出し、追い風になる方位と相性のよいエリア・物件を無料でお伝えします。",
       body, js))
print("diagnosis.html")
