# 心理諮商機器人

繁體中文 | [English](README.md)

本項目為東華大學資工系113學年度畢業專題

## 項目前言
近幾年人工智慧愈發方便，也漸漸的融入人們的日常生活中，其中最常見的無非就是大語言模型。大語言模型為經過大量的訓練以及調適過後，能夠理解自然語意的模型，常見的大語言模型有 OpenAI 推出的 ChatGPT、Google 推出的 Gemini 以及 X 推出的 Grok 等。各家科技大廠都在不斷的調整並優化自家的大語言模型，人工智慧的知識量以及功能也日益強大。

現今的大語言模型已經可以解決我們日常超過九成的問題，在其他領域方面也看到大語言模型正在取代對談性的工作，許多廠商將大語言模型經過微調後成為了線上克服，無須真人回覆就可以解決用戶的問題，省下了通話費及人力費；Apple 也在 iPhone 加入 Apple Intelligence 的功能，能夠透過大語言模型理解用戶的需求，並直接在用戶的裝置內搜尋相關資訊，彙整後並給出結論。這些都是大語言模型正在逐漸便利我們生活的實例。

## 項目介紹
本項目基於強化檢索生成 (RAG)，結合 linebot 與大語言模型，達到在手機也可以使用到心理諮商的目的。

## 項目結構
```
.
├── chat_analyzed                                         # 諮商總結保存處
│   └── 葉宸君
│       └── 葉宸君的諮詢整理.txt
├── chat_manager.py
├── chat_record                                           # 對話紀錄保存處
│   └── 葉宸君
│       └── U73f67a10e169ac584ae0a22039b3afff.txt
├── files                                                 # RAG 文本放置處
│   ├── 57161915994.pdf
│   ├── 台灣輔導與諮商學會輔導與諮商專業倫理守則守則修訂說明.pdf
│   ├── 諮商心理師遇見案主挑戰下接納的心理歷程初探.pdf
│   ├── 手冊內頁單元5-0921.pdf
│   └── 輔導與諮商實務.pdf
├── google_sheet                                          # google 表單(心理諮商前導問卷)腳本
│   └── test.js
├── line_bot.py                                           # 主程式
├── llamaindex_merged.py                                  # RAG 搜尋部分
├── package-lock.json
├── package.json
├── prompt.py                                             # 諮商機器人 prompt
└── template_message.py                                   # linebot 氣泡訊息格式
```

## 系統架構
<img width="572" height="514" alt="截圖 2025-07-17 下午6 37 19" src="https://github.com/user-attachments/assets/4b2dcf0b-17ee-4760-bac7-77a1660989f3" />

## 使用流程
<img width="1113" height="223" alt="截圖 2025-07-17 下午6 38 45" src="https://github.com/user-attachments/assets/266320d5-f54e-4376-b4a6-a910d83d752f" />



