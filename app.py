from __future__ import annotations

import argparse
import os
import sys
import threading
import webbrowser
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from autoapply.server import run_server  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AutoApply Local - 本地职位筛选、材料生成与浏览器填表助手"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="启动后不自动打开浏览器",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="自定义本地数据目录",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")
    if args.data_dir:
        os.environ["AUTOAPPLY_DATA_DIR"] = str(args.data_dir.resolve())
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        print("为保护个人资料，本工具只允许绑定到本机回环地址。", file=sys.stderr)
        return 2

    url = f"http://{args.host}:{args.port}"
    if not args.no_open:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    print(f"AutoApply Local 已启动：{url}")
    print("按 Ctrl+C 停止。个人资料只保存在本机 data 目录。")
    try:
        run_server(args.host, args.port)
    except OSError as exc:
        if getattr(exc, "winerror", None) == 10048 or getattr(exc, "errno", None) == 98:
            print(f"端口 {args.port} 已被占用。请关闭旧实例后重试。", file=sys.stderr)
            return 2
        raise
    except KeyboardInterrupt:
        print("\n已安全停止。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
