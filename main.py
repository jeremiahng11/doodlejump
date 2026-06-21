# pygame MUST be imported at the top level here: pygbag scans main.py's
# top-level imports to decide which packages to preload into the browser
# runtime. pygame is only imported inside game.py (a submodule), so without
# this line pygbag never fetches the pygame wheel and the game hangs on a
# blank screen after start. Do not remove.
import pygame
import asyncio
from game import Game


async def main():
    game = Game()
    await game.run()


# asyncio.run works both on desktop CPython and under pygbag's WebAssembly runtime.
asyncio.run(main())
