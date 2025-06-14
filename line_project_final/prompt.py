import subprocess
import json

def assistant_prompt(user_name):
    # 使用 subprocess 調用 Node.js 腳本
    try:
        result = subprocess.run(
            ['node', './google_sheet/test.js', user_name],  # 調用 JS 文件並傳遞參數
            capture_output=True, text=True, encoding="utf-8"  # 指定輸出為 UTF-8
        )
        # 檢查腳本是否執行成功
        if result.returncode != 0:
            print(f"Node.js script error: {result.stderr}")
            return None

        # 將腳本的標準輸出（stdout）轉換為 JSON
        result_json = json.loads(result.stdout.strip())
        # 如果是錯誤訊息，直接返回
        if isinstance(result_json, dict) and "error" in result_json:
            print(f"Error: {result_json['error']}")
            return None
    except subprocess.CalledProcessError as e:
        # 捕獲執行錯誤
        print(f"Error calling Node.js script: {e.stderr}")
        return None
    except json.JSONDecodeError:
        # 捕獲 JSON 解析錯誤
        print(f"Error decoding JSON: {result.stdout}")
        return None

    # 構建 Prompt，從列表中提取資料
    try:
        profile = f"""
        患者的基本資料：   
        - 姓名 : {user_name}
        - 性別 : {result_json[2] if len(result_json) > 2 else '未提供'}
        - 最近的困擾 : {result_json[3] if len(result_json) > 3 else '未提供'}
        - 需要的協助 : {result_json[4] if len(result_json) > 4 else '未提供'}
        """
        prompt = f"""
        - 你是一名專業的心理諮商師，擅長傾聽與引導病人表達內心的感受，並在適當時機提供支持與建議。
        - 附上的檔案是一些心理諮商的技巧，請靈活運用。
        - 你的對話方式應該自然、親切，就像與朋友聊天一樣，而不是機械式地提供解決方案。
        - 如果患者表達負面情緒，請先**認同並安撫**，然後再試圖引導他進一步分享，而不是直接提供建議。
        - 當患者詳細描述問題後，**再根據他的需求提供適當的建議**，並確保這些建議是**個人化的**，而非條列式的通用建議。
        - 在對話中保持溫暖、自然的語氣，避免使用過於制式或生硬的回答，**讓病人感覺到你的真誠與耐心**。
        - 不要**在一開始就長篇大論地解釋解決方案**，而是**透過互動與病人一起尋找適合他的方式**。
        - 你的回覆字數長度應限制在100字以內。
        - 請務必以繁體中文回答。

        以下是患者的基本資料：

        - 姓名 : {user_name}
        - 性別 : {result_json[2] if len(result_json) > 2 else '未提供'}
        - 最近的困擾 : {result_json[3] if len(result_json) > 3 else '未提供'}
        - 需要的協助 : {result_json[4] if len(result_json) > 4 else '未提供'}
        """
        return prompt, profile
    except IndexError:
        print("Error: Data format is incorrect or missing fields.")
        return None

