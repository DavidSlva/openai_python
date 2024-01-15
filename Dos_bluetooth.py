import asyncio
from bleak import discover

async def main():
    devices = await discover()
    for device in devices:
        print(device)
        print("Found device:", device.name, "with address:", device.address)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
