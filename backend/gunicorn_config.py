# gunicorn_config.py
# Post-fork hook to initialize MongoDB after worker fork (fork-safe)

import os
import sys

# Note: bind, workers, timeout, etc. are set in Procfile/railway.json command line
# This file only contains the post_fork hook for MongoDB initialization

def post_fork(server, worker):
    """Called after a worker has been forked."""
    # Initialize database indexes after fork (fork-safe)
    try:
        from models import init_db
        init_db()
        print(f"✅ Worker {worker.pid}: MongoDB initialized (post-fork)")
    except Exception as e:
        print(f"⚠️  Worker {worker.pid}: MongoDB init error: {e}")
        print(f"⚠️  Worker {worker.pid}: Will retry on first database operation")
        # Don't crash worker - connection will happen on first use
        import traceback
        traceback.print_exc()

