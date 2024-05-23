# Handling imports and missing dependencies
try:
    from google.cloud.sql.connector import Connector, IPTypes, create_async_connector
except ImportError:
    Connector = None
    IPTypes = None
    create_async_connector = None

try:
    import asyncpg
except ImportError:
    asyncpg = None

try:
    import pg8000
except ImportError:
    pg8000 = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
except ImportError:
    async_sessionmaker = None
    create_async_engine = None

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import DeclarativeBase, sessionmaker
except ImportError:
    create_engine = None
    DeclarativeBase = None
    sessionmaker = None

# Importing the required modules

import enum

from pydantic import BaseModel

from launchflow.gcp.resource import GCPResource
from launchflow.generic_clients import PostgresClient


# Connection information model
class CloudSQLPostgresConnectionInfo(BaseModel):
    connection_name: str
    user: str
    password: str
    database_name: str
    public_ip_address: str
    private_ip_address: str
    public_ip_enabled: bool


# TODO: Add Enums and other input types to generated docs.
# Punting for now since it goes to the top of the docs page - we need an option to
# have it go to the bottom.
class PostgresVersion(enum.Enum):
    POSTGRES_15 = "POSTGRES_15"
    POSTGRES_14 = "POSTGRES_14"
    POSTGRES_13 = "POSTGRES_13"
    POSTGRES_12 = "POSTGRES_12"
    POSTGRES_11 = "POSTGRES_11"
    POSTGRES_10 = "POSTGRES_10"
    POSTGRES_9_6 = "POSTGRES_9_6"


class CloudSQLPostgres(GCPResource[CloudSQLPostgresConnectionInfo], PostgresClient):
    """A Postgres cluster running on Google Cloud SQL.

    **Example usage:**
    ```python
    from sqlalchemy import text
    import launchflow as lf

    postgres = lf.gcp.CloudSQLPostgres("my-pg-db")

    # Quick utilities for connecting to SQLAlchemy, Django, and other ORMs
    engine = postgres.sqlalchemy_engine()

    with engine.connect() as connection:
        print(connection.execute(text("SELECT 1")).fetchone())  # prints (1,)
    ```
    """

    def __init__(
        self,
        name: str,
        *,
        postgres_version: PostgresVersion = PostgresVersion.POSTGRES_15,
    ) -> None:
        """Create a new Cloud SQL Postgres resource.

        **Args**:
        - `name`: The name of the Cloud SQL Postgres instance.
        - `postgres_version`: The version of Postgres to use. Defaults to `PostgresVersion.POSTGRES_15`.
        """
        super().__init__(
            name=name,
            product_name="gcp_sql_postgres",
            create_args={
                "postgres_version": postgres_version.value,
            },
        )

    def django_settings(self):
        """Returns a Django settings dictionary for connecting to the Cloud SQL Postgres instance.

        **Example usage:**
        ```python
        import launchflow as lf

        postgres = lf.gcp.CloudSQLPostgres("my-pg-db")

        # settings.py
        DATABASES = {
            # Connect Django's ORM to the Cloud SQL Postgres instance
            "default": postgres.django_settings(),
        }
        ```
        """
        if psycopg2 is None:
            raise ImportError(
                "psycopg2 is not installed. Please install it with `pip install psycopg2`."
            )

        connection_info = self.connect()

        host = connection_info.private_ip_address
        if connection_info.public_ip_enabled:
            host = connection_info.public_ip_address

        return {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": connection_info.database_name,
            "USER": connection_info.user,
            "PASSWORD": connection_info.password,
            "HOST": host,
            "SSLMODE": "require",
        }

    def sqlalchemy_engine_options(self, *, ip_type=None):
        if Connector is None or IPTypes is None:
            raise ImportError(
                "google-cloud-sql-connector not installed. Please install it with "
                "`pip install launchflow[gcp]`."
            )
        if pg8000 is None:
            raise ImportError(
                "pg8000 is not installed. Please install it with `pip install pg8000`."
            )
        connection_info = self.connect()
        if ip_type is None:
            if connection_info.public_ip_enabled:
                ip_type = IPTypes.PUBLIC
            else:
                ip_type = IPTypes.PRIVATE

        connector = Connector(ip_type)

        # initialize Connector object for connections to Cloud SQL
        def getconn():
            conn = connector.connect(
                instance_connection_string=connection_info.connection_name,
                driver="pg8000",
                user=connection_info.user,
                password=connection_info.password,
                db=connection_info.database_name,
            )
            return conn

        return {"url": "postgresql+pg8000://", "creator": getconn}

    async def sqlalchemy_async_engine_options(self, ip_type=None):
        if Connector is None or IPTypes is None or create_async_connector is None:
            raise ImportError(
                "google-cloud-sql-connector not installed. Please install it with "
                "`pip install launchflow[gcp]`."
            )
        if asyncpg is None:
            raise ImportError(
                "asyncpg is not installed. Please install it with `pip install asyncpg`."
            )
        connection_info = await self.connect_async()
        if ip_type is None:
            if connection_info.public_ip_enabled:
                ip_type = IPTypes.PUBLIC
            else:
                ip_type = IPTypes.PRIVATE
        connector = await create_async_connector()

        # initialize Connector object for connections to Cloud SQL
        async def getconn():
            conn = await connector.connect_async(
                instance_connection_string=connection_info.connection_name,
                driver="asyncpg",
                user=connection_info.user,
                password=connection_info.password,
                db=connection_info.database_name,
                ip_type=ip_type,
            )
            return conn

        return {"url": "postgresql+asyncpg://", "async_creator": getconn}

    def sqlalchemy_engine(self, *, ip_type=None, **engine_kwargs):
        """Returns a SQLAlchemy engine for connecting to the Cloud SQL Postgres instance.

        Args:
        - `ip_type`: The IP type to use for the connection. If not provided will default to the most permisive IP address.
            For example if your Cloud SQL instance is provisioned with a public IP address, the default will be `IPTypes.PUBLIC`.
            Otherwise it will default to `IPTypes.PRIVATE`.
        - `**engine_kwargs`: Additional keyword arguments to pass to `sqlalchemy.create_engine`.

        **Example usage:**
        ```python
        import launchflow as lf

        postgres = lf.gcp.CloudSQLPostgres("my-pg-db")

        # Creates a SQLAlchemy engine for connecting to the Cloud SQL Postgres instance
        engine = postgres.sqlalchemy_engine()

        with engine.connect() as connection:
            print(connection.execute("SELECT 1").fetchone())  # prints (1,)
        ```
        """
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install sqlalchemy`."
            )

        engine_options = self.sqlalchemy_engine_options(ip_type=ip_type)
        engine_options.update(engine_kwargs)

        return create_engine(**engine_options)

    async def sqlalchemy_async_engine(self, *, ip_type=None, **engine_kwargs):
        """Returns an async SQLAlchemy engine for connecting to the Cloud SQL Postgres instance.

        Args:
        - `ip_type`: The IP type to use for the connection. If not provided will default to the most permisive IP address.
            For example if your Cloud SQL instance is provisioned with a public IP address, the default will be `IPTypes.PUBLIC`.
            Otherwise it will default to `IPTypes.PRIVATE`.        - `**engine_kwargs`: Additional keyword arguments to pass to `create_async_engine`.

        **Example usage:**
        ```python
        import launchflow as lf

        postgres = lf.gcp.CloudSQLPostgres("my-pg-db")

        # Creates an async SQLAlchemy engine for connecting to the Cloud SQL Postgres instance
        engine = await postgres.sqlalchemy_async_engine()

        async with engine.begin() as connection:
            result = await connection.execute("SELECT 1")
            print(await result.fetchone())
        ```
        """
        if create_async_engine is None:
            raise ImportError(
                "SQLAlchemy asyncio extension is not installed. "
                "Please install it with `pip install sqlalchemy[asyncio]`."
            )

        engine_options = await self.sqlalchemy_async_engine_options(ip_type=ip_type)
        engine_options.update(engine_kwargs)

        return create_async_engine(**engine_options)
