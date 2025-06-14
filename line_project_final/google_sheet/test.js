const { GoogleSpreadsheet } = require('google-spreadsheet');
const { JWT } = require('google-auth-library');

/**
 * 從 Google Sheet 獲取資料
 * @param  {string} docID - Google Sheet 文件 ID
 * @param  {number} sheetID - Google Sheet 工作表 ID
 * @param  {string} credentialsPath - 認證檔案路徑
 * @returns {Promise<Array>} - 取得的資料陣列
 */
async function getData(docID, sheetID, credentialsPath = './line-bot-444415-c29cfc3090d0.json') {
  const result = [];
  const creds = require(credentialsPath);

  // 使用 google-auth-library 建立 JWT 驗證
  const serviceAccountAuth = new JWT({
    email: creds.client_email,
    key: creds.private_key.replace(/\\n/g, '\n'), // 處理可能的換行符號
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  });

  // 建立 GoogleSpreadsheet 實例並注入認證
  const doc = new GoogleSpreadsheet(docID, serviceAccountAuth);

  await doc.loadInfo(); // 載入 Google Sheet 資訊
  const sheet = doc.sheetsById[sheetID]; // 根據 sheet ID 獲取特定工作表
  const rows = await sheet.getRows(); // 獲取所有列

  for (const row of rows) {
    result.push(row._rawData); // 收集資料
  }

  return result;
}

/**
 * 主函數：根據名稱篩選資料（從最新的開始搜尋）
 * @param {string} targetName - 目標名稱
 * @returns {Promise<string>} 符合條件的完整資料列
 */
async function return_sheet(targetName) {
  const docID = '1n6w9qnz68gwt4_ZdunQ6P2xDBXoxMl9isyHN5HnxTA4';
  const sheetID = 1537196834;

  try {
    const data = await getData(docID, sheetID);

    // 從最後一筆資料開始搜尋
    const filteredData = [...data].reverse().find(
      row => Array.isArray(row) && typeof row[1] === 'string' && row[1].trim() === targetName.trim()
    );

    if (filteredData) {
      console.log(JSON.stringify(filteredData)); // 僅輸出 JSON 結果
    } else {
      console.log(JSON.stringify({ error: "未找到符合條件的資料" })); // 輸出錯誤訊息
    }
  } catch (err) {
    console.error(JSON.stringify({ error: err.message })); // 輸出錯誤訊息
  }
}

// 如果直接執行此文件，處理參數
if (require.main === module) {
  const targetName = process.argv[2]; // 從命令列獲取目標名稱
  return_sheet(targetName);
}

module.exports = { return_sheet, getData };