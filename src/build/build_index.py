# -*- coding: utf-8 -*-
import json
from common_v2 import *
from brand import LINEBOX, FAQ
LINE = json.load(open("lineart.json", encoding="utf-8"))
SHARED = LINE["tokyo"]        # 全ページ共通の1枚

faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)

body = f"""
<section class="hero"><div class="wrap">
  <div class="eyebrow">四柱推命 × 九星気学 × 不動産</div>
  <h1>ことを成す人は、<br>家を「星」で選ぶ。</h1>
  <p class="lead">家を買うのは、人生でいちばん大きな買い物。条件や価格だけでは、なかなか決めきれないものです。
    今が買い時か、この街でいいか、あなたと相性のいい家はどれか。
    私たちは、あなたの生まれ持った星から、ご縁のある一軒と、買うのに良い時期を見立てる不動産屋です。</p>
  <div class="acts">
    <a class="hbtn line" href="#line"><span class="badge">LINE</span>吉方位を無料診断</a>
    <a class="hbtn ghost" href="#props">住まいを見る</a>
  </div>
  <p class="hnote">完全無料／勧誘なし／あなたがやるのは、生年月日を送る30秒だけ。</p>
  <div class="illus"><img src="{SHARED}" alt="東京の街並み"></div>
</div></section>

<section class="sec"><div class="wrap read">
  <h2>土地の神様。</h2>
  <p class="big">あなたは、家に「相性」があると思いますか？</p>
  <p>あ、ちょっと怪しいですね。でも、ページを閉じる前に、少しだけ聞いてください。
    先に言っておくと、私たちは別にスピリチュアルが大好きな集団ではありません。高い壺も、開運グッズも売りません。
    ただの、運気をちょっと真剣に考える不動産屋です。</p>
  <p>でも、長く家の仕事をしていると、思うんです。同じ条件、同じ価格の物件でも、住んだ途端に運が回り出す家と、
    なぜかつまずく家がある。面白いもので、事業を伸ばす方や、ことを成す方ほど、この「縁」や「時」を大切にされます。
    理屈では説明できない。でも、確かにある。その「数字に出ない何か」を、私たちは気のせいで片付けたくないんです。</p>

  <h3>昔の人は、知っていた。</h3>
  <p>家を建てる前には土地を清める地鎮祭をやり、引っ越しの日取りを暦で選び、鬼門を気にして間取りを考えた。
    迷信と笑うのは簡単です。でも、何百年も受け継がれてきたということは、
    人がそこに「効いている何か」を感じ続けてきた、ということ。私たちは、その感覚を信じています。</p>
  <p>家を選ぶのは、本当は「これからの人生を、どこに置くか」を選ぶこと。だからこそ、価格と立地だけでなく、
    あなたとその土地・その時期との相性まで見て、はじめて納得のいく一軒に出会えると、私たちは思うんです。</p>
  <div class="quote">
    <p>土地と家をめぐる、不思議なご縁ってあるんです。<br>
       信じるか信じないかは、あなた次第。<br>
       でも、知っておいて損は、しませんよ。</p>
  </div>
  <div class="sig">― スピ不動産 ―</div>
</div></section>

<section class="sec" style="background:var(--bg-2);padding-bottom:clamp(3rem,9vw,5rem)"><div class="wrap">
  <div class="sec-hd"><h2>家を買う前、こんな不安はありませんか。</h2><span class="en">Before You Decide</span></div>
  <div class="worry">
    <div><h4>「今が、動く時なのか。」</h4>
      <p>買うべきか、売るべきか、もう少し待つべきか。大きな額が動く決断ほど、確かな決め手がほしい。</p></div>
    <div><h4>「この一手で、損はできない。」</h4>
      <p>高値で掴みたくないし、安く手放したくもない。数千万が動くからこそ、判断を間違えたくない。</p></div>
    <div><h4>「この選択は、先々まで効いてくる。」</h4>
      <p>住まいも資産も、長く付き合うもの。だからこそ、目先だけでなく運の巡りまで含めて選びたい。</p></div>
  </div>
  <p class="note">わかります。大きな決断ほど、物件そのものより「選ぶこと」が重いんですよね。
    でも、その迷いは、あなたとの「相性」と「動く時期」がわかるだけで、ぐっと定まります。</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-hd"><h2>だから、私たちはふたつの目で見ます。</h2><span class="en">Two Perspectives</span></div>
  <p class="note">その迷いは、相場の数字だけでは消えません。「この先どうなるか」を言い切れる人なんて、いないからです。
    だから私たちは、ひとつの不動産を、ふたつの目で見るようにしています。</p>
  <div class="two">
    <section><div class="num">一</div>
      <h4>不動産屋として、当たり前のことを。</h4>
      <p>周辺の成約事例から、根拠のある適正価格を出す。資金やローン、税のことまで見据える。
         契約の落とし穴も、先回りして潰しておく。占いの前に、まず地に足のついた仕事をします。
         星だけで、不動産は決められませんから。</p></section>
    <section><div class="num">二</div>
      <h4>あなたの星から、相性を。</h4>
      <p>四柱推命と九星気学で、あなたにとっての吉方位、動くと実を結びやすい時期、その土地との相性を見立てます。
         相場表には載っていない、ことを成す人が大切にしてきた判断材料です。</p></section>
  </div>
  <p class="note">現実の安心と、運気の納得。その両方が揃って、はじめて「ここだ」と思えるんです。</p>
</div></section>

<section class="sec"><div class="wrap read">
  <h2>「四柱推命」と「九星気学」って、なんですか？</h2>
  <p>急に難しそうな言葉が出てきましたね。でも、身構えなくて大丈夫です。
    どちらも昔から日本で大切にされてきた、「その人らしく生きるための、暮らしの知恵」のようなもの。
    かんたんに、お話しさせてください。</p>
  <h3>四柱推命は、生まれ持ったものを読む</h3>
  <p>生まれた年・月・日・時間の四つの柱から、あなたという人の持って生まれた性質や、運の流れを読み解くものです。
    いわば「あなたの取扱説明書」。どんな時期に力が出て、いつ慎重になったほうがいいか。
    家を動かすなら、いつがあなたにとって追い風なのか。その時期を見立てるのに使います。</p>
  <h3>九星気学は、方位との相性を読む</h3>
  <p>生まれた年から導く「九つの星」をもとに、あなたにとっての良い方角・気をつけたい方角を見るものです。
    昔の人が引っ越しの方角を気にしたのは、これ。同じ家でも、その人にとって追い風の方位と、向かい風の方位がある。
    だから、あなたの星に合った土地や方角を選ぶお手伝いに使います。</p>
  <p>むずかしく聞こえても、やることはシンプルです。あなたの「いつ動くといいか」を四柱推命で、
    「どこがいいか」を九星気学で。このふたつを重ねて、あなたにいちばん「ご縁」のある家を、ご一緒に探していきます。</p>
</div></section>

<section class="sec" style="background:var(--bg-2);padding-bottom:clamp(3rem,9vw,5rem)"><div class="wrap read">
  <h2>土地には、「気の流れ」があります。</h2>
  <p>これは占いというより、昔の人が何百年もかけて見つけてきた、土地の読み方です。少しだけ、面白い話をさせてください。</p>
  <h3>なぜ、あの土地は値が下がらないのか。</h3>
  <p>たとえば、東京のある場所は「四百年、地価が下がらない」と言われます。偶然ではありません。
    その昔、都を設計した人々は、北に山、東に川、南に水、西に道。四方を守りで囲まれた
    「四神相応（しじんそうおう）」という、気の集まる地形をわざわざ選んで中心に据えました。</p>
  <p>気が集まる場所には、人と富が自然と集まる。だから栄え、値が下がらない。昔の人はそう考えました。
    面白いのは、その通りに今も一等地であり続けている、ということです。</p>
  <h3>高台と、谷。</h3>
  <p>古い住宅地の地名には、ヒントが隠れています。「台」「丘」「山」がつく土地は高台。
    昔から気が安定し、住むのに良いとされ、今も高級住宅地はたいてい高台にあります。
    いっぽう「谷」がつく土地は、低くて気が流れすぎる、と昔の人は考えました。</p>
  <p>商いには「動き」がいるので、谷あいの街もにぎわいます。けれど「腰を据えて住む・構える」なら、
    気の安定した高台が良いとされてきた。物件を選ぶとき、地名の由来を一度調べてみると、面白い発見があるかもしれません。</p>
  <h3>谷の土地でも、大丈夫。</h3>
  <p>もし今、谷の土地にお住まいでも、心配はいりません。昔から「家の中の気は、整えられる」と言われてきました。
    玄関を明るく、風をよく通し、光を入れ、植物を置く。そうした昔ながらの工夫で、
    土地の弱さは半分以上、補えると考えられています。</p>
  <div class="quote"><p>大切なのは、土地の声を無視しないこと。<br>
    知ったうえで選び、整えれば、住まいは味方になります。</p></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-hd"><h2>あなたの「買い時」、無料でお調べします。</h2><span class="en">What You'll Know</span></div>
  <p class="note">あなたの生まれ持った星と、住まいの方位を照らし合わせる。
    すると、売る・買うの判断に直結する3つのことが、見えてきます。</p>
  <div class="trio">
    <div><div class="k">TIMING</div><h4>動くべき時期</h4>
      <p>運気には満ち欠けがあります。あなたが決断して実を結びやすい年を見極め、
         買い時・売り時は今か、待つべきかをお伝えします。</p></div>
    <div><div class="k">DIRECTION</div><h4>あなたの吉方位</h4>
      <p>同じ物件でも、あなたにとって追い風の方角と、向かい風の方角があります。
         金運・事業運・家庭運の観点から、良い方位を見立てます。</p></div>
    <div><div class="k">COMPATIBILITY</div><h4>土地・家との相性</h4>
      <p>その土地は、あなたと合うのか。間取りや方位を家相の知恵で診断し、
         住むほど・持つほど運を育む物件かどうかをお伝えします。</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-hd"><h2>鑑定の、おしながき。</h2><span class="en">Menu</span></div>
  <p class="note">ご相談の段階に合わせて、見立てのかたちをご用意しています。
    まずは無料の方位鑑定から。気になる物件が出てきたら、その物件との相性まで深く見ていきます。</p>
  <div class="menu">
    <div class="mcard"><div class="k">MENU 01</div><h4>吉方位 鑑定</h4>
      <p>生年月日から、四柱推命と九星気学であなたの吉方位・買い時を見立てます。
        「どこの街で探すといいか」「今が動く時か」の地図を、まず手にしていただくための鑑定です。</p>
      <div class="fee"><span>費用</span><b>無料</b></div></div>
    <div class="mcard"><div class="k">MENU 02</div><h4>物件 相性鑑定</h4>
      <p>気になる物件の方位・間取り・土地の気を、あなたの星と照らし合わせて診断します。
        家相の知恵も交え、住むほど・持つほど運を育む一軒かどうかを見極めます。</p>
      <div class="fee"><span>費用</span><b>物件探しと<br>あわせて無料</b></div></div>
    <div class="mcard"><div class="k">MENU 03</div><h4>住まい さがし鑑定</h4>
      <p>運気と条件、その両方が揃う住まいを、ご一緒に探します。物件の提案から、相場・資金・契約まわりの実務まで。
        星を読みながら、地に足のついた一軒選びまで伴走します。</p>
      <div class="fee"><span>費用</span><b>ご成約時の<br>仲介手数料のみ</b></div></div>
  </div>
  <p class="note">鑑定・ご相談・物件のご提案は、すべて無料です。
    費用をいただくのは、売買がご成約に至ったときの仲介手数料のみ。くわしい料金は、ご相談のなかでお伝えします。</p>
</div></section>

<section class="sec" id="props"><div class="wrap">
  <div class="sec-hd"><h2>運の巡る、住まいたち。</h2><span class="en">Properties</span></div>
  <p class="note">条件のよさだけでなく、土地の気や方位の相性まで見て選んだ住まいを、少しだけご紹介します。
    あなたの星に合うかどうかは、診断してはじめてわかります。</p>
</div></section>
<div class="rail" id="propRail"></div>
<div class="rail-hint">← スワイプで続きを見る</div>
<div class="wrap sec" style="padding-top:0">
  <div class="center"><a class="obtn" href="areas.html">エリアから探す →</a></div>
</div>

<section class="sec" style="background:var(--bg-2);padding-bottom:clamp(3rem,9vw,5rem)"><div class="wrap">
  <div class="sec-hd"><h2>お問い合わせから、住まい探しまで。</h2><span class="en">Flow</span></div>
  <p class="note">むずかしい手続きはありません。LINEひとつで、鑑定からご提案まで、ゆっくり進められます。
    急かすことは、いたしません。</p>
  <div class="flow">
    <div class="fstep"><span class="n">1</span><h4>LINEで友だち追加</h4><span class="t">30秒</span>
      <p>まずは公式LINEを友だち追加してください。お名前や細かな個人情報は、この時点では必要ありません。</p></div>
    <div class="fstep"><span class="n">2</span><h4>生年月日とご希望を送る</h4><span class="t">1分</span>
      <p>生年月日と、「買いたい／売りたい／まだ迷っている」などのご希望を送るだけ。まだ決まっていなくても、構いません。</p></div>
    <div class="fstep"><span class="n">3</span><h4>無料の吉方位鑑定が届く</h4><span class="t">後日</span>
      <p>あなたの吉方位と、動くべき時期を見立ててお届けします。気になる物件があれば、その相性もあわせて鑑定します。</p></div>
    <div class="fstep"><span class="n">4</span><h4>住まいのご提案・ご相談</h4><span class="t">じっくり</span>
      <p>鑑定をふまえ、運気と条件の揃う住まいをご提案します。相場や資金、契約のご相談も、このなかで承ります。</p></div>
    <div class="fstep"><span class="n">5</span><h4>ご納得のうえで、ご契約</h4><span class="t">ご縁が整えば</span>
      <p>現実の安心と運気の納得、その両方が揃ったときに、はじめてお進めします。急かすことは、決していたしません。</p></div>
  </div>
</div></section>

<section class="sec" id="line"><div class="wrap">
  <div class="sec-hd"><h2>あなたがやるのは、たった30秒だけ。</h2><span class="en">Start Here</span></div>
  <p class="note">物件を探し、相場を調べ、時を読む。その手間のかかる作業は、ぜんぶこちらが引き受けます。
    あなたは、要所の判断に集中してください。</p>
  {LINEBOX}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-hd"><h2>よくある、ご質問。</h2><span class="en">FAQ</span></div>
  <div class="faq">{faq}</div>
</div></section>
"""

js = """<script>
const E=FengshuiEngine;
const ST=["神谷町駅 徒歩2分","半蔵門駅 徒歩4分","白金高輪駅 徒歩5分","六本木駅 徒歩4分","大門駅 徒歩3分",
          "明治神宮前駅 徒歩7分","青山一丁目駅 徒歩6分","神谷町駅 徒歩6分","乃木坂駅 徒歩5分","六本木駅 徒歩8分"];
document.getElementById("propRail").innerHTML=Subjects.properties.map((p,i)=>{
  const r=E.evaluate(p), dir=E.helpers.dirOf(p.building.facing).n;
  return `<a class="pcard" href="property-azabudai.html"><span class="wm">${r.total}</span>
   <div class="top"><span class="no">${String(i+1).padStart(2,"0")}</span><span class="badge">売買</span></div>
   <div class="ar">${p.town}</div><h3>${p.name}</h3><hr>
   <dl class="kv"><dt>売買</dt><dd>${p.price}</dd></dl>
   <div class="st">${ST[i%ST.length]}　／　${dir}向き</div>
   <div class="fs"><div class="l">気の見立て</div>
     <div class="row"><b>${r.total}</b><small>pt</small><span class="arw">→</span></div></div></a>`;
}).join("");
</script>"""

open(f"{OUT}/index.html","w",encoding="utf-8").write(
  page("ことを成す人は、家を「星」で選ぶ。｜スピ不動産",
       "四柱推命と九星気学で、あなたの買い時・吉方位・土地との相性を無料で見立てる不動産屋です。",
       body, js))
print("index.html", round(len(open(f"{OUT}/index.html",encoding='utf-8').read())/1024), "KB")
