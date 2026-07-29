# -*- coding: utf-8 -*-
"""物件CSV → properties.js"""
import csv, io, json, re, subprocess

raw = open("/mnt/user-data/uploads/注目高級物件リスト_2026-07-29.csv","rb").read().decode("utf-8-sig")
R = list(csv.DictReader(io.StringIO(raw)))

DEG = {"北":0,"北東":45,"東":90,"南東":135,"南":180,"南西":225,"西":270,"北西":315}

# 東京23区の区名 → エンジンの区ID
TOKYO = json.loads(subprocess.run(["node","-e",
  "require('/mnt/user-data/outputs/subjects.js');console.log(JSON.stringify(Subjects.wards.map(w=>[w.name,w.id,w.en])))"],
  capture_output=True,text=True).stdout)
WID = {n:(i,e) for n,i,e in TOKYO}

# カード用の画像キー
IMGK = {"東京都":{"港区":"minato","千代田区":"chiyoda","渋谷区":"shibuya","目黒区":"meguro","世田谷区":"setagaya"},
        "大阪府":{}, "神奈川県":{}, "福岡県":{}}
CITY_IMG = {"東京都":"tokyo","大阪府":"osaka","神奈川県":"yokohama","福岡県":"fukuoka"}

def yen(n):
    n = int(n)
    oku, man = n // 10**8, (n % 10**8) // 10**4
    return (f"{oku}億{man:,}万円" if oku and man else f"{oku}億円" if oku else f"{man:,}万円")

out = []
for i, r in enumerate(R):
    pref, city, ward = r["都道府県"], r["市"], r["区"]
    m = re.match(r"(\d{4})年(\d{1,2})月", r["築年月"] or "")
    built = int(m.group(1)) if m else None
    face = r["方角"].strip()
    price_n = int(r["販売価格_円"]) if r["販売価格_円"].strip().isdigit() else None
    area = float(r["面積_㎡"]) if r["面積_㎡"].strip() else None
    tokyo = pref == "東京都"
    out.append({
      "id": f"p{i+1:04d}",
      "pref": pref, "city": city, "ward": ward,
      "wardId": WID.get(ward,[None])[0] if tokyo else None,
      "rank": int(r["区内選定順位"] or 0),
      "name": r["物件名"].strip(),
      "price": yen(price_n) if price_n else r["販売価格"],
      "priceN": price_n,
      "addr": r["所在地"].strip(),
      "st": r["最寄駅"].strip(), "walk": r["徒歩分数"].strip(),
      "layout": r["間取り"].strip(),
      "area": area,
      "built": built, "builtLabel": r["築年月"].strip(),
      "face": face, "deg": DEG.get(face),
      "url": r["物件URL"].strip(),
      "img": (IMGK.get(pref,{}).get(ward) or CITY_IMG.get(pref,"tokyo")),
      "tsubo": round(price_n / (area/3.30578)) if price_n and area else None,
    })

json.dump(out, open("props.json","w"), ensure_ascii=False)
print(f"{len(out)} 件を変換")
print("東京23区:", sum(1 for o in out if o['pref']=='東京都'), "／ 区IDの解決:",
      sum(1 for o in out if o['wardId']))
print("方角の解決:", sum(1 for o in out if o['deg'] is not None), "/", len(out))
print("築年の解決:", sum(1 for o in out if o['built']), "/", len(out))
print("坪単価の例:", [f"{o['name'][:12]} {o['tsubo']//10000}万円/坪" for o in out[:3] if o['tsubo']])
