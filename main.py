import logging
import os
import time
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request, HTTPException
import mysql.connector
import uvicorn

#로그 저장
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)

#로그 포맷 및 핸들러 설정
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

formatter = logging.Formatter(LOG_FORMAT)

file_handler = RotatingFileHandler(
    filename="logs/app.log",
    encoding="utf-8",
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('애플리케이션이ㅣ 시작되었습니다.')

app = FastAPI()

def get_db():
    con = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="tester",
        password="1234",
        database="test_db"
    )
    return con

"""
def get_db():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="tester",
                password="1234",
                database="test_db"
            )
            return conn
        except mysql.connector.Error as err:
            print(f"접속 대기 중... 남은 시도: {retries} (에러: {err})")
            retries -= 1
            time.sleep(5)  # 5초 대기 후 재시도
    raise Exception("DB 접속에 최종 실패했습니다.")
"""



# ---------------------------
# CREATE
# ---------------------------
@app.post("/todos")
async def create_todo(request: Request):
    body = await request.json()
    content = body.get("content")

    if not content:
        logging.error('제목 없는 할 일 생성 시도')
        raise HTTPException(status_code=400, detail="content is required")

    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # INSERT 문 작성
    # 예: INSERT INTO todo (content) VALUES (%s)
    cursor.execute(
        ### TODO: 여기에 INSERT SQL 작성 ###
        "INSERT INTO todo (content) VALUES (%s)",
        (content,)
    )
    conn.commit()

    todo_id = cursor.lastrowid

    # 👉 학생이 작성해야 하는 SQL
    # SELECT 문 작성하여 방금 만든 todo 조회
    cursor.execute(
        ### TODO: 여기에 SELECT SQL 작성 ###
        "SELECT id, content, created_at FROM todo WHERE id = %s",
        (todo_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    logging.debug(f'새로운 할 일 생성 완료: ID{todo_id}')
    print(todo_id)

    return {
        "id": row[0],
        "content": row[1],
        "created_at": str(row[2])
    }


# ---------------------------
# READ
# ---------------------------
@app.get("/todos")
def get_todos():
    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # 전체 todo 조회 SELECT 문 작성
    cursor.execute(
        ### TODO: 여기에 전체 조회 SELECT SQL 작성 ###
        "SELECT id, content, created_at FROM todo"
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": r[0],
            "content": r[1],
            "created_at": str(r[2])
        }
        for r in rows
    ]


# ---------------------------
# DELETE
# ---------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # 삭제 DELETE 문 작성
    cursor.execute(
        ### TODO: 여기에 DELETE SQL 작성 ###
        "DELETE FROM todo WHERE id = %s",
        (todo_id,)
    )
    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)