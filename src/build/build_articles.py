# -*- coding: utf-8 -*-
import json, re, html
from common_v2 import *
from brand import LINEBOX, DIAGNOSIS
C = json.load(open("columns.json", encoding="utf-8"))

TOKYO_EN = {"千代田区":"chiyoda","中央区":"chuo","港区":"minato","新宿区":"shinjuku","文京区":"bunkyo",
 "台東区":"taito","墨田区":"sumida","江東区":"koto","品川区":"shinagawa","目黒区":"meguro","大田区":"ota",
 "世田谷区":"setagaya","渋谷区":"shibuya","中野区":"nakano","杉並区":"suginami","豊島区":"toshima",
 "北区":"kita","荒川区":"arakawa","板橋区":"itabashi","練馬区":"nerima","足立区":"adachi",
 "葛飾区":"katsushika","江戸川区":"edogawa"}

def md(text):
    """見出しと段落だけの簡易マークダウン"""
    out, buf = [], []
    def flush():
        if buf:
            out.append("<p>" + html.escape(" ".join(buf)).replace("&quot;", '"') + "</p>")
            buf.clear()
    for line in text.split("\n"):
        l = line.strip()
        if not l: flush(); continue
        if l.startswith("### "): flush(); out.append(f"<h3>{html.escape(l[4:])}</h3>")
        elif l.startswith("## "): flush(); out.append(f"<h2>{html.escape(l[3:])}</h2>")
        else: buf.append(l)
    flush()
    return "\n".join(out)

def bullets(text):
    items = [re.sub(r"^[・･]\s*", "", x.strip()) for x in text.split("\n") if x.strip()]
    return "".join(f"<li><i>✓</i><span>{html.escape(i)}</span></li>" for i in items)

BYCITY = {}
for c in C: BYCITY.setdefault(c["city"], []).append(c)

for i, c in enumerate(C):
    same = BYCITY[c["city"]]
    idx = same.index(c)
    prev = same[idx-1] if idx > 0 else same[-1]
    nxt  = same[idx+1] if idx < len(same)-1 else same[0]
    sm = [x.strip() for x in c["summary"].split("／") if x.strip()]
    smrows = "".join(f"<dt>{x.split('：')[0]}</dt><dd>{'：'.join(x.split('：')[1:])}</dd>"
                     for x in sm if "：" in x)
    wardlink = (f'<a class="obtn" href="ward-{TOKYO_EN[c["ward"]]}.html">{c["ward"]}のページを見る →</a>'
                if c["city"] == "東京23区" and c["ward"] in TOKYO_EN else
                f'<a class="obtn" href="properties.html">{c["city"]}{c["ward"]}の物件を見る →</a>')
    refs = "".join(f'<a href="{r}" target="_blank" rel="noopener">{r}</a>' for r in c["refs"])
    chips = "".join(f'<span class="chip">{a}</span>' for a in c["areas"])

    body = f"""
<div class="wrap bc"><a href="index.html">トップ</a><span>/</span><a href="columns.html">コラム</a><span>/</span>{c['ward']}</div>
<div class="wrap pg">
  <div class="eyebrow">Column · {c['pref']}{c['city'] if c['city']!='東京23区' else ''}</div>
  <h1 class="pt">{("" if c['city']=="東京23区" else c['city']) + c['title'].split('｜')[0]}</h1>
  <div class="pt-sub">{c['title'].split('｜')[1] if '｜' in c['title'] else ''}</div>
  <p class="lead">{c['lead']}</p>
  <div class="chips">{chips}</div>
  <div class="stance">
    <div class="ic">この記事は<br>土地の話です</div>
    <p>生年月日や命星は使いません。地形・水系・地歴という、誰が見ても同じ土地の情報だけを扱います。
      風水の用語は形勢派の枠組みで用い、龍脈は超自然的な線ではなく、台地・尾根・谷・河川・街路の連なりを指す説明概念として扱います。
      吉凶の記述は、洪水・内水・高潮・液状化の想定区域と必ず照合してください。</p>
  </div>
  <div class="sumbox"><dl>{smrows}</dl></div>
  <div class="art">
    {md(c['body1'])}
    {md(c['keirei'])}
    {md(c['body2'])}
  </div>
  <div class="checkbox">
    <h3>現地で確認したいこと</h3><div class="en">Checklist</div>
    <ul>{bullets(c['check'])}</ul>
  </div>
  <div class="caution"><b>確認ポイント</b><p>{c['caution']}</p></div>
  <div class="refs"><div class="k">参考</div>{refs}</div>
  <div class="center" style="margin-top:2.4rem">{wardlink}</div>
  <div class="artnav">
    <a href="{prev['slug']}.html"><div><span class="l">← 前の記事</span><span class="n">{prev['ward']}</span></div></a>
    <a href="{nxt['slug']}.html"><div><span class="l">次の記事 →</span><span class="n">{nxt['ward']}</span></div></a>
  </div>
</div>
<div class="wrap sec">{LINEBOX}</div>
<section class="bridge"><div class="wrap"><div class="in">
  <div class="k">DIAGNOSIS</div>
  <h2><span>自分に合う</span><span>運命の住まいを</span><span>見つける</span></h2>
  <p>ここまでは土地の話でした。同じ土地でも、住む人によって合う・合わないがあるとされます。
     生年月日から命星と吉方位を割り出し、{c['ward']}のどのあたりが合うかをお伝えします。</p>
  <div class="btns">
    <a class="b1" href="diagnosis.html">無料で診断する　→</a>
  </div>
  <p class="fn" style="font-size:.82rem;color:var(--ink-2);margin-top:1.4rem">
    5つの質問に答えるだけ。登録も費用もかかりません。</p>
</div></div></section>"""

    # 区名は市をまたいで重複するため、東京以外は市名を冠する
    pfx = "" if c["city"] == "東京23区" else c["city"]
    seoT = (pfx + c["seoTitle"]) if pfx else c["seoTitle"]
    seoD = (pfx + c["seoDesc"]) if pfx else c["seoDesc"]
    open(f"{OUT}/{c['slug']}.html","w",encoding="utf-8").write(
        page(seoT + "｜スピ不動産", seoD, body, ""))
print(f"{len(C)} 本の記事ページを生成")
