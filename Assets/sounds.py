import sys
import pygame

pygame.mixer.init()

# pygbag/web (SDL2_mixer under WebAssembly) only plays OGG; desktop pygame plays
# WAV fine. We keep WAV in the repo for desktop and the Docker build transcodes
# them to OGG for the web bundle. The extension is chosen at runtime and the
# path is built with an f-string on purpose: pygbag's build-time "optimizing
# pass" rewrites *static* "....wav" string literals to ".ogg" (which previously
# left the code pointing at .ogg files that did not exist). A computed path is
# not rewritten, so the reference always matches the files actually shipped.
_EXT = "ogg" if sys.platform == "emscripten" else "wav"


def _sound(name):
    return pygame.mixer.Sound(f"Assets/Sounds/{name}.{_EXT}")


jump = _sound("jump")
shoot_1 = _sound("shoot_1")
shoot_2 = _sound("shoot_2")
tile_break = _sound("break")
tile_disappear = _sound("pop")
button = _sound("button")
monster = _sound("monster")
fall = _sound("fall")
thump = _sound("thump")
die_1 = _sound("die_1")
die_2 = _sound("die_2")
suck = _sound("suck")
spring = _sound("spring")
trampoline = _sound("trampoline")
jetpack = _sound("jetpack")
propeller = _sound("propeller")
block = _sound("block")
activate_shield = _sound("activate_shield")
explosion = _sound("explode")

ufo = _sound("ufo")
ufo_suck = _sound("ufo_suck")
