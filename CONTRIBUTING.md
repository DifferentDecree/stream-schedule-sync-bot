# Contributing

## Branching Strategy

- **main** -> Protected, always stable, triggers GitHub Actions
- **develop** -> Protected, active development
- **feature/** -> Feature branches created from develop
- **hotfix/** -> Emergency fixes from main

## Feature workflow

1. Create `feature/*` branch from `develop`
2. Develop locally, commit changes
3. Push branch to fork
4. Open PR -> target `develop`
5. Required: 1 approval + Code Owner review
6. Merge into `develop`
7. Merge `develop` -> `main` for release
8. Tag release (`get tag -a vX.X.X -m "Release notes"`)
9. Optional: GitHub Release Notes

## CODEOWNERS

- All PRs require approval from `@DifferentDecree` (CODEOWNERS)
- Located at `.github/CODEOWNERS`
- Cannot be modified without PR review

---

**Author:** DifferentDecree