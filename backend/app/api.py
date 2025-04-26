from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path


app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

'''
# Get the path to frontend build directory
frontend_build_path = Path(__file__).resolve().parents[2] / "frontend" / "dist"
app.mount("/assets", StaticFiles(directory=str(frontend_build_path / "assets")), name="static")
# Serve index.html for any other route
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_frontend(full_path: str, request: Request):
    # If path starts with /api, return 404
    if full_path.startswith("api/"):
        return HTMLResponse(status_code=404)
        
    # Read the index.html file and return it
    html_file = frontend_build_path / "index.html"
    if html_file.exists():
        with open(html_file) as f:
            return f.read()
    else:
        return HTMLResponse("Frontend build not found. Run 'npm run build' in frontend directory.", status_code=404)
'''

# API root
@app.get("/api", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list API."}

todos = [
    {
        "id": "1",
        "item": "Read some books."
    },
    {
        "id": "2",
        "item": "Cycle around in Iowa."
    }
]
@app.get("/api/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }

@app.post("/api/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": { "Todo added." }
    }

@app.put("/api/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }

@app.delete("/api/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
