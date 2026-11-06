@Library('nstut-ci') _

// Trusted-main, low-memory validation only. GitHub Actions continue to own
// fork/PR validation, cross-platform archives, runtime server smoke and release.
nstutPython(
    python: '3.11',
    command: '''#!/usr/bin/env bash
set -euo pipefail
python tools/ci_validate.py
python -m compileall -q tools/ci_validate.py tools/validate_quests.py tools/validate_pack.py
''',
    tests: 'ci-evidence/validation-tests.xml',
    artifacts: 'ci-evidence/**'
)
