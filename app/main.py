from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from pymongo import MongoClient
import traceback
import base64

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>FAST API</title>
        </head>
        <body>
            <h1>FAST API</h1>
            <form method="post" action="/input/audio/" enctype="multipart/form-data">
            <p><input type="file" id="v_file" name="v_file" accept="audio/*" /></p>
            <button type="submit">送信</button>
            </form>
        </body>
        <script>
        const url = new URL(window.location.href);
        const params = url.searchParams;
        const message =params.get('message');
        if(message){ alert(message) }
        </script>
    </html>
    """

@app.post("/input/audio/", response_class=HTMLResponse)
async def inputAudio(v_file: UploadFile = Form(...)):
    try:
      # MongoDBへの接続
      client = MongoClient('mongodb://root:example@mongo:27017/')
      db = client.fileData

      file_content = await v_file.read()
      # Base64でエンコード
      encoded_file = base64.b64encode(file_content)
      post = {
            "filename": v_file.filename,
            "file": encoded_file.decode()
        }
      db.audio.insert_one(post)
      return RedirectResponse("http://localhost:8000?message=アップロード完了")
    except Exception as e:
      # 例外情報をログに記録
      traceback.print_exc()
      # HTTPレスポンスとしてエラーメッセージを返す
      raise HTTPException(status_code=500, detail=str(e))