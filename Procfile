web: gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --threads 1 --timeout 180 --max-requests 100 --max-requests-jitter 10 --preload
