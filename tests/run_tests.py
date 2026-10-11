#!/usr/bin/env python3
"""
scanet — Zero-Dependency Universal Test Runner
Executes all test functions across test_adapters, test_analyzers, and test_engine.
"""
import os
import sys
import time
import inspect
import importlib.util

# Add backend and project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))
sys.path.insert(0, PROJECT_ROOT)

def discover_and_run(iterations=1):
    test_files = [
        os.path.join(PROJECT_ROOT, "tests", "test_adapters", "test_nmap_adapter.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_adapters", "test_nuclei_adapter.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_analyzers", "test_ai_advisor.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_analyzers", "test_cve_correlator.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_analyzers", "test_os_fingerprint.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_analyzers", "test_web_auditor.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_analyzers", "test_subdomain_takeover.py"),
        os.path.join(PROJECT_ROOT, "tests", "test_engine", "test_scope_validator.py"),
    ]

    total_runs = 0
    total_passed = 0
    total_failed = 0
    failed_details = []

    print("\033[96m" + "=" * 65 + "\033[0m")
    print(f"\033[1;36m  [*] scanet Automated Test Suite ({iterations} Iteration{'s' if iterations > 1 else ''})\033[0m")
    print("\033[96m" + "=" * 65 + "\033[0m\n")

    start_time = time.time()

    for iter_idx in range(1, iterations + 1):
        if iterations > 1:
            print(f"\033[94m--- Iteration {iter_idx}/{iterations} ---\033[0m")

        for fpath in test_files:
            rel_name = os.path.relpath(fpath, PROJECT_ROOT)
            module_name = os.path.splitext(os.path.basename(fpath))[0]
            spec = importlib.util.spec_from_file_location(module_name, fpath)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            # Discover all test_* functions
            for attr_name, attr_val in inspect.getmembers(mod):
                if attr_name.startswith("test_") and inspect.isfunction(attr_val):
                    total_runs += 1
                    try:
                        attr_val()
                        total_passed += 1
                        if iterations == 1:
                            print(f"  \033[92m[PASS]\033[0m {rel_name} :: {attr_name}")
                    except Exception as e:
                        total_failed += 1
                        failed_details.append((rel_name, attr_name, str(e)))
                        print(f"  \033[91m[FAIL]\033[0m {rel_name} :: {attr_name} -> {e}")

    duration = time.time() - start_time
    print("\n" + "\033[96m" + "-" * 65 + "\033[0m")
    if total_failed == 0:
        print(f"\033[1;92m  [OK] SUCCESS: {total_passed}/{total_runs} tests passed in {duration:.3f}s (100% Pass Rate)\033[0m")
    else:
        print(f"\033[1;91m  [ERR] FAILED: {total_failed} failures out of {total_runs} tests\033[0m")
    print("\033[96m" + "-" * 65 + "\033[0m\n")

    return total_failed == 0

if __name__ == "__main__":
    count = 1
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        count = int(sys.argv[1])
    success = discover_and_run(iterations=count)
    sys.exit(0 if success else 1)
