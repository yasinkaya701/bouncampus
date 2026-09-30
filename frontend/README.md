# BOUNCAMPUS frontend

The production web application is the Next.js app in this directory. Vercel routes the public deployment to `frontend/`; by default the UI uses the co-located `/api/v1/*` Next.js routes.

## Local development

Requirements:

- Node.js `24.x`
- npm

```bash
npm ci
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

Leave `NEXT_PUBLIC_API_URL` empty to use the co-located Next.js API. Set it only when intentionally testing against a separately deployed FastAPI research service.

## Verification

Before integration, run:

```bash
npm run verify
```

This runs TypeScript checks, lint, and the production build. GitHub CI runs the same frontend gates on the exact PR head.

## Primary product surfaces

- `/` — KREATE command center
- `/food-waste` — core food-waste decision workspace
- `/food-waste/pilot` — measured pilot evidence workflow
- `/demo` and `/demo/jury` — jury presentation flow
- `/decisions` — human-review decision ledger
- `/data` — source provenance and truth boundary
- `/buildings` — campus building intelligence
- `/mobility` — source-backed shuttle workspace
- `/scenarios` — counterfactual scenario workspace
- `/courses` — course/schedule explorer
- `/lab` — explicitly non-jury experimental roadmap surface

Historical mock/synthetic code belongs under the repository-level `legacy/` directory and must not be imported into production code.

## Truth boundary

Do not present model estimates, synthetic datasets, or unavailable integrations as measured/live university telemetry. The product must distinguish official/public sources, model estimates, unavailable sources, and measured pilot evidence.
