# Scientific Software Connectors

## Supported Roles

| Tool | Default role | Accepted outputs |
|---|---|---|
| Gaussian16 | input-template generation and log parsing | `.gjf`, `.com`, `.log`, `.out`, `.chk`, `.fchk` |
| formchk | command-template generation | `.chk`, `.fchk` |
| cubegen | density/ESP/MO command-template generation and cube parsing | `.fchk`, `.cube`, `.cub` |
| Multiwfn | QTAIM/NCI/ESP script-template generation and output parsing | `.fchk`, `.wfn`, `.wfx`, `.cube`, `.txt` |
| GoodVibes | output parsing and command-template generation | `.log`, `.out`, `.txt`, `.csv` |
| RDKit | local molecular parsing/conformer library | `.smi`, `.mol`, `.sdf`, `.xyz` |
| SLURM | submission-script generation only | `.sh`, `.gjf`, `.com` |

## Execution Modes

- `template_only`: generate text; never execute.
- `parse_only`: parse user-provided text/file read-only.
- `dry_run`: return the planned executable, arguments, files, limits, and rejection reasons.
- `confirmed_execute`: valid only in an isolated external runner, never in the normal API process.

## Mandatory Real-Runner Controls

If a downstream project enables real execution, require all controls:

1. Executable allowlist resolved to a configured absolute file.
2. Argument arrays, not shell strings.
3. Resolved input/output paths contained in a dedicated job directory.
4. Extension and MIME validation.
5. CPU, memory, wall-time, disk, and output-size limits.
6. No inherited user shell environment beyond an allowlisted environment map.
7. Explicit confirmation tied to one immutable job digest.
8. Audit log containing tool version, executable hash/path, arguments, input hashes, timestamps, exit code, and output hashes.
9. Cancellation and timeout handling.
10. Output remains C evidence until scientific validation promotes it.

Reject command templates containing `; & | $ < >` or backticks. A redirection-based template may be shown to a human but cannot enter the runner.

## Configuration

Prefer environment variables such as:

- `GAUSSIAN16_PATH`
- `FORMCHK_PATH`
- `CUBEGEN_PATH`
- `MULTIWFN_PATH`
- `GOODVIBES_PATH`
- `SLURM_SBATCH_PATH`

Path inspection must not execute a version command. Version checks require the same isolated-runner controls.
