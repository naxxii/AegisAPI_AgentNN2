from fastapi import FastAPI, HTTPException, Query
import os
app = FastAPI(title="Demo Service Mock")
DEMO_VERSION=os.getenv("DEMO_VERSION","v1")
USERS=[{"id":1,"userName":"alice","username":"alice","email":"alice@example.com"},
       {"id":2,"userName":"bob","username":"bob","email":"bob@example.com"}]
POSTS=[{"id":1,"title":"hello"},{"id":2,"title":"world"}]
@app.get("/users")
def list_users():
    if DEMO_VERSION=='v1':
        return {"items":[{"id":u["id"],"userName":u["userName"],"email":u["email"]} for u in USERS]}
    return {"items":[{"id":u["id"],"username":u["username"],"email":u["email"]} for u in USERS]}
@app.get("/users/{uid}")
def get_user(uid:int):
    for u in USERS:
        if u["id"]==uid:
            if DEMO_VERSION=='v1':
                return {"id":u["id"],"userName":u["userName"],"email":u["email"]}
            else:
                if uid==1: raise HTTPException(status_code=429, detail="slow down")
                return {"id":u["id"],"username":u["username"],"email":u["email"]}
    raise HTTPException(status_code=404, detail="not found")
@app.get("/posts")
def list_posts(limit: int | None = Query(default=None)):
    if DEMO_VERSION=='v2' and limit is None:
        raise HTTPException(status_code=400, detail="limit required")
    return POSTS
