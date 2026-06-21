import asyncio
from game import Game


async def main():
    game = Game()
    await game.run()


# asyncio.run works both on desktop CPython and under pygbag's WebAssembly runtime.
asyncio.run(main())
