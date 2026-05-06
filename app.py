from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client

app = Flask(__name__)

# [중요] 세션을 사용하기 위한 비밀키입니다. (관리자님만의 키로 설정)
app.secret_key = 'admin_secret_key_2026' 

# 1. Supabase 설정 (정확한 URL과 Key를 적용했습니다)
SUPABASE_URL = "https://dqizgoklyvdhqjtgpbj.supabase.co" 
SUPABASE_KEY = "sb_publishable_sPLJ04iTJNQtH6DB9NeTNQ_EBnN_A8_m_pE-Z1P0hV8pAnp7k9V8w" 

# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # [핵심] 세션에서 가입 여부(is_signed_up)를 가져옵니다. 없으면 False가 기본값입니다.
    is_signed_up = session.get('is_signed_up', False)
    
    # 지출 내역 날짜 설정 (기본값)
    year = request.args.get('year', '2026')
    month = request.args.get('month', '5')

    try:
        # DB에서 지출 내역 가져오기
        response = supabase.table("spending_list").select("*").execute()
        spendings = response.data
    except Exception:
        spendings = []

    # [핵심] HTML로 가입 여부(is_signed_up)를 전달합니다.
    return render_template('index.html', 
                           is_signed_up=is_signed_up, 
                           spendings=spendings, 
                           current_year=year, 
                           current_month=month)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Supabase 회원가입 실행
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        
        if auth_response.user:
            # [핵심] 가입 성공 시 세션에 신호를 기록합니다. 이 신호가 버튼을 숨깁니다.
            session['is_signed_up'] = True 
            # 알림창에 뜰 문구를 예약합니다.
            flash("회원가입이 완료되었습니다!") 
            return redirect(url_for('index'))
            
    except Exception as e:
        flash("가입 중 오류가 발생했습니다.")
        print(f"Error: {e}")
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # 로그아웃 시 세션 삭제 (다시 버튼이 나타나게 됩니다)
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 관리자님 로컬 서버 실행
    app.run(debug=True, port=5000)
