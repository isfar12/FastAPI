from fastapi import FastAPI
import time

app = FastAPI()


@app.middleware("http")
async def request_time_counter(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"Request method {request.method} at path {request.url} processed in {process_time} seconds")
    return response


@app.get("/",)
def read_root():
    return {"message": "Hello World"}
