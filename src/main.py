import uuid
import numpy
import datetime
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

class questionModel(BaseModel):
    size: int          # Required

class answerModel(BaseModel):
    uid: str           # Required
    answer: int        # Required

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

matrixProblems = {}

# 問題のデータ
class problemData():
    def __init__(self, start, answer):
        self.start = start
        self.answer = answer

def generateMatrix(n): # n×nの行列を生成する関数
    listMatrix = [] # 行列を初期化
    matrix = numpy.random.randint(0, 9, (n, n))
    for line in matrix:
        listMatrix.append(list(line))
    return matrix, listMatrix

def calculateDeterminant(matrix): # 行列式を計算する関数
    return int(round(numpy.linalg.det(matrix)))

def generateProblem(n): # 問題を生成する関数
    if n < 2:
        return False, "Matrix size must be greater than or equal to 2."
    elif n > 20:
        return False, "Matrix size too large. Please specify a size of 20 or less."
    else:
        matrix, matrixProblem = generateMatrix(n)
    matrixAnswer = calculateDeterminant(matrix) # determinantを計算
    problemUid = str(uuid.uuid4())
    now = datetime.datetime.now()
    matrixProblems[problemUid] = problemData(now, matrixAnswer) # {"START": now, "ANSWER": matrixAnswer} 問題を登録
    return problemUid, matrixProblem # matrixProblemはLISTで返す

def checkAnswer(uid, answer): # 答えをチェックする関数
    if uid in matrixProblems:
        dataAsset = matrixProblems[uid]
        del matrixProblems[uid] # データ消去
    else:
        return None, None, None
    # 比較用
    userAnswer = int(answer)
    # 開始時刻と、解答を取得
    timestamp = dataAsset.start
    comAnswer = dataAsset.answer
    # 時間差
    now = datetime.datetime.now()
    answerTime = now - timestamp
    # String
    answerTimeString = str(answerTime.total_seconds())
    comAnswerString = str(comAnswer)
    if userAnswer == comAnswer:
        return True, answerTimeString, comAnswerString
    else:
        return False, answerTimeString, comAnswerString

# API Endpoint
@app.post("/matrix/question")
async def question(qm: questionModel):
    matrixSize = qm.size
    problemUid, problem = generateProblem(matrixSize)
    if not problemUid:
        return {"status": False, "message": str(problem), "question": None} 
    else:
        return {"status": True, "message": None, "question": {"uid": problemUid, "matrix": str(problem)}}

@app.post("/matrix/answer")
async def answer(am: answerModel):
    uid = am.uid
    userAnswer = am.answer
    status, time, comAnswer = checkAnswer(uid, userAnswer)
    if status is None:
        return {"status": False, "correct": None, "message": "Problem is not found.", "data": None}
    elif status:
        return {"status": True, "correct": True, "message": None, "data": {"time": time, "answer": comAnswer}}
    elif not status:
        return {"status": True, "correct": False, "message": None, "data": {"time": time, "answer": comAnswer}}
        
uvicorn.run(app, host="0.0.0.0", port=10000)
