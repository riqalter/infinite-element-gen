from fastapi import FastAPI, HTTPException, APIRouter
from cache import get_cached_response, cache_response
from models import CraftingRequest, CraftingResponse
from ai import generate_craft
import fastapi_swagger_dark as fsd
import json

app: FastAPI = FastAPI(
    title="Element Craft API",
    description="An API for generating whimsical crafting combinations using AI.",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"}
    },
    docs_url=None
)

router: APIRouter = APIRouter(
    prefix="/api/v1",
    tags=["Crafting"]
)
app.include_router(router)

# penghitaman swagger ui
fsd.install(app, path="/api/docs") # type: ignore

@app.post("/api/v1/craft", response_model=CraftingResponse, tags=["Crafting"])
def combine_elements(req: CraftingRequest) -> CraftingResponse:
    cached = get_cached_response(req.first_element, req.second_element)
    if cached:
        print(f"Cache hit for {req.first_element} and {req.second_element}")
        return json.loads(cached) # type: ignore
    else:
        print(f"Cache miss for {req.first_element} and {req.second_element}")
    
    try:
        genai_response: str | None = generate_craft(req.first_element, req.second_element)
        parsed = json.loads(genai_response) # type: ignore
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )
    
    cache_response(req.first_element, req.second_element, parsed)
    
    return parsed

@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {
        "message": "Visit /api/docs for API documentation."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, use_colors=True, reload=True)