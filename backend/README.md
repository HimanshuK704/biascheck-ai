# BiasCheck AI — Render backend + React/Vite frontend

## Repository layout
- `backend/`: FastAPI analysis API for Render
- `render.yaml`: optional Render Blueprint configuration
- `FREEBUFF_PROMPT.md`: prompt to generate the React/Vite frontend

## 1. Deploy backend to Render
1. Push this repository to GitHub.
2. In Render, choose **New + → Web Service** and connect the repository.
3. Set **Root Directory** to `backend`.
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Health check path: `/health`
7. Deploy. Test `https://YOUR-SERVICE.onrender.com/health` and `/docs`.

For the first deployment, `FRONTEND_ORIGINS=*` permits requests from any origin. After deploying the frontend, change it to the exact frontend origin (for example, `https://your-site.example`) in Render environment variables and redeploy. Do not include a trailing slash in the origin.

## 2. Generate frontend in Freebuff
Use `FREEBUFF_PROMPT.md` as the build prompt. Export or push the generated React/Vite project into a `frontend/` folder (or a separate repository if that matches your existing workflow).

Create `frontend/.env` for local development:
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```
For a hosted frontend, set `VITE_API_BASE_URL` to your Render backend base URL in the frontend host's environment settings, then rebuild/redeploy.

## 3. Run backend locally
From the repository root:
```
python -m venv .venv
```
Windows PowerShell:
```
.\.venv\Scripts\Activate.ps1
```
Then:
```
pip install -r backend/requirements.txt
uvicorn main:app --reload --app-dir backend
```
- Health: `http://127.0.0.1:8000/health`
- Interactive API docs: `http://127.0.0.1:8000/docs`

## API
`POST /analyze`
```
{"text":"We need a young salesman."}
```

The API is stateless. It does not save submitted text. The rules are limited and explainable; matches require human review and must not be used to make automated hiring decisions.
