from fastapi import FastAPI
from pydantic import BaseModel
from detector.secure_prompt_advanced import run_secure_prompt_filter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    masked_prompt: str

@app.post("/api/filter", response_model=PromptResponse)
def filter_prompt(prompt: PromptRequest):
    masked = run_secure_prompt_filter(prompt.prompt)
    return {"masked_prompt": masked}
