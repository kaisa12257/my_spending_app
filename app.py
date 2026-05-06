from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# [1. Supabase 설정]
SUPABASE_URL = "https://dqizgoklyvdhqtjtgpbj.supabase.co"
# image_e4dc3b.png에서 복사한 키를 여기에 넣으세요.
SUPABASE_KEY = "sb_publishable_sPLJ04iTJNQtH6DB9NeTNQ_EBnN_..." 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# [2. 메인 페이지 라우팅] - 이 부분이 추가되어야 404 에러가 사라집니다!
@app.route('/')
def index():
    # templates 폴더 안의 index.html을 읽어서 브라우저에 보여줍니다.
    return render_template('index.html')

# [3. API 서버 기능]
@app.route('/api/get_expenses', methods=['GET'])
def get_expenses():
    response = supabase.table("fixed_expenses").select("*").execute()
    return jsonify(response.data)

@app.route('/api/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    response = supabase.table("fixed_expenses").insert(data).execute()
    return jsonify(response.data)

@app.route('/api/delete_expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    supabase.table("fixed_expenses").delete().eq("id", expense_id).execute()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # 외부 접속 허용을 위해 host='0.0.0.0'을 추가하는 것이 좋습니다.
    app.run(host='0.0.0.0', port=5000, debug=True)
