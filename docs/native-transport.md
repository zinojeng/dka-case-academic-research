# Native cross-session transport

依官方 cross-session messaging，獨立 `--bg` session 可用 **ListAgents** 找到同機 session、用 **SendMessage** 傳訊；不需 experimental team flag。**不要修改全域 inbound policy。**

## 兩層、分開記錄
| 層 | 什麼 | 記錄方式 |
|---|---|---|
| transport | SendMessage 呼叫是否成功送出（delivered / failed / peer-not-found） | `message send --kind transport --channel native --peer '<display name>' --transport-result ...` |
| application ACK | 對方**實際回覆**確認內容 | `message send --kind ack --channel native --reply-to <transport id>` |

SendMessage 成功 ≠ 對方已處理；沒收到回覆就沒有 ACK。file mailbox（`coordination/messages/`）是 durable fallback 與 audit trail，所有重要內容仍需寫入。

## Preflight（`dispatch|resume --native-preflight`）
prompt 會要求 session：
1. ListAgents，只在本專案 peers 中尋找：plan `native_messaging.peer_roles` 所列角色的 `display_name`（由 prompt 注入，排除自己；名稱永遠取自 plan，不另維護名單）。
2. 對**一個** peer SendMessage 一則 scoped ping 請求 ACK（不含 PHI、路徑、憑證）。
3. 記錄 transport 結果；收到回覆另記 ACK。

## 迴圈防護
- 每個 sender→peer 最多 **2** 次 native exchange（`native_messaging.max_exchanges_per_peer`）；第 3 筆 transport 記錄會被 `workflow.py` 拒絕，session 必須改用 file mailbox。
- 收到 ping 的一方只回一次 ACK，不得再 ping 回去。
- 臨床討論由 clinical 角色自己進行；workflow-builder 只做一次 preflight ping。
