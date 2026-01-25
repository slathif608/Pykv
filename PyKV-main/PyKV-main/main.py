from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os

from store import LRUCache
from persistence import append_log, recover_store, compact_log

# ==================== CONFIGURATION ====================
app = FastAPI(title="PyKV Store")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")

# IN-MEMORY STORE
kv_store = LRUCache(capacity=5)

# Recover persisted data on startup
recover_store(kv_store)

# ==================== DATA MODELS ====================
class KeyValue(BaseModel):
    key: str
    value: str
    ttl: Optional[int] = None


# ==================== UI ROUTES ====================
@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/stats-ui", response_class=HTMLResponse)
async def stats_page(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})


# ==================== API ROUTES ====================
@app.get("/stats")
async def get_stats():
    """Get current cache statistics"""
    return kv_store.stats()


@app.post("/set")
async def set_key(data: KeyValue):
    """Set a key-value pair with optional TTL"""
    print(f"DEBUG: Received POST /set with data: key={data.key}, value={data.value}, ttl={data.ttl}")
    try:
        # Store in cache
        print(f"DEBUG: Calling kv_store.set()")
        kv_store.set(data.key, data.value, data.ttl)
        print(f"DEBUG: kv_store.set() completed successfully")
        
        # Log the operation
        try:
            print(f"DEBUG: Calling append_log()")
            append_log("SET", data.key, data.value, data.ttl)
            print(f"DEBUG: append_log() completed successfully")
        except Exception as log_err:
            print(f"Warning: Failed to log SET operation: {log_err}")
        
        print(f"DEBUG: Returning success response")
        return {"message": "Key set successfully"}
    except Exception as e:
        print(f"Error in /set: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get/{key}")
async def get_key(key: str):
    """Get value by key"""
    value = kv_store.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}


@app.delete("/delete/{key}")
async def delete_key(key: str):
    """Delete a key from cache"""
    try:
        if key not in kv_store.cache:
            raise HTTPException(status_code=404, detail="Key not found")
        kv_store.delete(key)
        append_log("DELETE", key)
        return {"message": "Key deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/keys")
async def list_keys():
    """List all keys in cache"""
    return {"keys": kv_store.keys()}


@app.get("/all-data")
async def get_all_data():
    """Get all key-value pairs stored in cache"""
    all_pairs = []
    for key in kv_store.keys():
        value = kv_store.get(key)
        if value is not None:
            all_pairs.append({"key": key, "value": value})
    return {"data": all_pairs, "count": len(all_pairs)}


@app.get("/clear")
async def clear_cache():
    """Clear all data from cache"""
    kv_store.clear()
    return {"message": "Cache cleared successfully"}


@app.post("/compact")
async def compact_logs():
    """Compact the write-ahead log"""
    try:
        compact_log(kv_store)
        return {"message": "Log compacted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

