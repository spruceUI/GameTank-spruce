"""Wrapper mode's menu: one focused window a pad can drive, game paused while
it is open. Defined for gte.cpp only; wrapper mode also changes audio timing
in audio_coprocessor.cpp, which stays upstream's."""

PATH = "src/gte.cpp"
src = open(PATH).read()
if "#define WRAPPER_MODE" in src:
    raise SystemExit("gamepad_menu.py: already patched")
open(PATH, "w").write("#define WRAPPER_MODE 1\n" + src)
