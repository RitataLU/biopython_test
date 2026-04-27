"""
Evaluation harness for the FASTA parser autoresearch loop.

Runs Tests/test_SeqIO_FastaIO.py and prints a structured summary.
Analogous to evaluate_bpb in prepare.py — do NOT modify this file.

Usage:
    python evaluate_fasta.py
"""

import subprocess
import sys
import re
import os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(REPO_ROOT, "Tests", "test_SeqIO_FastaIO.py")
TESTS_DIR = os.path.join(REPO_ROOT, "Tests")


def run():
    env = os.environ.copy()
    # Ensure the local source tree is used, not any installed biopython.
    env["PYTHONPATH"] = REPO_ROOT + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-v", "--tb=short", "-q"],
        capture_output=True,
        text=True,
        cwd=TESTS_DIR,
        env=env,
    )

    output = result.stdout + result.stderr

    # Parse pytest summary line e.g. "17 passed" or "15 passed, 2 failed"
    passed = failed = 0
    m = re.search(r"(\d+) passed", output)
    if m:
        passed = int(m.group(1))
    m = re.search(r"(\d+) failed", output)
    if m:
        failed = int(m.group(1))

    total = passed + failed
    score = passed / total if total > 0 else 0.0

    print(output)
    print("---")
    print(f"tests_passed:  {passed}")
    print(f"tests_failed:  {failed}")
    print(f"tests_total:   {total}")
    print(f"score:         {score:.4f}")
    return score, passed, failed, total


if __name__ == "__main__":
    score, passed, failed, total = run()
    if failed > 0:
        sys.exit(1)
