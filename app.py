from flask import Flask, render_template, request
import calendar
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # 1. 현재 날짜 가져오기 (기본값)
    now = datetime.now()
    year = request.args.get('year', default=now.year, type=int)
    month = request.args.get('month', default=now.month, type=int)

    # 2. 달력 데이터 생성
    cal = calendar.monthcalendar(year, month)
    
    return render_template('index.html', year=year, month=month, cal=cal)

if __name__ == '__main__':
    # host='0.0.0.0'을 설정해야 같은 와이파이 내 다른 기기에서 접속 가능
    app.run(host='0.0.0.0', port=5000, debug=True)