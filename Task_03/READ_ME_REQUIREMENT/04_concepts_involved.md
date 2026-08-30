# Rust, Git, and Linux Concepts Involved

- **Modules, structs, traits**: `CompatibilityLayer` implements a
  `CompatibilityPolicy` trait; fixing `enforce` meant understanding how the
  trait method related to the layer's own `is_compatible` helper rather than
  duplicating (and getting wrong) similar logic inline.

- **Ownership & borrowing**: `StationRegistry::save` takes `&self` and a
  generic `P: AsRef<Path>` parameter, borrowing the registry's stations for
  serialization without consuming the registry.

- **Error handling**: Both `enforce` and `save` return `Result` types
  (`CompatibilityError`, `anyhow`/`io::Result`-style errors), so fixes had to
  preserve existing error variants rather than introduce panics.

- **Testing**: Integration tests under `tests/` exercise a crate's public API
  as an external consumer would, which is why they caught the
  target-`V1`-doesn't-reject-`V2` bug that unit tests hadn't covered.

- **Cargo workspaces**: A single workspace `Cargo.toml` ties the four
  archives and `navnet-core` together; `-p <crate>` lets you build/run one
  member without building the whole workspace's binaries.

- **Git tracking of empty directories**: Git tracks files, not directories,
  so an empty `config/assets/` directory silently disappears on clone unless
  a placeholder file (`.gitkeep`) is committed inside it.

- **Working directory vs. crate root**: On Linux, relative paths in a
  running process resolve against the shell's current working directory, not
  the source file's location or the crate manifest's directory — which is
  why `cargo run -p reverse-mountain` from the workspace root couldn't find
  `config/application.toml`, but running from inside
  `archives/reverse-mountain/` could.
