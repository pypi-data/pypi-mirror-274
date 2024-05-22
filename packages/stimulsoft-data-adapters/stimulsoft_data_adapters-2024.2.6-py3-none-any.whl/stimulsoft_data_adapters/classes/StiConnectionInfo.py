class StiConnectionInfo:
    """All database connection information taken from the connection string."""

    driver: str = ''
    host: str = ''
    port: int = 0
    database: str = ''
    userId: str = ''
    password: str = ''
    charset: str = ''
    privilege: str = ''
    dataPath: str = ''
    schemaPath: str = ''