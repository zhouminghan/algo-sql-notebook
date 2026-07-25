"""
每日一题 - FastAPI 后端
本地 Docker 部署，浏览器刷题。
"""
import json
import os
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# ── Config ──────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://algo:algo123@localhost:5432/algo_practice")
PROBLEMS_DIR = Path("/app/problems")
FRONTEND_DIR = Path("/app/frontend")
OUTPUT_DIR = Path("/app/output")
PROGRESS_FILE = OUTPUT_DIR / "progress.json"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI(title="每日一题", version="1.0.0")

# ── Static files ────────────────────────────────────────
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
app.mount("/lib", StaticFiles(directory=str(FRONTEND_DIR / "lib")), name="lib")


# ── Progress helpers ────────────────────────────────────
def load_progress() -> dict:
    """加载刷题进度 JSON"""
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {}


def save_progress(progress: dict) -> None:
    """保存刷题进度 JSON"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def init_progress_file() -> None:
    """首次启动时从 problems/ 目录初始化进度文件"""
    if PROGRESS_FILE.exists():
        return

    progress = {"algo": {}, "sql": {}, "meta": {"started": str(date.today()), "last_active": str(date.today())}}

    algo_dir = PROBLEMS_DIR / "algo"
    if algo_dir.exists():
        for f in sorted(algo_dir.glob("*.md")):
            pid = f.stem  # e.g. "001-两数之和"
            progress["algo"][pid] = {"status": "pending", "attempts": 0, "notes": ""}

    sql_dir = PROBLEMS_DIR / "sql"
    if sql_dir.exists():
        for f in sorted(sql_dir.glob("*.md")):
            pid = f.stem  # e.g. "SQL01-连续登录天数"
            progress["sql"][pid] = {"status": "pending", "attempts": 0, "notes": ""}

    save_progress(progress)


# ── Startup ─────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    init_progress_file()


# ── Pages ───────────────────────────────────────────────
@app.get("/")
async def home():
    """首页：题目列表 + 进度"""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/algo/{problem_id}")
async def algo_page(problem_id: str):
    """算法题详情页"""
    html_path = OUTPUT_DIR / "algo" / f"{problem_id}.html"
    if not html_path.exists():
        # 回退：显示原始 markdown（render.py 未运行时）
        md_path = PROBLEMS_DIR / "algo" / f"{problem_id}.md"
        if not md_path.exists():
            raise HTTPException(status_code=404, detail=f"题目不存在: {problem_id}")
        return FileResponse(FRONTEND_DIR / "algo" / "fallback.html")

    return FileResponse(html_path)


@app.get("/sql/{problem_id}")
async def sql_page(problem_id: str):
    """SQL 题详情页"""
    html_path = OUTPUT_DIR / "sql" / f"{problem_id}.html"
    if not html_path.exists():
        md_path = PROBLEMS_DIR / "sql" / f"{problem_id}.md"
        if not md_path.exists():
            raise HTTPException(status_code=404, detail=f"题目不存在: {problem_id}")
        return FileResponse(FRONTEND_DIR / "sql" / "fallback.html")

    return FileResponse(html_path)


# ── API: Progress ───────────────────────────────────────
@app.get("/api/progress")
async def get_progress():
    """获取完整进度"""
    return load_progress()


@app.post("/api/progress/{problem_type}/{problem_id}")
async def update_progress(
    problem_type: str,
    problem_id: str,
    status: str = Query(..., regex="^(pending|doing|done|review)$"),
    notes: str = Query(""),
):
    """更新单题进度"""
    progress = load_progress()
    if problem_type not in progress or problem_id not in progress.get(problem_type, {}):
        raise HTTPException(status_code=404, detail="题目不存在")

    progress[problem_type][problem_id]["status"] = status
    progress[problem_type][problem_id]["notes"] = notes
    progress["meta"]["last_active"] = str(date.today())
    save_progress(progress)
    return {"ok": True}


# ── API: SQL Execute ────────────────────────────────────
@app.post("/api/sql/execute")
async def execute_sql(sql: str = Query(..., description="要执行的 SQL")):
    """执行 SQL 查询（用户前端输入）"""
    # 安全限制：只允许 SELECT
    sql_stripped = sql.strip().upper()
    if not sql_stripped.startswith("SELECT"):
        raise HTTPException(status_code=400, detail="仅允许 SELECT 查询")

    try:
        async with SessionLocal() as session:
            result = await session.execute(text(sql))
            rows = result.fetchall()
            columns = list(result.keys())

            # 限制返回行数
            if len(rows) > 1000:
                rows = rows[:1000]

            return {
                "columns": columns,
                "rows": [list(row) for row in rows],
                "row_count": len(rows),
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL 执行错误: {str(e)}")


# ── API: SQL Init Tables ────────────────────────────────
@app.post("/api/sql/init-tables")
async def init_tables():
    """执行 db/init/ 下的所有 SQL 初始化脚本"""
    init_dir = Path("/app/db/init")
    if not init_dir.exists():
        return {"ok": True, "message": "无初始化脚本"}

    results = []
    async with SessionLocal() as session:
        for sql_file in sorted(init_dir.glob("*.sql")):
            try:
                content = sql_file.read_text(encoding="utf-8")
                await session.execute(text(content))
                results.append({"file": sql_file.name, "status": "ok"})
            except Exception as e:
                results.append({"file": sql_file.name, "status": "error", "error": str(e)})

        await session.commit()

    return {"ok": True, "results": results}


# ── API: Problem List ──────────────────────────────────
@app.get("/api/problems")
async def list_problems():
    """按需加载题目列表（用于前端列表渲染）"""
    progress = load_progress()

    algo_list = []
    algo_dir = PROBLEMS_DIR / "algo"
    if algo_dir.exists():
        for f in sorted(algo_dir.glob("*.md")):
            pid = f.stem
            algo_list.append({
                "id": pid,
                "title": pid.split("-", 1)[-1] if "-" in pid else pid,
                "type": "algo",
                "status": progress.get("algo", {}).get(pid, {}).get("status", "pending"),
            })

    sql_list = []
    sql_dir = PROBLEMS_DIR / "sql"
    if sql_dir.exists():
        for f in sorted(sql_dir.glob("*.md")):
            pid = f.stem
            sql_list.append({
                "id": pid,
                "title": pid.split("-", 1)[-1] if "-" in pid else pid,
                "type": "sql",
                "status": progress.get("sql", {}).get(pid, {}).get("status", "pending"),
            })

    return {
        "algo": algo_list,
        "sql": sql_list,
        "meta": progress.get("meta", {}),
    }


# ── Health ──────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {"status": "ok", "date": str(date.today())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
