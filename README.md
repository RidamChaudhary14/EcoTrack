# EcoTrack

## Database Configuration (Supabase PostgreSQL)

This project uses Supabase PostgreSQL as its exclusive database. There are no local fallbacks.

### Obtaining the Connection String
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Navigate to **Project Settings** -> **Database**.
3. Scroll down to **Connection String** and copy the URI (ensure you switch to the "Transaction" mode pooler if you plan to use pgbouncer, and "Session" mode for migrations via `DIRECT_URL`).

### Environment Variables
Place a `.env` file in the `backend/` directory. Example:
```env
# Database configuration
DATABASE_URL="postgresql://postgres.your_project_id:[YOUR-PASSWORD]@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?pgbouncer=true"
DIRECT_URL="postgresql://postgres.your_project_id:[YOUR-PASSWORD]@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

# Security settings
SECRET_KEY="your-secure-random-string"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

### Running Migrations
We use Alembic for database migrations. To apply all pending migrations, ensure your `DATABASE_URL` is set, and run from the `backend/` directory:
```bash
alembic upgrade head
```

### Seeding the Database
To populate the database with initial dummy data, run the seed script from the `backend/` directory:
```bash
python seed.py
```
