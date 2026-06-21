# pygame MUST be imported at the top level here: pygbag scans main.py's
# top-level imports to decide which packages to preload into the browser
# runtime. pygame is only imported inside game.py (a submodule), so without
# this line pygbag never fetches the pygame wheel and the game hangs on a
# blank screen after start. Do not remove.
import pygame
import asyncio
import traceback


async def _show_error(text):
    """Draw a Python traceback onto the canvas.

    On the web there is no terminal, so an uncaught exception just leaves a
    blank screen. This renders the error in-page so it can be read (and
    screenshotted) without opening the browser dev console.
    """
    try:
        pygame.init()
        screen = pygame.display.get_surface() or pygame.display.set_mode((640, 900))
    except Exception:
        print(text, flush=True)
        return

    font = pygame.font.Font(None, 22)
    lines = []
    for raw in text.replace("\t", "    ").rstrip().split("\n"):
        while len(raw) > 72:
            lines.append(raw[:72])
            raw = raw[72:]
        lines.append(raw)

    while True:
        screen.fill((18, 18, 28))
        y = 16
        for ln in lines:
            screen.blit(font.render(ln, True, (255, 150, 150)), (10, y))
            y += 22
        pygame.display.flip()
        await asyncio.sleep(0)


async def main():
    try:
        from game import Game
        game = Game()
        await game.run()
    except BaseException:
        tb = traceback.format_exc()
        print(tb, flush=True)
        await _show_error(tb)


# asyncio.run works both on desktop CPython and under pygbag's WebAssembly runtime.
asyncio.run(main())
