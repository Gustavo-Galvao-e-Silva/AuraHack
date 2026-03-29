import asyncio
import json
import sys
import threading
import requests
import websockets

HOST     = "35.172.182.0"
PORT     = 6000
HTTP_URL = f"http://{HOST}:{PORT}"
WS_URL   = f"ws://{HOST}:{PORT}"


def fetch_history(conversation_id: str, perspective: str) -> None:
    print("\n── Message history ──────────────────────────────")
    try:
        r = requests.get(
            f"{HTTP_URL}/chat/history/{conversation_id}",
            params={"perspective": perspective},
            timeout=5,
        )
        r.raise_for_status()
        data = r.json()
        messages = data.get("messages", [])
        if not messages:
            print("  (no messages yet)")
        for m in messages:
            arrow = "→" if m["role"] == "self" else "←"
            print(f"  {arrow} {m['content']}  [{m['created_at'][:19]}]")
    except requests.RequestException as e:
        print(f"  [HTTP error] {e}")
    print("─────────────────────────────────────────────────\n")


async def ws_session(my_email: str, other_email: str) -> None:
    conversation_id = ":".join(sorted([my_email, other_email]))
    ws_endpoint     = f"{WS_URL}/chat/ws/{conversation_id}"

    print(f"Connecting to {ws_endpoint} ...")

    async with websockets.connect(ws_endpoint) as ws:

        # ---- identity handshake ----
        challenge = json.loads(await ws.recv())
        print(f"[server] {challenge.get('message', challenge)}")

        await ws.send(json.dumps({"type": "identify", "email": my_email}))

        ack = json.loads(await ws.recv())
        if ack.get("type") != "connection_established":
            print(f"[error] unexpected response: {ack}")
            return

        print(f"[server] connected — conversation {ack['conversation_id']}\n")

        # ---- pull history over HTTP ----
        fetch_history(conversation_id, my_email)

        print(f'Type your message and press Enter to send to {other_email}.')
        print('Type "quit" to exit.\n')

        # ---- receive loop ----
        async def receive_loop() -> None:
            try:
                async for raw in ws:
                    msg = json.loads(raw)
                    if msg.get("type") == "new_message":
                        m = msg["message"]
                        if m["role"] == "other":
                            print(f"\r\033[K  ← {other_email}: {m['content']}")
                            print("send> ", end="", flush=True)
                    elif msg.get("type") == "error":
                        print(f"\r[server error] {msg.get('message')}")
                        print("send> ", end="", flush=True)
            except websockets.ConnectionClosed:
                print("\n[disconnected]")

        loop     = asyncio.get_event_loop()
        recv_task = asyncio.create_task(receive_loop())

        # ---- send loop (stdin in a thread) ----
        def read_stdin() -> None:
            while True:
                try:
                    line = input("send> ").strip()
                except (EOFError, KeyboardInterrupt):
                    asyncio.run_coroutine_threadsafe(ws.close(), loop)
                    return

                if line.lower() == "quit":
                    asyncio.run_coroutine_threadsafe(ws.close(), loop)
                    return

                if not line:
                    continue

                payload = json.dumps({"content": line})
                asyncio.run_coroutine_threadsafe(ws.send(payload), loop)

        threading.Thread(target=read_stdin, daemon=True).start()
        await recv_task


def main() -> None:
    print("╔══════════════════════════════════════╗")
    print("║       Chat Server Test Client        ║")
    print("╚══════════════════════════════════════╝\n")

    try:
        my_email    = input("Your email:      ").strip()
        other_email = input("Other's email:   ").strip()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

    if not my_email or not other_email:
        print("[error] both emails are required")
        sys.exit(1)

    try:
        asyncio.run(ws_session(my_email, other_email))
    except KeyboardInterrupt:
        pass
    except OSError as e:
        print(f"\n[error] could not connect: {e}")
        print(f"        Is the server running on port {PORT}?")
        sys.exit(1)


if __name__ == "__main__":
    main()
