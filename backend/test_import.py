"""Test if the app can be imported."""
try:
    from app.main import app
    print("OK: Import successful! App is ready.")
except Exception as e:
    print(f"ERROR: Import failed: {e}")
    import traceback
    traceback.print_exc()

