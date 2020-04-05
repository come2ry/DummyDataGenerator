import json

s = """
[
		"IT・ソフトウェア",
		"通信",
		"WEB",
		"教育",
		"VC・起業支援",
		"ゲーム",
		"コンサルティング",
		"スポーツ",
		"ファッション・アパレル",
		"ホテル・ブライダル",
		"メーカー",
		"メディア・出版",
		"流通・小売",
		"運輸・物流",
		"教育",
		"金融",
		"広告・PR",
		"商社",
		"人材",
		"医療・福祉",
		"農業",
		"不動産・建築",
		"士業",
		"旅行・レジャー",
		"飲食",
		"官公庁",
		"NPO・ボランティア",
		"エンタメ・芸能",
		"その他サービス"
	]
"""
l = s.strip().replace("\n", "").replace("[", "").replace("]", "").replace("\t", "").replace('"', "").split(",")
d = dict((str(i), l[i]) for i in range(len(l)))
jt = json.dumps(d, ensure_ascii=False)

print(jt)