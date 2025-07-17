# Psychological Counseling Chatbot

[繁體中文](README_TW.md) | English

This project is a senior capstone project for the Department of Computer Science and Information Engineering, National Dong Hwa University, Academic Year 113.

## Project Preface

In recent years, artificial intelligence has become increasingly accessible and has gradually integrated into people’s daily lives. Among the most prominent advancements are large language models (LLMs). These models, after being trained on massive datasets and fine-tuned, are capable of understanding natural language. Common LLMs include ChatGPT by OpenAI, Gemini by Google, and Grok by X. Major tech companies are continuously optimizing their own LLMs, and the knowledge and capabilities of these AI systems are becoming increasingly powerful.

Modern LLMs can now solve over 90% of our everyday problems. In many domains, LLMs are also replacing conversational jobs. Many companies have fine-tuned LLMs to serve as online customer service agents, resolving user issues without human intervention—saving both communication and labor costs. Apple has also integrated "Apple Intelligence" into the iPhone, enabling the device to understand user needs through LLMs, perform on-device searches, and summarize relevant information to provide conclusions. These are just a few examples of how LLMs are making our lives more convenient.

## Project Introduction

This project is based on Retrieval-Augmented Generation (RAG), integrating Line Bot and a large language model to enable psychological counseling services to be accessible via mobile devices.

## Project Structure

```
.
├── chat_analyzed                                         # Storage for counseling summaries
│   └── 葉宸君
│       └── 葉宸君的諮詢整理.txt
├── chat_manager.py
├── chat_record                                           # Storage for chat records
│   └── 葉宸君
│       └── U73f67a10e169ac584ae0a22039b3afff.txt
├── files                                                 # Files used for RAG
│   ├── 57161915994.pdf
│   ├── 台灣輔導與諮商學會輔導與諮商專業倫理守則守則修訂說明.pdf
│   ├── 諮商心理師遇見案主挑戰下接納的心理歷程初探.pdf
│   ├── 手冊內頁單元5_0921.pdf
│   └── 輔導與諮商實務.pdf
├── google_sheet                                          # Script for Google Form (pre-counseling questionnaire)
│   └── test.js
├── line_bot.py                                           # Main program
├── llamaindex_merged.py                                  # RAG search module
├── package-lock.json
├── package.json
├── prompt.py                                             # Prompt settings for the counseling chatbot
└── template_message.py                                   # Bubble message format for Line Bot
```

## System Architecture

<img width="572" height="514" alt="Screenshot 2025-07-17 6:37:19 PM" src="https://github.com/user-attachments/assets/4b2dcf0b-17ee-4760-bac7-77a1660989f3" />

## Usage Flow

<img width="1113" height="223" alt="Screenshot 2025-07-17 6:38:45 PM" src="https://github.com/user-attachments/assets/266320d5-f54e-4376-b4a6-a910d83d752f" />
