#!/usr/bin/env bash
# Installs the OpenCode CLI deterministically on CI.
#
# The upstream installer resolves "latest" through the unauthenticated GitHub
# API (https://api.github.com/repos/anomalyco/opencode/releases/latest). On
# GitHub-hosted runners that call is rate limited and intermittently fails with
# "Failed to fetch version information", which kills a batch run before any
# writing starts. Passing --version skips that API lookup entirely, so the
# version is pinned here and a release download is the only network dependency.
#
# Order of preference:
#   1. pinned version via the upstream installer
#   2. pinned version via npm (independent registry and delivery path)
#   3. unpinned latest via the upstream installer (in case a pin is ever yanked)
set -uo pipefail

PINNED_VERSION="${OPENCODE_VERSION:-1.18.33}"
INSTALL_SCRIPT_URL="https://opencode.ai/install"
LOG_DIR="${1:-logs}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/install-opencode.log"

log() { printf '%s install_opencode[%s]: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$$" "$*"; }

log "starting; pinned version $PINNED_VERSION"

# The upstream installer writes $HOME/.opencode/bin to $GITHUB_PATH itself, but
# npm installs elsewhere, so every candidate directory is registered here.
register_path() {
  local dir="$1"
  [ -n "$dir" ] || return 0
  mkdir -p "$dir"
  case ":${GITHUB_PATH:-}:" in
    *":$dir:"*) ;;
    *) printf '%s\n' "$dir" >> "${GITHUB_PATH:-/dev/null}" ;;
  esac
  case ":${PATH}:" in
    *":$dir:"*) ;;
    *) PATH="$dir:$PATH" ;;
  esac
}

refresh_path() {
  register_path "$HOME/.opencode/bin"
  if command -v npm >/dev/null 2>&1; then
    local prefix
    prefix="$(npm prefix -g 2>/dev/null || true)"
    if [ -n "$prefix" ]; then
      register_path "$prefix/bin"
    fi
  fi
  register_path "$HOME/.local/bin"
  hash -r 2>/dev/null || true
  return 0
}

opencode_works() {
  command -v opencode >/dev/null 2>&1 || return 1
  opencode --version >/dev/null 2>&1
}

# A single install attempt is only successful when the binary answers.
verify() {
  refresh_path
  if opencode_works; then
    log "opencode is working: $(opencode --version 2>/dev/null || echo unknown)"
    return 0
  fi
  return 1
}

already_installed() {
  refresh_path
  if opencode_works; then
    local current
    current="$(opencode --version 2>/dev/null || echo unknown)"
    if [ "$current" = "$PINNED_VERSION" ]; then
      log "opencode $PINNED_VERSION already present"
      return 0
    fi
    log "opencode present but version is $current, reinstalling $PINNED_VERSION"
  fi
  return 1
}

fetch_installer() {
  curl -fsSL --retry 3 --retry-delay 3 --retry-all-errors --connect-timeout 20 \
    --max-time 120 "$INSTALL_SCRIPT_URL"
}

install_pinned() {
  log "trying upstream installer pinned to $PINNED_VERSION"
  fetch_installer | bash -s -- --version "$PINNED_VERSION" --no-modify-path
}

install_latest() {
  log "trying upstream installer with unpinned latest"
  fetch_installer | bash -s -- --no-modify-path
}

install_npm() {
  log "trying npm install opencode-ai@$PINNED_VERSION"
  npm install -g "opencode-ai@$PINNED_VERSION"
}

retry() {
  local label="$1" tries="$2"
  shift 2
  local n=1
  while [ "$n" -le "$tries" ]; do
    log "$label attempt $n of $tries"
    if "$@" >>"$LOG_FILE" 2>&1 && verify; then
      log "$label succeeded on attempt $n"
      return 0
    fi
    log "$label attempt $n failed"
    n=$((n + 1))
    [ "$n" -le "$tries" ] && sleep $((n * 5))
  done
  return 1
}

if already_installed; then
  exit 0
fi

# Pinned upstream install first: fastest path and no API rate limit.
retry "pinned-installer" 3 install_pinned && exit 0

# npm is a different host, so it still works when github.com is degraded.
retry "npm" 2 install_npm && exit 0

# Last resort: let the upstream installer resolve latest itself.
retry "unpinned-installer" 2 install_latest && exit 0

log "all install attempts failed; last output follows"
tail -n 40 "$LOG_FILE" 2>/dev/null || true
echo "OpenCode install failed; see $LOG_FILE" >&2
exit 1
