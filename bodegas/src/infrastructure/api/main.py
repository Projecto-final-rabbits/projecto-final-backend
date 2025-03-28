from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
def healthcheck():
    return JSONResponse(content={"message": "OK"}, status_code=200)

@app.get("/test2")
def test2_healthcheck():
    return JSONResponse(content={"message": "OK"}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)