import unittest
import sys
import argparse


def run_tests(pattern="*_test.py", verbosity=2, use_buffer=False):
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="test", pattern=pattern)

    # buffer=True gets stdout/stderr and only shows if test failed
    runner = unittest.TextTestRunner(verbosity=verbosity, buffer=use_buffer)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n" + "\033[92m" + "All tests passed!")
        sys.exit(0)
    else:
        print(
            "\n"
            + "\033[93m"
            + f"Failed: {len(result.failures)} failures, {len(result.errors)} errors."
        )
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metrics App Healthcheck")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action="store_true", help="Minimum output")
    group.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    parser.add_argument("--pattern", default="*_test.py", help="Test file pattern")

    args = parser.parse_args()

    if args.quiet:
        level = 0
        buf = True
    elif args.verbose:
        level = 2
        buf = False
    else:
        level = 1
        buf = False

    run_tests(pattern=args.pattern, verbosity=level, use_buffer=buf)
