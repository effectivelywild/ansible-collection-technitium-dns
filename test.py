import subprocess
import time
import sys
import os
import signal
from collections import defaultdict

# --- Configuration ---
LOG_FILE = "continuous_test_failures.log"
# Command to list all integration tests
LIST_COMMAND = ["ansible-test", "integration", "--list"]
# Test to explicitly exclude (the disabled one)
EXCLUDED_TEST = "technitium_dns_resync_cluster"

# --- State Variables ---
TEST_PASS_COUNTS = defaultdict(int)
TEST_FAIL_COUNTS = defaultdict(int)
TEST_RUN_TIMES = defaultdict(lambda: 0.0) # Stores the duration of the last run (seconds)
TEST_NAMES = []
TOTAL_RUNS = 0
TOTAL_PASSES = 0
TOTAL_FAILS = 0
LAST_CYCLE_DURATION = 0.0 # Stores the duration of the last full cycle (seconds)

def initialize_tests():
    """Runs ansible-test --list and populates the TEST_NAMES array."""
    global TEST_NAMES
    
    print("Gathering and initializing test list using Python...")
    
    try:
        # Run the list command and capture output
        result = subprocess.run(
            LIST_COMMAND,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        
        # Process output line by line
        for line in result.stdout.splitlines():
            test_name = line.strip()
            # Filter out warnings, empty lines, and the excluded test
            if test_name and not test_name.startswith('WARNING:') and test_name != EXCLUDED_TEST:
                TEST_NAMES.append(test_name)
    
    except subprocess.CalledProcessError as e:
        print(f"Error running ansible-test: {e.stderr}", file=sys.stderr)
        sys.exit(1)
        
    if not TEST_NAMES:
        print("ERROR: No tests found after filtering.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(TEST_NAMES)} unique integration tests.")
    
    # Clear the previous log file
    with open(LOG_FILE, 'w') as f:
        f.write("--- Starting Continuous Integration Test Runner ---\n")

def display_stats():
    """Clears the screen and prints the current statistics."""
    os.system('clear')
    
    print("=" * 60)
    print("            CONTINUOUS TEST RUNNER                ")
    print("=" * 60)
    print(f" Total Unique Tests: {len(TEST_NAMES)}")
    print(f" Total Runs Completed: {TOTAL_RUNS}")
    print(f"   ✅ Total Passes: {TOTAL_PASSES}")
    print(f"   ❌ Total Fails: {TOTAL_FAILS}")
    print(f"   ⏳ Last Cycle Duration: {LAST_CYCLE_DURATION:.2f} seconds")
    print("-" * 60)
    print("           INDIVIDUAL TEST STATS                  ")
    print("-" * 60)
    
    # Print the header with the new TIME column
    print(f"{'TEST NAME':<40} | {'✅ PASS':<8} | {'❌ FAIL':<8} | {'TIME (s)':<8}")
    print("-" * 75)
    
    # Print individual test stats
    for name in TEST_NAMES:
        passes = TEST_PASS_COUNTS[name]
        fails = TEST_FAIL_COUNTS[name]
        run_time = TEST_RUN_TIMES[name]
        
        # New: Print the run time next to the PASS/FAIL counts
        print(f"{name:<40} | {passes:^8} | {fails:^8} | {run_time:^8.2f}")

    print("-" * 60)
    
    # Print last 3 failures from the log
    if TOTAL_FAILS > 0:
        print("Last 3 failures recorded in log:")
        try:
            with open(LOG_FILE, 'r') as f:
                # Find the last 3 failure log markers
                lines = f.readlines()
                failure_lines = [line.strip() for line in lines if line.startswith('--- START FAILURE LOG FOR')]
                
                for line in failure_lines[-3:]:
                    print(line)
        except Exception:
            pass # Ignore file reading errors for display

def run_test(test_name):
    """Executes a single ansible-test command and records its time."""
    global TOTAL_RUNS, TOTAL_PASSES, TOTAL_FAILS
    
    display_stats()
    print(f"Running test: **{test_name}**")

    run_command = ["ansible-test", "integration", test_name]
    
    # --- Start Timer ---
    start_time = time.time()

    try:
        # Execute the test
        result = subprocess.run(
            run_command,
            capture_output=True,
            text=True,
            check=False, # Do not raise exception on non-zero exit code
            encoding='utf-8'
        )
        
        # --- Stop Timer and Record Time ---
        duration = time.time() - start_time
        TEST_RUN_TIMES[test_name] = duration
        
        # Check the exit code
        if result.returncode == 0:
            # Test Passed
            TEST_PASS_COUNTS[test_name] += 1
            TOTAL_PASSES += 1
            print(f" [PASS] {test_name} took {duration:.2f}s")
        else:
            # Test Failed
            TEST_FAIL_COUNTS[test_name] += 1
            TOTAL_FAILS += 1
            print(f" [FAIL] {test_name} took {duration:.2f}s (Total Fails: {TOTAL_FAILS})")

            # Log the failure output
            with open(LOG_FILE, 'a') as f:
                f.write(f"--- START FAILURE LOG FOR {test_name} (FAIL: {TOTAL_FAILS}) @ {time.ctime()} ---\n")
                
                # Combine stdout and stderr for logging
                full_output = result.stdout + result.stderr
                # Get the last 20 lines
                failure_lines = full_output.splitlines()
                
                # Write the last 20 lines to the log
                f.write('\n'.join(failure_lines[-20:]))
                f.write('\n--- END FAILURE LOG FOR ' + test_name + ' ---\n\n')

        TOTAL_RUNS += 1

    except Exception as e:
        # Handle exceptions outside of subprocess execution
        duration = time.time() - start_time
        TEST_RUN_TIMES[test_name] = duration 
        print(f"An unexpected error occurred while running {test_name}: {e}", file=sys.stderr)
        
        TEST_FAIL_COUNTS[test_name] += 1
        TOTAL_FAILS += 1
        TOTAL_RUNS += 1


def main_loop():
    """Main continuous loop."""
    global LAST_CYCLE_DURATION
    try:
        initialize_tests()
        print("--- Starting Continuous Test Loop. Press Ctrl+C to stop. ---")
        
        while True:
            cycle_start_time = time.time()
            
            for test_name in TEST_NAMES:
                run_test(test_name)
            
            cycle_end_time = time.time()
            LAST_CYCLE_DURATION = cycle_end_time - cycle_start_time
            
            display_stats()
            print(f"--- Cycle Complete ({len(TEST_NAMES)} Tests Run) in {LAST_CYCLE_DURATION:.2f} seconds ---")
            print("Pausing for 5 seconds before starting the next cycle. Press Ctrl+C to stop.")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n--- INTERRUPTED ---")
        display_stats()
        print("Exiting test runner.")
        sys.exit(0)

if __name__ == "__main__":
    main_loop()
