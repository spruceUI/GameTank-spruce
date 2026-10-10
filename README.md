# GameTank-spruce

Cross-compiled [GameTankEmulator](https://github.com/clydeshaffer/GameTankEmulator) standalone builds for [spruceOS](https://github.com/spruceUI/spruceOS).

## Builds

| Build | Output | Devices | Base |
|-------|--------|---------|------|
| Universal | `gametank-aarch64.tar.gz` | 64-bit spruce devices | Ubuntu 20.04 (glibc 2.31) |
| A30 | `gametank-a30.tar.gz` | Miyoo A30 | A30 buildroot toolchain (glibc 2.23) |

## Usage

```bash
# Trigger a build
gh workflow run build-all.yml

# Download the output
gh release download beta-main -p "gametank-*.tar.gz"
```

## Output structure

```
GameTankEmulator     # standalone binary, libstdc++ linked statically
commit_hash.txt      # upstream commit it was built from
```

## Patches

`patches/common` applies to every build, `patches/universal` and `patches/a30` to one. `*.patch` files go through `git apply`, `*.py` files are run from the source root.
