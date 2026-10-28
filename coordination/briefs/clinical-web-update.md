# 新資料與網站內容工作指示
Codex統籌。使用者新增medorders/I&O/vitals/weight/units，並要求白話內容與供PGY/Fellow使用的Cloudflare網站。先讀 .private/case-brief.md 最後的 supplement v2，reports/clinical-summary.zh-TW.md，兩份專題報告及evidence/source-register.json；只用去識別brief，原始數字檔病歷與credentials禁止讀。
你是本輪clinical-update的唯一內容owner：reports/全部醫學內容（舊作者都done，Codex明確授權更新）、site/content/clinical.json、docs/case-questions.md（deidfacts）。不可碰site其他檔、scripts/tests/.claude/git/Cloudflare。用已下載的官方NovoRapid EMA PDF（fulltext/label_ema_novorapid_epar_pi.pdf）和既有全文，必要時Web查官方sources；病歷不得送外部PDF解析。
先盡快產出 site/content/clinical.json，契約：
{
"title":"DKA 床邊判讀","audience":"PGY / Fellow","updated":"2026-10-28",
"overview": ["白話段落..."],
"metrics":[{"label":"...","value":"...","unit":"...","note":"...","status":"known|caution|unknown"}],
"topics":[{"id":"calcium-phosphate|sodium|potassium|fluids|insulin","title":"...","summary":"...","body":["白話段落"],"fellow":["精確醫學深讀段落"],"takeaway":"...","sourceIds":["S02"]}],
"timeline":[{"day":"Day 0","title":"...","items":["..."]}],
"medications":[{"name":"...","order":"...","evidence":"order|user-confirmed|recorded","teaching":"..."}],
"io":{"label":"僅貼出片段...","inputMl":2946,"urineMl":2050,"differenceMl":896,"caveats":["..."]},
"known":["..."],"unknown":["..."],
"quizzes":[{"id":"...","question":"...","options":["..."],"answer":0,"explanation":"...","sourceIds":["S02"]}],
"references":[{"id":"S02","title":"...","url":"https://doi.org/..."}]
}
Public website不放MRN、真實case日期/醫師/機構/地點、本機paths、workflow內部log。Age寫40多歲男性；保留104.5kg計算需要。所有Day0/1/2一致。不要包含完整慢性藥清單識別細節，可只列與DKA教學相關orders。
臨床必修：
1.P單位已確認mg/dL，1.3→1.6=0.42→0.52mmol/L，不能再說unknown。
2.有CaCl2、IVKCl和oralK-Glu藥囑，不能再說無證據有補充醫囑；order!=已給完，CaCl2salt vs elemental不同，QID80+STAT20+IV20不能無MAR直接稱全給120/day。
3.體重104.5，insulin50/500=0.1U/mL，20–30mL/h=2–3U/h，目前2；0.019/0.029U/kg/h。比0.05參考低不能直接建議增速，K3.4與latestBOHB仍是限制。液體vehicle480–720mL/day算術需放入總fluid討論。
4.藥囑列NovoRapidFlexPen，但EMA支援IV用vial；核對實際產品與藥局配製，不能由order顯示名直接判error。EMA配方0.05–1U/mL/指定容器24h、起始adsorption，20mL/h500mL需25h，需核對hangtime不是宣告已超時。
5.I/O片段條件式2946 in/2050urine/+896，不混固體未知units、不稱24h、不算mL/kg/h。最新BP149/86HR85RR18及有進食可知；仍缺consciousness、完整MAR、latestCr/BOHB/ionizedCa/ISE。
6.Bloodketone大多可能BOHB但需分析物確認，不能引用reference就當已confirmed。舊DKAresolution與Na/pseudohyponatremia、K安全及Toujeo限制維持；老文獻不捏造最新research。
先JSON後更新白話summary/時間軸/專題內文/clinical-review.md新增supplement更動紀錄；過去版本的歷史mailbox不要改。不要再寫一大堆過時「缺weight/無vitals無進食」；用明確「已知/仍待核對」替換。白話要連貫，sources保留可點擊3–6。完成訊息到codex自己的新JSON、停下不用舊workflowmanifest，Codex重驗收hash。
