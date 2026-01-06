#!/usr/bin/env bash
# Block direct pushes to main/master branch
# This enforces the worktree + PR workflow
#
# NOTE: This hook does NOT rely on stdin because pre-commit framework
# does not pass stdin to hook scripts. Instead, we check the current branch
# and the push destination directly.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Protected branches
PROTECTED_BRANCHES=("main" "master")

# Helper function to print block message and exit
block_push() {
    local branch="$1"
    echo -e "${RED}ERROR: Direct push to '$branch' is blocked.${NC}"
    echo ""
    echo -e "${YELLOW}The TDD workflow requires using feature branches and PRs:${NC}"
    echo ""
    echo "  1. Create a worktree:  just worktree-new feature-name"
    echo "  2. Make changes in:    cd ../feature-name"
    echo "  3. Commit your work:   git add -A && git commit -m '...'"
    echo "  4. Create a PR:        just pr 'feat(scope): description'"
    echo ""
    exit 1
}

# Check 1: Current branch name
# This catches the common case of being on main and pushing
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

for protected in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$current_branch" == "$protected" ]]; then
        block_push "$current_branch"
    fi
done

# Check 2: Push destination (catches `git push origin feature:main`)
# Try to get the upstream tracking branch
push_dest=$(git rev-parse --abbrev-ref --symbolic-full-name '@{push}' 2>/dev/null || echo "")
if [[ "$push_dest" == refs/remotes/* ]]; then
    # Extract branch name from refs/remotes/origin/main -> main
    push_branch="${push_dest##*/}"
    for protected in "${PROTECTED_BRANCHES[@]}"; do
        if [[ "$push_branch" == "$protected" ]]; then
            block_push "$push_branch (via @{push})"
        fi
    done
fi

# Check 3: Read from stdin if available (for native git hook usage)
if [ ! -t 0 ]; then
    while read -r local_ref local_sha remote_ref remote_sha; do
        if [[ "$remote_ref" == refs/heads/* ]]; then
            branch_name="${remote_ref#refs/heads/}"
            for protected in "${PROTECTED_BRANCHES[@]}"; do
                if [[ "$branch_name" == "$protected" ]]; then
                    block_push "$branch_name (via refspec)"
                fi
            done
        fi
    done
fi

exit 0
