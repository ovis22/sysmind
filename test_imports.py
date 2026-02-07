try:
    import google.genai
    print("[OK] google-genai imported")
except ImportError as e:
    print(f"[FAIL] google-genai missing: {e}")

try:
    from rich.console import Console
    print("[OK] rich imported")
except ImportError as e:
    print(f"[FAIL] rich missing: {e}")

try:
    import pyttsx3
    print("[OK] pyttsx3 imported")
except ImportError:
    print("[WARN] pyttsx3 missing (Voice feedback will be disabled)")

import sys
print(f"[INFO] Python version: {sys.version}")
