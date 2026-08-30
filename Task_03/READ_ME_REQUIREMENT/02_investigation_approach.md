# Approach Used to Investigate the Issues



&#x20;**Read before touching anything.** Started with `git status` / `git diff --stat` to see what state the tree was already in, then read the existing
`restoration-report.md` and `README.md` to understand what the archive is doing



1. **Compiled first, ran second.** `cargo check --workspace` and
`cargo test --workspace` surfaced the compatibility-policy gap (via a
failing/missing test case) and the build-hygiene warnings without needing
to run anything.

2. **Ran each archive from its own directory** (`cd archives/<name> \&\& cargo run`) to separate "does it compile" from "does it behave correctly at
runtime," which is how the `config/application.toml` path issue and the
missing `config/assets/` directory were found — both are invisible to
`cargo build`.

3. **Traced data flow through `navnet-core`** — legacy YAML → migration →
compatibility check → registry → persistence — to find where the pipeline
in East Blue's `main.rs` stopped short of what the module structure
implied it should do.

4. **Verified with tests, not just manual runs.** Added integration tests
that pin down the specific behaviors that were previously unverified
(`V1` rejecting `V2`, registry round-tripping through `save`/`load`,
legacy snapshot migration), so the fixes are checked by `cargo test --workspace` going forward rather than only by eyeballing log output.

