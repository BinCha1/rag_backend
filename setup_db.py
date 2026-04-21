#!/usr/bin/env python
"""Quick database setup script."""

from app.db.init_db import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✓ Database ready!")
