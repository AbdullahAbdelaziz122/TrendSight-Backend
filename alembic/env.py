import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Import your Base and models so Alembic can "see" them
from app.db.database import Base
from app.models import User, Symbol, Model, Prediction  # Import all your models here!
from app.configs.configs import get_settings 

config = context.config

# 2. Setup Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Set Metadata
target_metadata = Base.metadata

# 4. Override the URL in alembic.ini with the one from your settings/env
# This ensures it uses the same URL as your app
config.set_main_option("sqlalchemy.url", get_settings().DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode. (Unchanged standard code)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode (Async Version)."""
    
    # 5. Create Async Engine
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # 6. Run the sync migration function inside the async loop
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    # 7. Run the Async loop
    asyncio.run(run_migrations_online())