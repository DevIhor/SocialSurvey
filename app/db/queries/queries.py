import pathlib

import aiosql as aiosql

queries = aiosql.from_path(pathlib.Path(__file__).parent / "sql", "asyncpg")
