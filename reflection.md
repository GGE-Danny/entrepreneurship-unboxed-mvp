
# Technical Reflection

## 1) Code Structure
- Flask app with two main routes (`/match`, `/dashboard`)
- `data/investors.json` for quick iteration
- Minimal template for founder dashboard

## 2) Scaling to 100k Users
- Move to MSQL; use indexes for queries
- Cache hot queries with Redis
- Run behind Gunicorn + Nginx; add load balancer
- Background jobs for heavy tasks (RQ/Celery)
- Optionally migrate to Django or expand Flask with blueprints

## 3) Security/Financial Considerations
- Input validation & request size limits
- TLS in transit; encrypt sensitive data at rest
- RBAC for investor/founder access
- Audit logs & anomaly detection
- Compliance awareness (KYC/AML if handling funds)

## 4) Future AI Integration
- ML-based matching from historical success
- NLP on pitch text to enrich features
- Personalised actions on the dashboard
