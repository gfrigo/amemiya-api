from src.core.database import start_connection, start_cursor
from src.core.config import settings, logger


def create_telemetry_table():
    """Create Telemetry table if it does not exist.

    Uses the configured MySQL connection from `settings.db_credentials`.
    """
    ddl = (
        "CREATE TABLE IF NOT EXISTS Telemetry ("
        "id BIGINT AUTO_INCREMENT PRIMARY KEY,"
        "company_id INT NULL,"
        "device_id VARCHAR(128) NULL,"
        "payload JSON,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ");"
    )

    try:
        creds = settings.db_credentials
        with start_connection(creds) as conn:
            with start_cursor(conn) as cursor:
                cursor.execute(ddl)
                conn.commit()
                logger.info("Telemetry table ensured in database.")
    except Exception as e:
        logger.error(f"Failed to create Telemetry table: {e}")
