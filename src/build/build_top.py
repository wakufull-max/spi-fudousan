# -*- coding: utf-8 -*-
"""前のトップページ構成に、提供原稿のブロックを追加する"""
import json, re
from brand import FAQ

OUT = "/mnt/user-data/outputs"
t = open("template.html", encoding="utf-8").read()
photos = json.load(open("images.json", encoding="utf-8"))
thumb  = photos

merged = {"hero": photos["hero"]}
for k in ["minato","chiyoda","shibuya","meguro","setagaya","tokyo","yokohama","osaka","kawasaki","shonan","fukuoka"]:
    merged[k] = thumb[k]
for i,k in enumerate(["shibuya","kawasaki","tokyo","meguro"]): merged[f"col{i+1}"] = thumb[k]

# 。 1. 基本の調整（白基調・余白・ブランド・はみ出し対策） 。
R = [
 ("--cream:#EFECE4; --cream-2:#F5F3ED; --white:#FBFAF7;","--cream:#FFFFFF; --cream-2:#F7F5F0; --white:#FFFFFF;"),
 ("--ink:#2A2723; --ink-2:#6F6960; --ink-3:#9C958A;","--ink:#16150F; --ink-2:#45413A; --ink-3:#6B665D;"),
 ("--rule:#DCD6CA; --rule-2:#E7E2D8;","--rule:#D9D3C7; --rule-2:#E8E4DA;"),
 ("--gold:#AD9463;","--gold:#A8905F;"),
 ("font-size:clamp(2.35rem,10.5vw,4.4rem);line-height:1.4;letter-spacing:.06em;",
  "font-size:clamp(1.85rem,7.4vw,3.4rem);line-height:1.5;letter-spacing:.05em;"),
 ("\n.sec-hd{margin-bottom:clamp(1.6rem,6vw,2.4rem)}","\n.sec-hd{margin-bottom:clamp(1.4rem,5vw,2rem);padding-bottom:1rem;border-bottom:1px solid var(--rule)}"),
 ("--sp:clamp(1.15rem,5vw,2rem)","--sp:clamp(2.5rem,10.5vw,4.5rem)"),
 ("font-weight:300;\n  font-size:14px;line-height:2","font-weight:400;\n  font-size:15px;line-height:2"),
 ("background:rgba(245,243,237,.94)","background:rgba(255,255,255,.95)"),
 ("*{box-sizing:border-box;margin:0;padding:0}",
  "*{box-sizing:border-box;margin:0;padding:0;min-width:0}\nhtml,body{max-width:100%;overflow-x:hidden}\n@supports (overflow:clip){html,body{overflow-x:clip}}"),
 ("padding:0 var(--sp) .5rem;margin:0 calc(var(--sp) * -1)}",
  "padding:1.5rem var(--sp) 1.4rem;margin:0;max-width:100%;"
  "padding-left:max(var(--sp),calc((100% - var(--maxw))/2 + var(--sp)));"
  "scroll-padding-left:max(var(--sp),calc((100% - var(--maxw))/2 + var(--sp)))}"),
 ("<b>龍脈</b><span>RYUMYAKU REAL ESTATE</span>","<b>スピ不動産</b><span>SPI REAL ESTATE</span>"),
 ("© 2026 RYUMYAKU. All rights reserved.","© 2026 SPI REAL ESTATE. All rights reserved."),
 ("RYUMYAKU SHONAN →","スピ不動産 湘南 →"),
 ("<title>風水スコアで選ぶ東京の住まい｜龍脈 RYUMYAKU</title>",
  "<title>ことを成す人は、家を「星」で選ぶ。｜スピ不動産</title>"),
 ('transition:transform 1.2s ease;filter:saturate(.9)}','transition:transform 1.2s ease;filter:saturate(.92) contrast(.98)}'),
 ('background:linear-gradient(to bottom,rgba(24,26,30,.30),rgba(24,26,30,.42))}',
  'background:linear-gradient(to bottom,rgba(20,22,26,.26),rgba(20,22,26,.52))}'),
]
for a,b in R:
    if a not in t: print("⚠ 未一致:", a[:40])
    t = t.replace(a,b)
t = t.replace(";overflow-x:hidden}","}",1)
t = t.replace(""".logo b{display:block;font-family:var(--lat);font-weight:300;font-size:1.7rem;
  letter-spacing:.32em;text-indent:.32em}""",
""".logo b{display:block;white-space:nowrap;font-family:var(--min);font-weight:400;font-size:1.32rem;
  letter-spacing:.2em;text-indent:.2em}""")

# 。 2. 追加ブロック用のCSS 。
CSS = '''
.hero h1 span{display:inline-block}
h1 span,h2 span,h3 span,h4 span,.hero .sub span{display:inline-block}
h1,h2,h3,h4,.lead,.txt,.sub,.read p,.worry p,.two p,.trio p,.mcard p,.fstep p,.faq p{
  word-break:auto-phrase;line-break:strict;overflow-wrap:anywhere}
.read{max-width:46rem;margin:0}
.txt{font-size:.92rem;color:var(--ink-2);line-height:2.35;margin-top:1.4rem;max-width:46rem}

.read h3{font-family:var(--min);font-weight:600;font-size:clamp(1.12rem,4.4vw,1.4rem);
  letter-spacing:.06em;line-height:1.7;margin-top:2.8rem}
.read p{font-size:.92rem;color:var(--ink-2);line-height:2.35;margin-top:1.4rem;max-width:46rem}
.read p.big{font-size:1.02rem;color:var(--ink)}
.read .sig{font-family:var(--min);font-size:.95rem;letter-spacing:.16em;color:var(--ink-2);
  text-align:right;margin-top:2.4rem;max-width:46rem}
.read .big{font-size:1rem;color:var(--ink)}
.quote{border-left:3px solid var(--gold);padding:.4rem 0 .4rem 1.6rem;margin-top:2.2rem;max-width:46rem}
.quote p{margin-top:.5rem;font-family:var(--min);font-size:1rem;line-height:2.2;color:var(--ink)}
.worry{display:grid;grid-template-columns:1fr;gap:1.1rem;margin-top:2rem}
@media(min-width:820px){.worry{grid-template-columns:repeat(3,1fr)}}
.worry>div{background:#fff;border:1px solid var(--rule-2);border-radius:14px;box-shadow:0 2px 10px rgba(29,28,26,.06);padding:2rem 1.8rem}
.worry h4{font-family:var(--min);font-weight:600;font-size:1.06rem;line-height:1.7}
.worry p{font-size:.92rem;color:var(--ink-2);line-height:2.35;margin-top:1.1rem}
.two{margin-top:1.6rem;border-top:1px solid var(--rule)}
.two>section{display:grid;grid-template-columns:54px 1fr;padding:2.2rem 0;border-bottom:1px solid var(--rule-2)}
.two .num{display:flex;gap:5px;padding-top:.5rem}
.two .num i{display:block;width:1.5px;height:26px;background:var(--ink)}
.two h4{font-family:var(--min);font-weight:600;font-size:1.16rem;line-height:1.7}
.two p{grid-column:2;font-size:.92rem;color:var(--ink-2);line-height:2.35;margin-top:1.1rem;max-width:46rem}
.trio{display:grid;grid-template-columns:1fr;gap:1.1rem;margin-top:2rem}
@media(min-width:820px){.trio{grid-template-columns:repeat(3,1fr)}}
.trio>div{background:#fff;border:1px solid var(--rule-2);border-radius:14px;box-shadow:0 2px 10px rgba(29,28,26,.06);padding:2rem 1.8rem}
.trio .k{font-family:var(--mono,var(--lat));font-size:.74rem;letter-spacing:.24em;color:var(--gold)}
.trio h4{font-family:var(--min);font-weight:600;font-size:1.12rem;margin-top:.7rem}
.trio p{font-size:.92rem;color:var(--ink-2);line-height:2.3;margin-top:1.1rem}
.menu{display:grid;grid-template-columns:1fr;gap:1.1rem;margin-top:2rem}
@media(min-width:900px){.menu{grid-template-columns:repeat(3,1fr)}}
.mcard{background:#fff;border:1px solid var(--rule-2);border-radius:14px;box-shadow:0 2px 10px rgba(29,28,26,.06);padding:2.1rem 1.9rem 1.9rem;display:flex;flex-direction:column}
.mcard .k{font-family:var(--lat);font-size:.74rem;letter-spacing:.22em;color:var(--ink-3)}
.mcard h4{font-family:var(--min);font-weight:600;font-size:1.26rem;letter-spacing:.08em;margin-top:.7rem}
.mcard p{font-size:.92rem;color:var(--ink-2);line-height:2.3;margin-top:1.1rem}
.mcard .fee{margin-top:auto;padding-top:1.6rem;border-top:1px solid var(--rule-2);display:flex;align-items:baseline;justify-content:space-between;gap:.8rem}
.mcard .fee span{font-size:.78rem;color:var(--ink-3)}
.mcard .fee b{font-family:var(--min);font-weight:600;font-size:1.12rem;color:var(--gold);text-align:right;line-height:1.6}
.flow{margin-top:2rem;border-top:1px solid var(--rule)}
.fstep{display:grid;grid-template-columns:2.6rem 1fr auto;gap:.6rem 1.1rem;padding:1.8rem 0;border-bottom:1px solid var(--rule);align-items:baseline}
.fstep .n{font-family:var(--lat);font-size:1.3rem;color:var(--gold)}
.fstep h4{font-family:var(--min);font-weight:600;font-size:1.06rem}
.fstep p{grid-column:2/-1;font-size:.92rem;color:var(--ink-2);line-height:2.3;margin-top:.6rem;max-width:46rem}
.fstep .t{font-size:.76rem;color:var(--ink-3);white-space:nowrap}
.faq{margin-top:2rem;border-top:1px solid var(--rule)}
.faq details{border-bottom:1px solid var(--rule)}
.faq summary{list-style:none;cursor:pointer;padding:1.4rem 2rem 1.4rem 0;position:relative;font-family:var(--min);font-size:1rem;line-height:1.7}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"＋";position:absolute;right:.2rem;top:1.35rem;color:var(--gold)}
.faq details[open] summary::after{content:"−"}
.faq p{font-size:.92rem;color:var(--ink-2);line-height:2.3;padding:0 0 1.6rem;max-width:46rem}
.linebox{margin-top:2.6rem;background:#fff;border:1px solid var(--rule);border-top:3px solid #06C755;
  border-radius:12px;padding:2.8rem 1.8rem;text-align:center}
.linebox .k{font-family:var(--min);font-size:.86rem;letter-spacing:.22em;color:#3FAE55}
.linebox h3{font-family:var(--min);font-weight:400;font-size:clamp(1.1rem,4.6vw,1.5rem);margin-top:1.1rem;line-height:1.7}
.linebox .sb{font-size:.88rem;color:var(--ink-2);margin-top:.8rem;line-height:1.95}
.linebox ul{list-style:none;text-align:left;max-width:34rem;margin:1.6rem auto 0}
.linebox li{display:grid;grid-template-columns:20px 1fr;gap:.4rem;font-size:.89rem;color:var(--ink-2);padding:.44rem 0;line-height:2}
.linebox li i{color:#06C755;font-style:normal}
.gbtn{display:flex;align-items:center;justify-content:center;gap:.6rem;max-width:30rem;margin:1.8rem auto 0;
  background:#06C755;color:#fff;padding:1.05rem;font-family:var(--min);font-size:.96rem;letter-spacing:.1em;border-radius:6px}
.gbtn:hover{background:#05B34C}
.gbtn .badge{width:24px;height:24px;border-radius:7px;background:#fff;color:#06C755;display:inline-flex;
  align-items:center;justify-content:center;font-family:var(--lat);font-size:.58rem;font-weight:600;flex:0 0 auto}
.linebox .fn{font-size:.82rem;color:var(--ink-2);margin-top:1rem;line-height:1.95}
.rcard2{position:relative;width:min(74vw,308px);background:#fff;border:1px solid var(--rule-2);
  border-radius:16px;box-shadow:0 2px 10px rgba(29,28,26,.06);display:flex;flex-direction:column;
  overflow:hidden;color:var(--ink)}
.rcard2 .rph{aspect-ratio:16/10;background-size:cover;background-position:center;
  background-color:var(--cream-2);border-bottom:1px solid var(--rule-2)}
.rcard2 .rbd{position:relative;padding:1.7rem 1.6rem 1.5rem;display:flex;flex-direction:column;flex:1;min-height:210px}
.rcard2 .rwm{position:absolute;top:.4rem;right:1rem;font-family:var(--lat);font-style:italic;
  font-size:2.6rem;color:rgba(29,28,26,.05);line-height:1}
.rcard2 .ren{position:relative;font-family:var(--lat);font-size:.82rem;letter-spacing:.26em;text-indent:.26em}
.rcard2 h3{position:relative;font-family:var(--min);font-weight:600;font-size:1.42rem;
  letter-spacing:.12em;margin-top:.45rem}
.rcard2 hr{border:none;border-top:1px solid var(--rule);margin:1rem 0}
.rcard2 p{position:relative;font-size:.87rem;color:var(--ink-2);line-height:2.15}
.rcard2 .rgo{position:relative;margin-top:auto;padding-top:1.3rem;display:flex;
  align-items:center;justify-content:space-between;font-family:var(--min);font-size:.9rem;letter-spacing:.1em}

/* エリアカード（写真＋白いカード本体） */
.acard{position:relative;width:min(74vw,300px);background:#fff;border:1px solid var(--rule-2);
  border-radius:16px;box-shadow:0 2px 10px rgba(29,28,26,.06);display:flex;flex-direction:column;
  overflow:hidden;color:var(--ink);transition:.25s}
.acard:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(29,28,26,.11)}
.acard .ph{position:relative;aspect-ratio:16/10;background-size:cover;background-position:center;
  background-color:var(--cream-2);border-bottom:1px solid var(--rule-2);transform:none}
.acard::after{content:none}
.acard .bd{position:relative;padding:1.6rem 1.5rem 1.4rem;display:flex;flex-direction:column;flex:1;min-height:170px}
.acard .no{position:absolute;top:.4rem;right:1rem;font-family:var(--lat);font-style:italic;
  font-size:2.4rem;color:rgba(29,28,26,.05);line-height:1}
.acard .en{position:relative;font-family:var(--lat);font-size:.78rem;letter-spacing:.24em;
  text-indent:.24em;color:var(--gold)}
.acard .jp{position:relative;font-family:var(--min);font-weight:600;font-size:1.36rem;
  letter-spacing:.1em;margin-top:.45rem;color:var(--ink);text-shadow:none}
.acard hr{border:none;border-top:1px solid var(--rule);margin:.95rem 0}
.acard .tg{position:relative;font-size:.86rem;color:var(--ink-2);line-height:2.05;text-shadow:none}
.acard .go{position:relative;margin-top:auto;padding-top:1.2rem;display:flex;
  align-items:center;justify-content:space-between;font-family:var(--min);font-size:.9rem;
  letter-spacing:.1em;color:var(--gold)}
/* コラムカード */
.ccard{background:#fff;border:1px solid var(--rule-2);border-radius:14px;overflow:hidden;
  box-shadow:0 2px 10px rgba(29,28,26,.06);display:flex;flex-direction:column;
  width:min(74vw,300px);transition:.25s}
.ccard:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(29,28,26,.11)}
.ccard .ph{aspect-ratio:16/9;background-size:cover;background-position:center;
  background-color:var(--cream-2);border-bottom:1px solid var(--rule-2)}
.ccard .bd{padding:1.4rem 1.35rem 1.5rem;display:flex;flex-direction:column;flex:1}
.ccard .cat{align-self:flex-start;border:1px solid var(--rule);padding:.18rem .75rem;
  font-size:.75rem;color:var(--ink-2)}
.ccard h3,.ccard .ttl{font-family:var(--min);font-weight:600;font-size:1.02rem;line-height:1.8;
  margin-top:.85rem;color:var(--ink)}
.ccard .dt{margin-top:auto;padding-top:1.2rem;font-family:var(--lat);font-size:.78rem;color:var(--ink-2)}
.pcard2{position:relative;width:min(74vw,308px);background:#FAF8F3;border:1px solid var(--rule-2);
  border-radius:16px;box-shadow:0 2px 10px rgba(29,28,26,.06);display:flex;flex-direction:column;overflow:hidden;color:var(--ink)}
.ph2{aspect-ratio:16/9;background-size:cover;background-position:center;background-color:#FBFAF7;
  border-bottom:1px solid var(--rule-2)}
.bd2{position:relative;padding:1.7rem 1.6rem 1.5rem;display:flex;flex-direction:column;flex:1;min-height:270px}
.pcard2 .wm2{position:absolute;top:-.6rem;right:.9rem;font-family:var(--min);font-weight:700;font-size:8rem;line-height:1;color:rgba(29,28,26,.035)}
.top2{position:relative;display:flex;align-items:center;justify-content:space-between}
.no2{font-family:var(--lat);font-style:italic;font-size:1rem;color:var(--ink-2)}
.badge2{background:#7B2E27;color:#fff;font-size:.72rem;letter-spacing:.08em;padding:.26rem .8rem;border-radius:3px}
.ar2{position:relative;font-size:.79rem;color:var(--ink-2);letter-spacing:.1em;margin-top:1.1rem}
.pcard2 h3{position:relative;font-family:var(--min);font-weight:600;font-size:1.2rem;margin-top:.2rem;line-height:1.5}
.pcard2 hr{border:none;border-top:1px solid var(--rule);margin:.9rem 0 1rem}
.kv2{position:relative;display:flex;align-items:baseline;gap:.8rem}
.kv2 dt{font-size:.74rem;color:var(--ink-3)} .kv2 dd{font-family:var(--min);font-size:.96rem}
.pcard2 .st{position:relative;font-size:.79rem;color:var(--ink-2);margin-top:.5rem;line-height:1.9}
.fs2{position:relative;margin-top:auto;padding-top:1.2rem}
.l2{font-family:var(--min);font-size:.86rem;color:var(--ink-2);letter-spacing:.06em}
.row2{display:flex;align-items:flex-end;gap:.3rem;margin-top:.2rem}
.row2 b{font-family:var(--min);font-weight:700;font-size:2.3rem;color:#8A7346;line-height:1}
.row2 small{font-size:.78rem;color:var(--ink-3);margin-bottom:.28rem}
.arw2{margin-left:auto;color:var(--ink-3);margin-bottom:.3rem}
'''
t = t.replace("@media(prefers-reduced-motion:reduce)", CSS + "@media(prefers-reduced-motion:reduce)")

# 。 3. ヒーローの文言 。
t = t.replace("""    <h1>気は、<br>地形に宿る。</h1>
    <p class="sub">標高、尾根、坐向、形殺。<br>東京の土地の吉凶を、たどれる数値に。</p>""",
"""    <div class="eyebrow" style="font-family:var(--min);font-size:.86rem;letter-spacing:.2em;color:rgba(255,255,255,.82)">四柱推命 × 九星気学 × 不動産</div>
    <h1><span>ことを成す人は、</span><span>家を「星」で選ぶ。</span></h1>
    <p class="sub">今が買い時か、この街でいいか、あなたと相性のいい家はどれか。<br>
      生まれ持った星から、ご縁のある一軒と、買うのに良い時期を見立てます。</p>""")
t = t.replace('<a class="hbtn solid" href="#diagnose">命星診断（無料）→</a>',
              '<a class="hbtn solid" href="#line">吉方位を無料診断 →</a>')
t = t.replace('<a class="hbtn line" href="#areas">エリアから探す</a>',
              '<a class="hbtn line" href="#props">住まいを見る</a>')

# 。 4. 「龍脈の視点」を「ふたつの目」に差し替え 。
vi = t.index('<h2>龍脈の視点</h2>')
start = t.rindex('<section', 0, vi)
end   = t.index('<section class="blk" id="column">')
t = t[:start] + '''<!-- ══ ふたつの目 ══ -->
<section class="blk alt"><div class="wrap">
  <div class="sec-hd row"><h2>だから、ふたつの目で見ます。</h2><span class="en">Two Perspectives</span></div>
  <p class="txt">
    その迷いは、相場の数字だけでは消えません。「この先どうなるか」を言い切れる人なんて、いないからです。
    だから私たちは、ひとつの不動産を、ふたつの目で見るようにしています。</p>
  <div class="two">
    <section><div class="num"><i></i></div>
      <h4>不動産屋として、当たり前のことを。</h4>
      <p>周辺の成約事例から、根拠のある適正価格を出す。資金やローン、税のことまで見据える。
        契約の落とし穴も、先回りして潰しておく。占いの前に、まず地に足のついた仕事をします。
        星だけで、不動産は決められませんから。</p></section>
    <section><div class="num"><i></i><i></i></div>
      <h4>あなたの星から、相性を。</h4>
      <p>四柱推命と九星気学で、あなたにとっての吉方位、動くと実を結びやすい時期、その土地との相性を見立てます。
        相場表には載っていない、ことを成す人が大切にしてきた判断材料です。</p></section>
  </div>
  <p class="txt">
    現実の安心と、運気の納得。その両方が揃って、はじめて「ここだ」と思えるんです。</p>
</div></section>

''' + t[end:]

# 。 5. 各所にブロックを挿入 。
READ_KAMISAMA = '''
<!-- ══ 土地の神様 ══ -->
<section class="blk"><div class="wrap">
  <div class="sec-hd row"><h2>土地の神様。</h2><span class="en">Our Belief</span></div>
  <div class="read">
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
  <div class="quote"><p>土地と家をめぐる、不思議なご縁ってあるんです。<br>
    信じるか信じないかは、あなた次第。<br>でも、知っておいて損は、しませんよ。</p></div>
  <div class="sig">― スピ不動産 ―</div>
  </div>
</div></section>
'''

WORRY = '''
<!-- ══ 不安 ══ -->
<section class="blk alt"><div class="wrap">
  <div class="sec-hd row"><h2>家を買う前、こんな不安はありませんか。</h2><span class="en">Before You Decide</span></div>
  <div class="worry">
    <div><h4>「今が、動く時なのか。」</h4>
      <p>買うべきか、売るべきか、もう少し待つべきか。大きな額が動く決断ほど、確かな決め手がほしい。</p></div>
    <div><h4>「この一手で、損はできない。」</h4>
      <p>高値で掴みたくないし、安く手放したくもない。数千万が動くからこそ、判断を間違えたくない。</p></div>
    <div><h4>「この選択は、先々まで効いてくる。」</h4>
      <p>住まいも資産も、長く付き合うもの。だからこそ、目先だけでなく運の巡りまで含めて選びたい。</p></div>
  </div>
  <p class="txt">
    わかります。大きな決断ほど、物件そのものより「選ぶこと」が重いんですよね。
    でも、その迷いは、あなたとの「相性」と「動く時期」がわかるだけで、ぐっと定まります。</p>
</div></section>
'''

TERMS = '''
<!-- ══ 用語 ══ -->
<section class="blk"><div class="wrap">
  <div class="sec-hd row"><h2>「四柱推命」と「九星気学」って、なんですか？</h2><span class="en">Basics</span></div>
  <div class="read">
  <p>急に難しそうな言葉が出てきましたね。でも、身構えなくて大丈夫です。
    どちらも昔から日本で大切にされてきた、「その人らしく生きるための、暮らしの知恵」のようなもの。</p>
  <h3>四柱推命は、生まれ持ったものを読む</h3>
  <p>生まれた年・月・日・時間の四つの柱から、あなたという人の持って生まれた性質や、運の流れを読み解くものです。
    いわば「あなたの取扱説明書」。どんな時期に力が出て、いつ慎重になったほうがいいか。
    家を動かすなら、いつがあなたにとって追い風なのか。その時期を見立てるのに使います。</p>
  <h3>九星気学は、方位との相性を読む</h3>
  <p>生まれた年から導く「九つの星」をもとに、あなたにとっての良い方角・気をつけたい方角を見るものです。
    昔の人が引っ越しの方角を気にしたのは、これ。同じ家でも、その人にとって追い風の方位と、向かい風の方位がある。</p>
  <p>むずかしく聞こえても、やることはシンプルです。あなたの「いつ動くといいか」を四柱推命で、
    「どこがいいか」を九星気学で。このふたつを重ねて、あなたにいちばん「ご縁」のある家を、ご一緒に探していきます。</p>
  </div>
</div></section>
'''

TERRAIN = '''
<!-- ══ 気の流れ ══ -->
<section class="blk alt"><div class="wrap">
  <div class="sec-hd row"><h2>土地には、「気の流れ」があります。</h2><span class="en">Reading the Land</span></div>
  <div class="read">
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
  </div>
</div></section>
'''

TRIO_MENU = '''
<!-- ══ わかる3つ ══ -->
<section class="blk"><div class="wrap">
  <div class="sec-hd row"><h2>あなたの「買い時」、無料でお調べします。</h2><span class="en">What You'll Know</span></div>
  <p class="txt">
    あなたの生まれ持った星と、住まいの方位を照らし合わせる。
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

  <div class="sec-hd row" style="margin-top:3.5rem"><h2>鑑定の、おしながき。</h2><span class="en">Menu</span></div>
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
  <p class="txt">
    鑑定・ご相談・物件のご提案は、すべて無料です。費用をいただくのは、売買がご成約に至ったときの仲介手数料のみ。</p>
</div></section>
'''

faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in FAQ)
FLOW_FAQ = f'''
<!-- ══ 流れ・LINE・FAQ ══ -->
<section class="blk" id="line"><div class="wrap">
  <div class="sec-hd row"><h2>お問い合わせから、住まい探しまで。</h2><span class="en">Flow</span></div>
  <p class="txt">
    むずかしい手続きはありません。LINEひとつで、鑑定からご提案まで、ゆっくり進められます。急かすことは、いたしません。</p>
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

  <div class="linebox">
    <div class="k">LINE 無料鑑定</div>
    <h3>あなたがやるのは、<br>たった30秒だけ。</h3>
    <p class="sb">物件を探し、相場を調べ、時を読む。その手間のかかる作業は、ぜんぶこちらが引き受けます。<br>
      あなたは、要所の判断に集中してください。</p>
    <ul>
      <li><i>✓</i>動くべき時期。決断が実を結びやすい年を見極めます</li>
      <li><i>✓</i>あなたの吉方位。金運・事業運・家庭運から良い方角を見立てます</li>
      <li><i>✓</i>土地・家との相性。間取りと方位を家相の知恵で診断します</li>
      <li><i>✓</i>気になる物件があれば、その一軒との相性まで</li>
    </ul>
    <a class="gbtn" href="#"><span class="badge">LINE</span>LINEで吉方位を無料診断</a>
    <p class="fn">完全無料／勧誘なし／お忙しい方も気軽に。<br>売る・買うが決まっていなくても、構いません。</p>
  </div>
</div></section>

<section class="blk alt"><div class="wrap">
  <div class="sec-hd row"><h2>よくある、ご質問。</h2><span class="en">FAQ</span></div>
  <div class="faq">{faq_html}</div>
</div></section>
'''

t = t.replace('<section class="blk" id="areas">', READ_KAMISAMA + '\n<section class="blk" id="areas">')

AREA_TEMPLATE = """document.getElementById("areaRail").innerHTML = AREAS.map((a,i)=>`
 <a class="acard" href="${WHREF[a.jp]||'areas.html'}">
  <div class="ph" style="background-image:url('${IMG[a.img]}')"></div>
  <div class="bd"><span class="no">${String(i+1).padStart(2,'0')}</span>
    <div class="en">${WEN[a.jp]||''}</div><div class="jp">${a.jp}</div>
    <hr><div class="tg">${a.tag}</div>
    <div class="go"><span>この区を読む</span><span>&rarr;</span></div>
  </div></a>`).join('')
 + `<a class="acard" href="areas.html">
    <div class="ph" style="background-image:url('${IMG.tokyo}')"></div>
    <div class="bd"><div class="en">ALL AREAS</div><div class="jp">23区すべて</div>
      <hr><div class="tg">同じ基準で並べて、比べられます。</div>
      <div class="go"><span>一覧を見る</span><span>&rarr;</span></div></div></a>`;
"""

COL_TEMPLATE = """document.getElementById("colRail").innerHTML = COLS.map(c=>`
 <a class="ccard" href="columns.html">
  <div class="ph" style="background-image:url('${IMG[c.img]}')"></div>
  <div class="bd"><span class="cat">${c.cat}</span>
    <div class="ttl">${c.t}</div><div class="dt">${c.d}</div>
  </div></a>`).join('');

"""

# ── エリアカード・コラムカードを物件カードと同じ体裁にする ──
import json as _cj
_WEN = _cj.dumps({'千代田区': 'CHIYODA', '中央区': 'CHUO', '港区': 'MINATO', '渋谷区': 'SHIBUYA', '目黒区': 'MEGURO', '世田谷区': 'SETAGAYA'}, ensure_ascii=False)
_WHREF = _cj.dumps({'千代田区': 'ward-chiyoda.html', '中央区': 'ward-chuo.html', '港区': 'ward-minato.html', '渋谷区': 'ward-shibuya.html', '目黒区': 'ward-meguro.html', '世田谷区': 'ward-setagaya.html'}, ensure_ascii=False)

_ai = t.index('document.getElementById("areaRail").innerHTML')
_ae = t.index(chr(10) + "function renderProps", _ai)
_area_js = (
  "const WEN=" + _WEN + ";" + chr(10) +
  "const WHREF=" + _WHREF + ";" + chr(10) +
  AREA_TEMPLATE
)
t = t[:_ai] + _area_js + t[_ae:]

_ci = t.index('document.getElementById("colRail").innerHTML')
_ce = t.index('document.getElementById("regRail")', _ci)
t = t[:_ci] + COL_TEMPLATE + t[_ce:]

t = t.replace('<section class="blk" id="diagnose">', WORRY + '\n<section class="blk" id="diagnose">')
# 命星診断のブロックを切り出して、おしながきの後ろへ移す
di = t.index('<section class="blk" id="diagnose">')
de = t.index('</section>', t.index('</div></section>', di)) + len('</section>')
diag_block = t[di:de]
t = t[:di] + t[de:]
t = t.replace('<section class="blk" id="column">', TERMS + '\n<section class="blk" id="column">')
# 「エリアを見る」を切り出して「注目物件」の直下へ移動
oi = t.index('<h2>エリアを見る</h2>')
os_ = t.rindex('<section', 0, oi)
oe  = t.index('</section>', oi) + len('</section>')
region_block = t[os_:oe]
t = t[:os_] + t[oe:]
pi = t.index('<section class="blk alt" id="props">')
pe = t.index('</section>', pi) + len('</section>')
t = t[:pe] + '\n' + region_block + '\n' + t[pe:]
# 「土地には気の流れが」はコラムの手前に置く
ci = t.index('<section class="blk" id="column">')
t = t[:ci] + TERRAIN + '\n' + t[ci:]
# 旧CTAを新ブロック群に置換
cs = t.index('<section class="cta" id="cta">'); ce = t.index('</main>')
t = t[:cs] + TRIO_MENU + diag_block + FLOW_FAQ + t[ce:]

# 。 6. エンジンで物件カードを描画 。
libs = ""
for f in ("fengshui-engine.js","subjects.js","render.js"):
    libs += "<script>" + open(f"{OUT}/{f}", encoding="utf-8").read() + "</script>\n"
t = t.replace('<script>\n"use strict";', libs + '<script>\n"use strict";')
# PROPS〜score() だけを差し替える（COLS/REGS/各railの描画は残す）
st = t.index("const PROPS=[")
en = t.index("const COLS=[")
t = t[:st] + '''const TOPP=[{"id":"p0281","name":"三田ガーデンヒルズ パークマンション","ward":"港区","price":"22億円","st":"麻布十番","walk":"7","layout":"3LDK","area":160.95,"builtLabel":"2024年12月","dir":"南","total":83,"grade":"A","era":100,"img":"minato"},{"id":"p0282","name":"三田ガーデンヒルズ パークマンション","ward":"港区","price":"22億円","st":"麻布十番","walk":"7","layout":"3LDK","area":160.95,"builtLabel":"2024年12月","dir":"南","total":83,"grade":"A","era":100,"img":"minato"},{"id":"p0283","name":"三田ガーデンヒルズ パークマンション","ward":"港区","price":"22億円","st":"麻布十番","walk":"7","layout":"3LDK","area":160.95,"builtLabel":"2024年12月","dir":"南","total":83,"grade":"A","era":100,"img":"minato"},{"id":"p0284","name":"三田ガーデンヒルズ パークマンション","ward":"港区","price":"22億円","st":"麻布十番","walk":"7","layout":"3LDK","area":160.95,"builtLabel":"2024年12月","dir":"南","total":83,"grade":"A","era":100,"img":"minato"},{"id":"p0286","name":"パークコート青山ザタワー","ward":"港区","price":"21億円","st":"青山一丁目","walk":"3","layout":"3LDK+S（納戸）","area":234.04,"builtLabel":"2017年12月","dir":"南","total":83,"grade":"A","era":96,"img":"minato"},{"id":"p0225","name":"クラッシィタワー新宿御苑","ward":"新宿区","price":"6億6,980万円","st":"新宿御苑前","walk":"5","layout":"3LDK","area":116.14,"builtLabel":"2024年11月","dir":"南","total":81,"grade":"A","era":100,"img":"tokyo"},{"id":"p0230","name":"上落合１丁目ビル ６・７階メゾネット（住居・158.57m 2 ） 大型車２台駐車可","ward":"新宿区","price":"5億4,800万円","st":"下落合","walk":"4","layout":"3LDK+2S（納戸）","area":158.57,"builtLabel":"1996年4月","dir":"南","total":81,"grade":"A","era":96,"img":"tokyo"},{"id":"p0167","name":"ブランズザハウス一番町","ward":"千代田区","price":"7億9,800万円","st":"半蔵門","walk":"3","layout":"3LDK","area":137.29,"builtLabel":"2016年10月","dir":"南","total":80,"grade":"A","era":96,"img":"chiyoda"},{"id":"p0285","name":"三田ガーデンヒルズ パークマンション","ward":"港区","price":"21億6,800万円","st":"麻布十番","walk":"5","layout":"3LDK","area":163.09,"builtLabel":"2025年3月","dir":"北","total":80,"grade":"A","era":88,"img":"minato"},{"id":"p0161","name":"ザ・パークハウスグラン千鳥ヶ淵","ward":"千代田区","price":"20億円","st":"半蔵門","walk":"7","layout":"3LDK","area":127.76,"builtLabel":"2015年3月","dir":"南東","total":79,"grade":"A","era":56,"img":"chiyoda"},{"id":"p0163","name":"パークコート千代田富士見ザ タワー","ward":"千代田区","price":"8億8,800万円","st":"飯田橋","walk":"3","layout":"2LDK","area":106.08,"builtLabel":"2014年3月","dir":"南東","total":79,"grade":"A","era":56,"img":"chiyoda"},{"id":"p0164","name":"パレスビュー四番町","ward":"千代田区","price":"8億1,500万円","st":"市ケ谷","walk":"4","layout":"2LDK+S（納戸）","area":190.41,"builtLabel":"2009年11月","dir":"南東","total":79,"grade":"A","era":56,"img":"chiyoda"}];

''' + t[en:]

ps = t.index("function renderProps(res){")
pe = t.index("renderProps(null);") + len("renderProps(null);")
t = t[:ps] + '''function renderProps(){
  document.getElementById("propRail").innerHTML = TOPP.map((s,i)=>`
    <a class="pcard2" href="property.html?id=${s.id}">
      <div class="ph2" style="background-image:url('${IMG[s.img]||IMG.tokyo}')"></div>
      <div class="bd2"><span class="wm2">${s.total}</span>
        <div class="top2"><span class="no2">${String(i+1).padStart(2,"0")}</span><span class="badge2">売買</span></div>
        <div class="ar2">${s.ward}</div><h3>${s.name}</h3><hr>
        <dl class="kv2"><dt>売買</dt><dd>${s.price}</dd></dl>
        <div class="st">${s.st}駅 徒歩${s.walk}分　／　${s.dir}向き</div>
        <div class="st">${s.layout}／${s.area}㎡　${s.builtLabel}築</div>
        <div class="fs2"><div class="l2">気の見立て</div>
          <div class="row2"><b>${s.total}</b><small>pt</small><span class="arw2">→</span></div></div>
      </div></a>`).join("");
}
renderProps();''' + t[pe:]

t = t.replace("paint(res);renderProps(res);", "paint(res);")

# ── ナビゲーションを実ページへ接続する
NAV = [
 ('href="#diagnose"',            'href="diagnosis.html"'),
 ('href="index.html#diagnose"',  'href="diagnosis.html"'),
 ('<a class="hbtn solid" href="#line">',  '<a class="hbtn solid" href="diagnosis.html">'),
 ('<a class="hd-cta" href="#line">',      '<a class="hd-cta" href="diagnosis.html">'),
 # ヘッダー・フッター
 ('<a href="#areas">エリア風水</a>',   '<a href="areas.html">エリア風水</a>'),
 ('<a href="#props">物件一覧</a>',     '<a href="properties.html">物件一覧</a>'),
 ('<a href="#column">コラム</a>',      '<a href="columns.html">コラム</a>'),
 ('<a href="#">開運口コミ</a>',        '<a href="columns.html">コラム一覧</a>'),
 ('<a href="#">龍脈とは</a>',          '<a href="#top">スピ不動産とは</a>'),
 ('<a href="#">採点基準</a>',          '<a href="areas.html">エリアを見る</a>'),
 # 「すべて見る」系
 ('<a class="more" href="#">すべて見る / <em>ALL AREAS</em></a>',
  '<a class="more" href="areas.html">すべて見る / <em>ALL AREAS</em></a>'),
 ('<a class="more" href="#">すべて見る / <em>ALL PROPERTIES</em></a>',
  '<a class="more" href="properties.html">すべて見る / <em>ALL PROPERTIES</em></a>'),
 ('<a class="more" href="#">一覧を見る / <em>COLUMN</em></a>',
  '<a class="more" href="columns.html">一覧を見る / <em>COLUMN</em></a>'),
 ('<a class="more" href="#"><em>OTHER REGIONS</em></a>',
  '<a class="more" href="areas.html"><em>OTHER REGIONS</em></a>'),
 ('<a class="obtn" href="#">128件すべて見る →</a>',
  '<a class="obtn" href="properties.html">物件一覧をすべて見る →</a>'),
 ('<a class="obtn" href="#">コラム一覧を見る →</a>',
  '<a class="obtn" href="columns.html">コラム一覧を見る →</a>'),
 ('<a class="obtn" href="#">湘南のコラムを見る →</a>',
  '<a class="obtn" href="columns.html">エリア別のコラムを見る →</a>'),
]
for _a, _b in NAV: t = t.replace(_a, _b)

# JSが生成するカードのリンク先
t = t.replace('AREAS.map(a=>`<a class="acard" href="#">',
  'AREAS.map(a=>`<a class="acard" href="${a.jp===\'港区\'?\'ward-minato.html\':\'areas.html\'}">')
t = t.replace('+`<a class="acard all" href="#">', '+`<a class="acard all" href="areas.html">')
t = t.replace('COLS.map(c=>`\n <a class="ccard" href="#">', 'COLS.map(c=>`\n <a class="ccard" href="columns.html">')
t = t.replace('<a class="ccard" href="#">', '<a class="ccard" href="columns.html">')

# ── 診断関連のリンクを最終的に診断ページへ寄せる
t = t.replace('href="#diagnose"', 'href="diagnosis.html"')
t = t.replace('href="index.html#diagnose"', 'href="diagnosis.html"')
t = t.replace('<a class="hbtn solid" href="#line">', '<a class="hbtn solid" href="diagnosis.html">')
t = t.replace('<a class="hd-cta" href="#line">', '<a class="hd-cta" href="diagnosis.html">')


# ── 日本語の改行を語句単位に固定する ──────────────────────
import re as _re2
def _phrases(t):
    """句読点・鉤括弧で意味の切れ目に分け、途中で折り返さない単位にする"""
    out, buf, i = [], "", 0
    while i < len(t):
        ch = t[i]
        buf += ch
        if ch in "、。？！":
            out.append(buf); buf = ""
        i += 1
    if buf: out.append(buf)
    # 短すぎる断片は前後へ寄せる
    merged = []
    for p in out:
        if merged and len(p) <= 3: merged[-1] += p
        else: merged.append(p)
    return merged

def _wrap_headings(html):
    def rep(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if "${" in inner or "<" in inner or len(inner.strip()) < 7: return m.group(0)
        ps = _phrases(inner.strip())
        if len(ps) < 2: return m.group(0)
        return f"<{tag}{attrs}>" + "".join(f"<span>{p}</span>" for p in ps) + f"</{tag}>"
    html = _re2.sub(r"<(h1|h2|h3|h4)([^>]*)>([^<]+)</\1>", rep, html)
    # ヒーローのサブコピー
    def rep2(m):
        inner = m.group(1)
        if "${" in inner: return m.group(0)
        parts = [x for x in inner.split("<br>") if x.strip()]
        out = []
        for pt in parts:
            out.append("".join(f"<span>{p}</span>" for p in _phrases(pt.strip())))
        return '<p class="sub">' + "<br>".join(out) + "</p>"
    html = _re2.sub(r'<p class="sub">(.*?)</p>', rep2, html, flags=_re2.S)
    return html

t = _wrap_headings(t)

out = t.replace("__IMAGES__", json.dumps(merged, ensure_ascii=False))
open(f"{OUT}/index.html","w",encoding="utf-8").write(out)
print("index.html", round(len(out)/1024), "KB | token残", out.count("__IMAGES__"))
