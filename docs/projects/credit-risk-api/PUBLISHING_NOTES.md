# Publishing notes — Credit Risk Scoring API

## ZIP contents
- `index.html`: standalone project detail page.
- `assets/architecture.svg`: architecture diagram.
- `project-card-snippet.html`: card markup for the project listing.
- `PUBLISHING_NOTES.md`: these instructions.

## Extraction
Extract the ZIP at the root of your repository (`my-ai-ml-project-library/`).
It creates `docs/projects/credit-risk-api/index.html` and its `assets/` folder.
It does not overwrite your API source code or existing project README.

## Add the project to the library home page
Open `docs/index.html`, find the existing project-card grid, and insert the contents of `project-card-snippet.html` alongside the other cards. The link is relative to `docs/index.html`: `projects/credit-risk-api/`. If your site uses different card CSS classes, adapt the wrapper to match a neighboring card.

## Publish from repository root
```powershell
git status
git add docs/projects/credit-risk-api/index.html docs/projects/credit-risk-api/assets/architecture.svg docs/projects/credit-risk-api/project-card-snippet.html docs/projects/credit-risk-api/PUBLISHING_NOTES.md docs/index.html
git commit -m "Publish credit risk scoring API project page"
git push origin main
```

## Accuracy notes
- Metrics are from the logged MLflow run on the held-out 6,000-row test set.
- Dataset: UCI Default of Credit Card Clients, ID 350; existing card clients in Taiwan.
- Model: StandardScaler + LogisticRegression in a scikit-learn Pipeline.
- The 0.30 threshold is exploratory and not business-approved.
- MANUAL_REVIEW and LOW_RISK are prototype routing labels, not approval/rejection outcomes.
- No claim is made that the API is publicly deployed or production-ready.
