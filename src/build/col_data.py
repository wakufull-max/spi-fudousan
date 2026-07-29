# -*- coding: utf-8 -*-
import csv, io, json
t = open("/mnt/user-data/uploads/注目高級物件リスト_2026-07-29_-_エリア別コラム.csv","rb").read().decode("utf-8-sig")
R = list(csv.DictReader(io.StringIO(t)))

CITY = {"東京23区":"tokyo","大阪市":"osaka","横浜市":"yokohama","福岡市":"fukuoka"}
WARD = {
 # 東京23区
 "千代田区":"chiyoda","中央区":"chuo","港区":"minato","新宿区":"shinjuku","文京区":"bunkyo",
 "台東区":"taito","墨田区":"sumida","江東区":"koto","品川区":"shinagawa","目黒区":"meguro",
 "大田区":"ota","世田谷区":"setagaya","渋谷区":"shibuya","中野区":"nakano","杉並区":"suginami",
 "豊島区":"toshima","北区":"kita","荒川区":"arakawa","板橋区":"itabashi","練馬区":"nerima",
 "足立区":"adachi","葛飾区":"katsushika","江戸川区":"edogawa",
 # 大阪市
 "都島区":"miyakojima","福島区":"fukushima","此花区":"konohana","西区":"nishi","大正区":"taisho",
 "天王寺区":"tennoji","浪速区":"naniwa","西淀川区":"nishiyodogawa","東淀川区":"higashiyodogawa",
 "東成区":"higashinari","生野区":"ikuno","旭区":"asahi","城東区":"joto","阿倍野区":"abeno",
 "住吉区":"sumiyoshi","東住吉区":"higashisumiyoshi","西成区":"nishinari","淀川区":"yodogawa",
 "鶴見区":"tsurumi","住之江区":"suminoe","平野区":"hirano",
 # 横浜市
 "神奈川区":"kanagawa","中区":"naka","南区":"minami","港南区":"konan","保土ケ谷区":"hodogaya",
 "保土ヶ谷区":"hodogaya","磯子区":"isogo","金沢区":"kanazawa","港北区":"kohoku","緑区":"midori",
 "青葉区":"aoba","都筑区":"tsuzuki","戸塚区":"totsuka","栄区":"sakae","泉区":"izumi","瀬谷区":"seya",
 # 福岡市
 "東区":"higashi","博多区":"hakata","城南区":"jonan","早良区":"sawara",
}
CATS = {"東京23区":"東京23区","大阪市":"大阪市","横浜市":"横浜市","福岡市":"福岡市"}

out, miss = [], set()
for r in R:
    w = r["区"].strip(); c = r["市"].strip()
    if w not in WARD: miss.add(w); continue
    slug = f"column-{CITY[c]}-{WARD[w]}"
    out.append({
      "id": int(r["ID"]), "slug": slug, "pref": r["都道府県"], "city": c, "ward": w,
      "title": r["コラムタイトル"].strip(), "lead": r["リード文"].strip(),
      "summary": r["風水サマリー"].strip(),
      "body1": r["本文（地形・歴史｜完成稿）"].strip(),
      "body2": r["本文（住まい選び｜完成稿）"].strip(),
      "keirei": r["形勢派風水解説"].strip(),
      "check": r["風水確認チェック"].strip(),
      "areas": [a.strip() for a in r["代表エリア"].replace("・","／").split("／") if a.strip()],
      "caution": r["注意点"].strip(),
      "seoTitle": r["SEOタイトル"].strip(),
      "seoDesc": r["メタディスクリプション"].strip(),
      "refs": [u.strip() for u in r["参考URL"].split("|") if u.strip()],
    })
if miss: print("⚠ 未対応の区:", miss)
json.dump(out, open("columns.json","w"), ensure_ascii=False)
print(f"{len(out)} 件を変換 / slug重複: {len(out)-len({o['slug'] for o in out})}")
import collections
for k,v in collections.Counter(o["city"] for o in out).items(): print(f"   {k}: {v}件")
