import os
import sys
import time
import signal
import subprocess
from pathlib import Path


def open_in_safari_via_browser_env(url: str) -> None:
	# Prefer using the host's $BROWSER wrapper so the host browser (Safari) opens.
	browser_env = os.environ.get("BROWSER")
	if browser_env:
		subprocess.run(["/bin/sh", "-c", f'$BROWSER "{url}"'])
	else:
		try:
			import webbrowser

			webbrowser.open(url)
		except Exception:
			print("Could not open browser. Please open:", url)


def serve_and_open(html_dir: Path, port: int = 8000, open_delay: float = 0.5, stay_seconds: int = 12) -> None:
	cmd = [sys.executable, "-m", "http.server", str(port), "--directory", str(html_dir)]
	proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	try:
		time.sleep(open_delay)
		url = f"http://127.0.0.1:{port}/index.html"
		open_in_safari_via_browser_env(url)
		# Keep the server alive long enough for the page to open and close
		time.sleep(stay_seconds)
	finally:
		try:
			proc.terminate()
			proc.wait(timeout=3)
		except Exception:
			try:
				proc.kill()
			except Exception:
				pass


if __name__ == "__main__":
	repo_root = Path(__file__).resolve().parent
	html_dir = repo_root / "red_browser"
	if not html_dir.exists():
		print("Missing red_browser/index.html — create it first.")
		sys.exit(1)

	serve_and_open(html_dir, port=8000, open_delay=0.5, stay_seconds=12)


