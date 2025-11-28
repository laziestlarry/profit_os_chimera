# Profit OS Chimera v0.1.0_Publish - Production Deployment Guide

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <repository-url>
cd profit_os_chimera

# Start services
./scripts/start.sh --with-frontend
```

### Docker Deployment

```bash
# Build and deploy
./scripts/deploy.sh production

# Or use docker-compose directly
cd infrastructure/docker
docker-compose up -d
```

### API Access

- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **Frontend:** http://localhost:8501

---

## Architecture

### Components

1. **API Server** (FastAPI)
   - RESTful endpoints
   - Job orchestration
   - KPI evaluation
   - Play triggering

2. **Database** (SQLAlchemy)
   - SQLite (development)
   - PostgreSQL (production ready)

3. **Frontend** (Streamlit)
   - Dashboard interface
   - Company management
   - KPI visualization
   - Cycle execution

4. **Core Engine**
   - Agent system
   - Playbook evaluation
   - Evidence logging

---

## Production Deployment

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (for production)
- Domain name (optional)
- SSL certificate (for HTTPS)

### Steps

1. **Configure Environment**
   ```bash
   export DATABASE_URL="postgresql://user:pass@host:5432/profit_os"
   export API_ENV="production"
   export SECRET_KEY="your-secret-key"
   ```

2. **Deploy**
   ```bash
   ./scripts/deploy.sh production
   ```

3. **Verify**
   ```bash
   curl http://localhost:8000/api/health
   ```

### Cloud Deployment Options

#### AWS
- Use ECS/Fargate for containers
- RDS for PostgreSQL
- ALB for load balancing
- CloudFront for CDN

#### Google Cloud
- Cloud Run for containers
- Cloud SQL for database
- Cloud Load Balancing

#### Azure
- Container Instances or AKS
- Azure Database for PostgreSQL
- Application Gateway

---

## API Endpoints

### Companies
- `POST /api/v1/companies/` - Create company
- `GET /api/v1/companies/` - List companies
- `GET /api/v1/companies/{id}` - Get company

### KPIs
- `POST /api/v1/kpis/` - Record KPI
- `GET /api/v1/kpis/company/{id}` - Get company KPIs
- `GET /api/v1/kpis/company/{id}/latest` - Latest snapshot

### Plays
- `GET /api/v1/plays/` - List plays
- `POST /api/v1/plays/evaluate` - Evaluate triggers

### Jobs
- `POST /api/v1/jobs/` - Create job
- `GET /api/v1/jobs/company/{id}` - Get company jobs

### Evidence
- `POST /api/v1/evidence/` - Create evidence
- `GET /api/v1/evidence/company/{id}` - Get evidence

### Cycles
- `POST /api/v1/cycles/run` - Run growth cycle

---

## Monitoring

### Health Checks
```bash
curl http://localhost:8000/api/health
```

### Logs
```bash
# Docker logs
docker-compose logs -f api

# Application logs
tail -f logs/profit_os.log
```

### Metrics
- API response times
- Job success/failure rates
- Database query performance
- Error rates

---

## Backup & Recovery

### Database Backup
```bash
# SQLite
cp profit_os_chimera.db backups/backup-$(date +%Y%m%d).db

# PostgreSQL
pg_dump profit_os > backups/backup-$(date +%Y%m%d).sql
```

### Restore
```bash
# SQLite
cp backups/backup-YYYYMMDD.db profit_os_chimera.db

# PostgreSQL
psql profit_os < backups/backup-YYYYMMDD.sql
```

---

## Security

### Current (v0.1.0)
- Input validation (Pydantic)
- SQL injection prevention (ORM)
- CORS configuration

### Planned (v0.2.0)
- JWT authentication
- Role-based access control
- API rate limiting
- HTTPS enforcement

---

## Scaling

### Horizontal Scaling
- Run multiple API instances behind load balancer
- Use shared database (PostgreSQL)
- Session storage in database or Redis

### Vertical Scaling
- Increase container resources
- Database connection pooling
- Query optimization

---

## Troubleshooting

### API not starting
- Check port 8000 is available
- Verify database connection
- Check environment variables

### Database errors
- Verify database exists
- Check connection string
- Run migrations: `alembic upgrade head`

### Frontend not connecting
- Verify API_BASE_URL in Streamlit config
- Check CORS settings
- Verify API is running

---

## Support

- **Documentation:** See `/docs` directory
- **API Docs:** http://localhost:8000/api/docs
- **Issues:** GitHub Issues
- **Email:** [support-email]

---

**Version:** 0.1.0_Publish
**Status:** Production Ready ✅



