import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from DataPrediction.predictNewData import predict_data

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_data")
async def get_data(request: Request):
    try:
        json = await request.json()  # Correctly call the json() method
        target_column = json["target_column"]
        # Ensure the return value is JSON serializable
        return {
            "data": predict_data(target_column).tolist()
        }  # Convert to list if necessary
    except KeyError:
        raise HTTPException(
            status_code=400, detail="Missing 'target_column' in request body"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
