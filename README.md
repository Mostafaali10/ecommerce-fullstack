# Full-Stack E-Commerce (Next.js + FastAPI)

Beginner-oriented monorepo: a **Next.js** storefront under `frontend/` and a **FastAPI** API under `backend/`. Arabic + English comments are used in the Python code to make learning easier.

---

## 1) Suggested repository name

Pick a name that states **what** it is and **who** it is for (learning vs production):

| Suggested name | Why |
|---------------|-----|
| **`commerce-stack-learning`** | Clear that it is a learning-oriented full stack. |
| **`next-fastapi-ecommerce-starter`** | Good for discoverability (tech stack in the name). |
| **`trendstyle-dev`** | Brand-style name if this is your portfolio app. |

Rename on GitHub: **Repository → Settings → General → Repository name**.

The link you mentioned (`Mostafaali10/-E-Commerce-Web-Application`) can stay as upstream; this folder layout matches a clean **fork** or **new repo** with the same features.

---

## 2) Full proposed folder structure

```text
project-root/
├── README.md                 # This file — how to run everything
├── .gitignore
│
├── backend/
│   ├── requirements.txt
│   ├── .env.example          # Copy to `.env` and edit
│   ├── ecommerce.db          # Created automatically when using SQLite (gitignored)
│   └── app/
│       ├── main.py           # FastAPI app + CORS + router includes
│       ├── database.py       # Engine, SessionLocal, Base
│       ├── core/
│       │   ├── config.py     # Settings from environment (.env)
│       │   └── security.py   # JWT helpers + HTTPBearer + admin dependency
│       ├── dependencies/
│       │   ├── database.py   # get_db() session per request
│       │   └── auth.py       # get_current_user_entity() for /users/me
│       ├── models/           # SQLAlchemy tables
│       ├── schemas/          # Pydantic request/response shapes
│       ├── routers/          # APIRouter modules (auth, users, products, …)
│       └── utils/            # Reserved for small shared helpers
│
└── frontend/
    ├── package.json
    ├── next.config.mjs
    ├── tsconfig.json         # "@/*" → "./src/*"
    ├── components.json       # shadcn-style paths
    └── src/
        ├── app/              # Next.js App Router
        │   ├── layout.tsx
        │   ├── page.tsx
        │   └── globals.css
        ├── components/
        │   ├── contexts/     # auth, cart, filters (client state)
        │   └── ui/           # Button, Card, … (Radix-based primitives)
        ├── hooks/
        └── lib/              # api.ts, constants, types, utils (cn)
```

Legacy folders (`app/` at repo root, duplicate `routers/`, typo `requirments/`) were removed so beginners only look at **`backend/app`** and **`frontend/src`**.

---

## 3) Quick start

### Backend (FastAPI)

```powershell
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

**Demo accounts (same behavior as before)**  
- Customer: `user@example.com` / `password123`  
- Admin: `admin@example.com` / `admin123`  

Register any email containing `admin` to get the **admin** role (demo rule in code).

### Frontend (Next.js)

```powershell
cd frontend
npm install
npm run dev
```

- App: `http://localhost:3000`

The UI still uses **local mock data** in `frontend/src/lib/api.ts` and **client contexts** for cart/auth (same idea as before). Wiring every page to the FastAPI backend can be your next learning step.

---

## 4) Environment variables (backend)

| Variable | Meaning |
|----------|---------|
| `DATABASE_URL` | SQLAlchemy URL (default SQLite file next to `backend/`). |
| `SECRET_KEY` | JWT signing secret — change for anything beyond local dev. |
| `ALGORITHM` | JWT algorithm (default `HS256`). |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime. |
| `CORS_ORIGINS` | Comma-separated origins, or `*` for quick tests. |

---

## 5) Database note (SQLite + new `stock` column)

The reorganized `Product` model includes a **`stock`** column used by products and orders. If you already had an old `ecommerce.db` **without** that column, either delete the file and restart, or run a proper migration (Alembic) — for learning, deleting the SQLite file is simplest.

---

## 6) What changed (high level)

- **Backend** moved under `backend/app` with `core/`, `dependencies/`, `routers/`, `models/`, `schemas/`.
- **JWT**: single source in `app/core/security.py`; settings in `app/core/config.py`.
- **Frontend** moved under `frontend/src` with `@/*` pointing at `src/*`; added **context providers** and **UI primitives** so imports like `@/components/ui/button` resolve.
- **Removed** unused duplicate routers at repo root and empty `requirments` folder.

---

## 7) Team / credits

Original README listed team members (Mariam, Salma, Nada, Alaa, Ahmed, etc.). Keep attributions in your course or portfolio if you reuse this template.
