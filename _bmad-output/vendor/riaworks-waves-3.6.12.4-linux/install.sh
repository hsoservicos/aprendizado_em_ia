#!/bin/sh
# riaworks-waves 3.6.12.4 — bundle installer for Linux, macOS and WSL.
#
# Installs both levels of the module, in one run, from the files next to this
# script: no git, no PyPI account, no credential. Both levels are idempotent —
# re-run this against a newer bundle and it upgrades in place.
#
#   MACHINE  the `waves` orchestrator (plus the `waves tui` dashboard), installed
#            from ./wheels/ into uv's own managed tool environment.
#   PROJECT  the `waves-*` skills, the coding-CLI hook relay, .waves/loop/policy.toml
#            and the gitignore entries — laid down by `waves init`.
#
# Usage:
#   sh install.sh [--project <dir>] [--cli <name>]... [options]
#
#   --project <dir>     the BMAD project to wire up (default: the current directory)
#   --cli <name>        coding CLI whose hooks to register; repeatable (default: claude)
#   --tool-only         install the machine level and stop
#   --project-only      skip the machine level (`waves` must already be on PATH)
#   --via-bmad          also register the module with the BMAD installer, so
#                       /bmad-help lists it (needs npx; never required to run)
#   --no-tui            install without the [tui] extra (no `waves tui`)
#   --find-links <dir>  resolve dependencies from a local wheel directory instead
#                       of PyPI, and pass --offline (see INSTALL.md)
#   --force             refresh project skill copies that already exist
#   --no-bootstrap      never install a missing prerequisite; report and continue
#   -h, --help          this text
#
# PREREQUISITES ARE INSTALLED, NOT DEMANDED. A machine that has never run any of
# this has no uv, and possibly no git, tmux or python: what installs without
# privilege (uv, and python through uv) is installed here, and what needs a package
# manager is attempted through this system's own, with the exact command printed
# when that cannot work. --no-bootstrap turns all of it off.
#
# Nothing here writes outside `waves`' own names. The skills, the state directory
# (.waves/), the versioned project directory (_waves/), the environment variables (WAVES_*) and the BMAD module directory
# (_bmad/waves/) are namespaced, and `waves init` only ever APPENDS its own relay
# to a coding CLI's hook config — another tool's registrations are left as they are.
set -eu

VERSION="3.6.12.4"
WHEEL_NAME="riaworks_waves-3.6.12.4-py3-none-any.whl"
PKG_DIR="riaworks-waves-3.6.12.4"
SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

MODE=both
PROJECT="."
# Whether --project was given: a path on the command line is an ANSWER, so the
# installer uses it instead of asking again.
PROJECT_GIVEN=0
CLIS=""
EXTRA="[tui]"
FIND_LINKS=""
FORCE=0
VIA_BMAD=0
BOOTSTRAP=1
# Every network call is bounded. An unbounded fetch does not fail — it hangs, with
# no exit status to react to; this project's CI lost 14 minutes that way to an
# `apt-get update` that never returned, and `|| true` cannot catch a command that
# never exits.
NET_TIMEOUT=300

usage() { sed -n '2,/^set -eu$/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; }
die() {
  echo "riaworks-waves: $*" >&2
  exit 2
}
note() { echo "  $*"; }
step() { echo "==> $*"; }
have() { command -v "$1" >/dev/null 2>&1; }

TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT INT TERM

# bounded <seconds> <cmd...> — the bound is the point; without `timeout` present we
# still run the command rather than refusing to work.
bounded() {
  if have timeout; then
    timeout "$@"
  else
    shift
    "$@"
  fi
}

add_path() {
  case ":$PATH:" in
    *":$1:"*) ;;
    *)
      PATH="$1:$PATH"
      export PATH
      ;;
  esac
}

fetch() { # fetch <url> -> stdout
  if have curl; then
    bounded "$NET_TIMEOUT" curl -LsSf "$1"
  elif have wget; then
    bounded "$NET_TIMEOUT" wget -qO- "$1"
  else
    return 1
  fi
}

as_root() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  else
    sudo "$@"
  fi
}

# The system package manager, or "" when this host has none we know.
pkg_manager() {
  for m in apt-get dnf yum pacman zypper apk brew; do
    if have "$m"; then
      echo "$m"
      return 0
    fi
  done
  echo ""
}

pkg_install() { # pkg_install <package>
  mgr=$(pkg_manager)
  [ -n "$mgr" ] || return 1
  # brew refuses to run as root; everything else needs to be root or have sudo.
  if [ "$mgr" != brew ] && [ "$(id -u)" -ne 0 ] && ! have sudo; then return 1; fi
  case "$mgr" in
    apt-get)
      bounded 180 as_root apt-get update -qq >/dev/null 2>&1 || true
      bounded "$NET_TIMEOUT" as_root apt-get install -y -qq "$1" >/dev/null 2>&1
      ;;
    dnf | yum) bounded "$NET_TIMEOUT" as_root "$mgr" install -y "$1" >/dev/null 2>&1 ;;
    pacman) bounded "$NET_TIMEOUT" as_root pacman -S --noconfirm "$1" >/dev/null 2>&1 ;;
    zypper) bounded "$NET_TIMEOUT" as_root zypper --non-interactive install "$1" >/dev/null 2>&1 ;;
    apk) bounded "$NET_TIMEOUT" as_root apk add "$1" >/dev/null 2>&1 ;;
    brew) bounded "$NET_TIMEOUT" brew install "$1" >/dev/null 2>&1 ;;
  esac
}

# ensure_tool <binary> <package> <hint> — install it, or say exactly what to run.
ensure_tool() {
  if have "$1"; then
    note "$1: present"
    return 0
  fi
  if [ "$BOOTSTRAP" -eq 0 ]; then
    note "warning: $1 not found (--no-bootstrap). Install it with: $3"
    return 1
  fi
  note "$1 not found — installing it"
  if pkg_install "$2" && have "$1"; then
    note "$1 installed"
    return 0
  fi
  note "warning: could not install $1 automatically. Install it with: $3"
  return 1
}

ensure_uv() {
  if have uv; then
    note "uv: $(uv --version)"
    return 0
  fi
  UV_HINT='curl -LsSf https://astral.sh/uv/install.sh | sh'
  [ "$BOOTSTRAP" -eq 1 ] || die "uv is required and --no-bootstrap was given.
  Install it with:  $UV_HINT"
  note "uv not found — installing it from https://astral.sh/uv"
  if ! fetch https://astral.sh/uv/install.sh > "$TMPD/uv-install.sh"; then
    die "could not download the uv installer (no network, or no curl/wget).
  Install it yourself with:  $UV_HINT"
  fi
  [ -s "$TMPD/uv-install.sh" ] || die "the uv installer downloaded empty — check the network"
  # The installer also writes the PATH line into the shell profile, which is what a
  # student wants: the next shell has uv without this script being involved.
  bounded "$NET_TIMEOUT" sh "$TMPD/uv-install.sh" >/dev/null 2>&1 || die "the uv installer failed"
  add_path "${XDG_BIN_HOME:-$HOME/.local/bin}"
  add_path "$HOME/.local/bin"
  have uv || die "uv installed but is not on PATH — open a new shell and re-run this installer"
  note "uv installed: $(uv --version)"
}

looks_like_project() { [ -d "$1/_bmad" ]; }

# Two directories this must never wire up, however it was pointed at them.
#
# Its own: a student extracts the zip, cds into it and runs this — the skills,
# .waves/ and a .gitignore would land in the bundle folder, no error printed, and
# their project would get nothing.
#
# The home directory: there `.claude/` is not a project's, it is the coding CLI's
# GLOBAL configuration. `waves init` would register the hook relay in the settings
# every project reads and drop ten skills into the personal skills directory —
# and the damage is invisible until every future session starts running a relay
# for a project that has none.
refuse_unsuitable_dir() {
  case "$1" in
    "$SELF_DIR" | "$SELF_DIR"/*)
      die "that is this installer's own folder, not a project:
  $1
  Re-run with --project <your project>, or cd into the project first."
      ;;
  esac
  if [ "$1" = "$HOME" ]; then
    die "that is your home directory, not a project:
  $1
  Installing there would register the hook relay in your GLOBAL coding-CLI settings
  and drop the skills into your personal skills directory, affecting every project.
  Name the project instead: --project <dir>."
  fi
}

# Confirm the target BEFORE anything is installed. Asking after the machine level
# would mean a student who mistyped has already paid for the whole install.
resolve_project() {
  step "project"
  DEFAULT=$(CDPATH= cd -- "$PROJECT" 2>/dev/null && pwd) || die "directory does not exist: $PROJECT"
  if [ "$PROJECT_GIVEN" -eq 1 ]; then
    PROJECT="$DEFAULT"
    refuse_unsuitable_dir "$PROJECT"
    note "target: $PROJECT"
    return 0
  fi
  # Enter is only offered where accepting it is defensible. A directory that is
  # neither a BMAD project nor a git repository is almost certainly not where the
  # student meant to install, and a default there is a trap: they press Enter.
  if looks_like_project "$DEFAULT"; then
    note "found _bmad/ here."
    allow_default=1
  elif [ -d "$DEFAULT/.git" ]; then
    note "this is a git repository, but has no _bmad/ yet."
    allow_default=1
  else
    note "this directory is neither a BMAD project nor a git repository."
    allow_default=0
  fi
  [ "$DEFAULT" != "$HOME" ] || allow_default=0
  [ -t 0 ] || die "no terminal to ask on — name the project with --project <dir>."
  tries=0
  while [ "$tries" -lt 3 ]; do
    tries=$((tries + 1))
    echo ""
    if looks_like_project "$DEFAULT"; then
      echo "  wire up this project?"
    else
      echo "  which project should I wire up?"
    fi
    if [ "$allow_default" -eq 1 ]; then
      echo "  [Enter = $DEFAULT]"
    else
      echo "  (type a path — there is no sensible default here)"
    fi
    printf "  path: "
    read -r answer || answer=""
    if [ -z "$answer" ]; then
      if [ "$allow_default" -eq 1 ]; then
        answer="$DEFAULT"
      else
        note "a path is required here"
        continue
      fi
    fi
    case "$answer" in "~/"*) answer="$HOME/${answer#"~/"}" ;; esac
    if [ -d "$answer" ]; then
      PROJECT=$(CDPATH= cd -- "$answer" && pwd)
      refuse_unsuitable_dir "$PROJECT"
      looks_like_project "$PROJECT" ||
        note "warning: no _bmad/ there — install the BMAD Method in it first"
      note "target: $PROJECT"
      return 0
    fi
    note "not a directory: $answer"
  done
  die "no usable project directory after 3 tries"
}

ensure_python() {
  # uv downloads a managed interpreter on its own when a project needs one, so this
  # is about saying so out loud rather than letting it happen inside another command.
  if uv python find ">=3.11" >/dev/null 2>&1; then
    note "python: $(uv python find ">=3.11" 2>/dev/null)"
    return 0
  fi
  note "no python 3.11+ found — installing one through uv"
  if bounded "$NET_TIMEOUT" uv python install >/dev/null 2>&1; then
    note "python installed: $(uv python find ">=3.11" 2>/dev/null)"
  else
    note "warning: uv could not install a python; it will try again during the tool install"
  fi
}

while [ $# -gt 0 ]; do
  case "$1" in
    --project)
      [ $# -ge 2 ] || die "--project needs a directory"
      PROJECT="$2"
      PROJECT_GIVEN=1
      shift 2
      ;;
    --cli)
      [ $# -ge 2 ] || die "--cli needs a name"
      CLIS="$CLIS $2"
      shift 2
      ;;
    --find-links)
      [ $# -ge 2 ] || die "--find-links needs a directory"
      FIND_LINKS="$2"
      shift 2
      ;;
    --tool-only) MODE=tool; shift ;;
    --project-only) MODE=project; shift ;;
    --via-bmad)
      VIA_BMAD=1
      shift
      ;;
    --no-tui)
      EXTRA=""
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --no-bootstrap)
      BOOTSTRAP=0
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *) die "unknown argument: $1 (try --help)" ;;
  esac
done

echo "riaworks-waves $VERSION — bundle installer"

# ---------------------------------------------------------------- preflight
if [ "$MODE" != tool ]; then
  resolve_project
fi

step "preparing prerequisites"

if [ "$MODE" != project ]; then
  ensure_uv
  ensure_python
fi

# git's floor is enforced by `waves run` itself (2.34), so a host below it installs
# fine and fails at the first run. Say so now rather than there.
if ensure_tool git git "your system's package manager"; then
  GIT_V=$(git --version | sed 's/[^0-9.]*//; s/ .*//')
  GIT_MAJOR=${GIT_V%%.*}
  GIT_REST=${GIT_V#*.}
  GIT_MINOR=${GIT_REST%%.*}
  if [ "$GIT_MAJOR" -lt 2 ] || { [ "$GIT_MAJOR" -eq 2 ] && [ "$GIT_MINOR" -lt 34 ]; }; then
    note "warning: git $GIT_V is below the 2.34 floor — runs will refuse to start"
  else
    note "git: $GIT_V"
  fi
fi

# tmux is the POSIX multiplexer backend: needed to RUN, not to install.
ensure_tool tmux tmux "your system's package manager" || true

if [ "$VIA_BMAD" -eq 1 ]; then
  ensure_tool npx nodejs "install Node.js from https://nodejs.org" \
    || die "--via-bmad needs npx (Node.js); drop the flag to skip BMAD registration"
fi

# ------------------------------------------------------------ machine level
WAVES=waves
if [ "$MODE" != project ]; then
  step "installing the orchestrator (machine level)"
  WHEEL="$SELF_DIR/wheels/$WHEEL_NAME"
  [ -f "$WHEEL" ] || die "wheel missing from the bundle: wheels/$WHEEL_NAME"

  BEFORE=""
  if have waves; then BEFORE=$(waves --version 2>/dev/null || true); fi
  [ -z "$BEFORE" ] || note "already installed: $BEFORE"

  # --python is not optional: `uv tool install` otherwise resolves against the
  # system's default interpreter and fails outright on a host whose `python3` is
  # older than the wheel's floor — which is most machines that have never run any
  # of this. A version REQUEST (not a path) also lets uv download a managed 3.11+
  # when the host has none.
  set -- --force --python ">=3.11"
  if [ -n "$FIND_LINKS" ]; then
    [ -d "$FIND_LINKS" ] || die "--find-links is not a directory: $FIND_LINKS"
    set -- "$@" --find-links "$FIND_LINKS" --offline
    note "resolving dependencies offline from $FIND_LINKS"
  fi
  # `uv tool install` puts waves in uv's own managed environment: no virtualenv to
  # activate, and no PEP 668 externally-managed conflict with the system python.
  uv tool install "$@" "${WHEEL}${EXTRA}"

  # Use the binary uv just wrote, not whatever `waves` the PATH resolves to: on a
  # machine that already carries one from a source checkout, the PATH copy is a
  # different program and the project would be wired up by it.
  BIN=$(uv tool dir --bin 2>/dev/null || echo "$HOME/.local/bin")
  WAVES="$BIN/waves"
  [ -x "$WAVES" ] || die "waves was installed but is not at $WAVES — check 'uv tool list'"
  ON_PATH=$(command -v waves || true)
  if [ -z "$ON_PATH" ]; then
    # Telling a student to fix their own PATH is where an install stops being an
    # install. uv writes the line into the shell profile itself; all that is left
    # is saying that the CURRENT shell still does not have it.
    if [ "$BOOTSTRAP" -eq 1 ] && uv tool update-shell >/dev/null 2>&1; then
      note "added $BIN to your shell profile — open a new shell to get 'waves' on PATH"
    else
      note "warning: $BIN is not on your PATH"
      note "         run 'uv tool update-shell' and open a new shell, or add it yourself"
    fi
    add_path "$BIN"
  elif [ "$ON_PATH" != "$WAVES" ]; then
    note "warning: a different waves is ahead on your PATH: $ON_PATH"
    note "         this install wired the project with $WAVES"
  fi
  note "installed: $("$WAVES" --version)"
fi

if [ "$MODE" = tool ]; then
  echo
  echo "Machine level done. Wire up a project with:  sh install.sh --project-only --project <dir>"
  exit 0
fi

# ------------------------------------------------------------ project level
if [ "$MODE" = project ]; then
  WAVES=$(command -v waves || true)
  if [ -z "$WAVES" ]; then
    BIN=$(uv tool dir --bin 2>/dev/null || echo "$HOME/.local/bin")
    [ -x "$BIN/waves" ] || die "waves is not installed — run without --project-only first"
    WAVES="$BIN/waves"
  fi
  note "using: $("$WAVES" --version) ($WAVES)"
fi

step "wiring up the project: $PROJECT"

looks_like_project "$PROJECT" ||
  note "warning: no _bmad/ here — install the BMAD Method first (npx bmad-method install)"

# An upgrade must refresh the per-project skill copies, or the project keeps
# yesterday's prose against today's tool. Detect it rather than making the
# student remember a flag.
REFRESH=$FORCE
if [ -d "$PROJECT/.claude/skills/waves-core-orchestrator" ] || [ -d "$PROJECT/.agents/skills/waves-core-orchestrator" ]; then
  if [ "$REFRESH" -eq 0 ]; then
    note "existing skills found — refreshing them for $VERSION"
    REFRESH=1
  fi
fi

set -- --project "$PROJECT"
for c in ${CLIS:-claude}; do set -- "$@" --cli "$c"; done
[ "$REFRESH" -eq 0 ] || set -- "$@" --force-skills
"$WAVES" init "$@"

# ---------------------------------------------------------- BMAD registration
if [ "$VIA_BMAD" -eq 1 ]; then
  step "registering the module with the BMAD installer"
  SRC="$SELF_DIR/$PKG_DIR"
  [ -d "$SRC" ] || die "the module tree is missing from the bundle: $PKG_DIR"
  TOOLS=""
  for c in ${CLIS:-claude}; do
    case "$c" in
      claude) TOOLS="$TOOLS,claude-code" ;;
      codex | gemini | copilot | antigravity | opencode | opencode-http) TOOLS="$TOOLS,$c" ;;
      *) die "cannot map CLI '$c' to a BMAD tool id — register it by hand (see INSTALL.md)" ;;
    esac
  done
  npx bmad-method install --custom-source "$SRC" --tools "${TOOLS#,}"
fi

# ------------------------------------------------------------------ preflight
step "preflight"
# validate exits 1 on a real problem (no BMAD install yet, missing dev primitive,
# git too old). That is information for the student, not a failed installation:
# everything this script writes is already on disk and correct.
if "$WAVES" validate --project "$PROJECT"; then
  RC=0
else
  RC=$?
fi

echo
if [ "$RC" -eq 0 ]; then
  echo "Done. riaworks-waves $VERSION is installed and this project is ready."
else
  echo "Installed, but the preflight above found problems to fix before the first run."
fi
echo "Next:  /waves-master-tui in your coding CLI launches a run; /waves-master-parallelism plans an epic."
exit "$RC"
