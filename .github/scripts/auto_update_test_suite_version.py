import sys
import argparse
import pathlib
from dynaconf import Dynaconf
import json
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.utility.constants import NRT_SUITES_FILE



def main():
    parser = argparse.ArgumentParser(description='Automatically update test suite version')
    parser.add_argument('--version-change', '-v', default='skip', help='Type of version change label')
    parser.add_argument('--suite', '-s', default='', help='Changed suite label')
    parser.add_argument('--pending-count', type=int, default=0, help='Number of pending version bump PRs')

    args = parser.parse_args()
    version_label = str(args.version_change).lower()
    suite_label = str(args.suite).upper()
    pending_count = args.pending_count

    if version_label == 'skip' or suite_label == '':
        print("Skipping test suite version update due to missing version or suite label")
        return

    if version_label != 'skip' and suite_label:
        print(f"Updating test suite version for version: {version_label}, suite: {suite_label}, pending bumps: {pending_count}")
        with open(NRT_SUITES_FILE, 'r') as f:
            suites = json.load(f)

        current_version = [x.get('version') for x in suites.get('suites', []) if x.get('id') == suite_label.lower()][0]
        if not current_version:
            print(f"No current version found for suite: {suite_label}")
            return
        
        
        major, minor, patch = map(int, current_version.split('.'))
        
        # Apply version bump once per increment type
        # If pending bumps exist for the same suite, accumulate them by counting all pending bumps
        # and applying the same increment type multiple times
        total_bumps = 1 + pending_count
        for _ in range(total_bumps):
            match version_label:
                case 'major':
                    major += 1
                    minor = 0
                    patch = 0
                case 'minor':
                    minor += 1
                    patch = 0
                case 'patch':
                    patch += 1
        
        new_version = f"{major}.{minor}.{patch}"
        print(f"New version for {suite_label}: {current_version} -> {new_version} (applied {total_bumps} increment(s))")
        
        for suite in suites.get('suites', []):
            if suite.get('id') == suite_label.lower():
                suite['version'] = new_version
                break

        with open(NRT_SUITES_FILE, 'w') as f:
            json.dump(suites, f, indent=2)
            f.write('\n')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
           print(f"[ERROR][auto_update_test_suite_version] {str(e)}")
           raise