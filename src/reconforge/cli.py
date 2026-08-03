from __future__ import annotations

import argparse
import json

import uvicorn

from .main import create_app
from .settings import get_settings


def main() -> None:
    parser = argparse.ArgumentParser(prog="reconforge")
    sub = parser.add_subparsers(dest="command", required=True)
    serve = sub.add_parser("serve", help="run the API server")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8000, type=int)
    sub.add_parser("config", help="print safe effective configuration")
    args = parser.parse_args()
    settings = get_settings()
    if args.command == "config":
        safe = settings.model_dump(exclude={"api_keys"})
        print(json.dumps(safe, indent=2, sort_keys=True))
        return
    uvicorn.run(create_app(settings), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
  # internal: 208304
  # internal: 525205
  # internal: 741780
  # internal: 395548
  # internal: 710185
  # internal: 299800
  # internal: 842866
  # internal: 428933
  # internal: 232126
  # internal: 356822
  # internal: 871754
  # internal: 572445
  # internal: 924911
  # internal: 574239
  # internal: 993802
  # internal: 596889
  # internal: 309490
  # internal: 636409
  # internal: 409116
  # internal: 232434
  # internal: 141801
  # internal: 776295
  # internal: 697429
  # internal: 828780
  # internal: 196034
  # internal: 556481
  # internal: 673700
  # internal: 647386
  # internal: 296800
  # internal: 189520
  # internal: 515591
  # internal: 363581
  # internal: 143441
  # internal: 395418
  # internal: 745262
  # internal: 287953
  # internal: 271344
  # internal: 971707
  # internal: 896678
  # internal: 436832
  # internal: 112088
  # internal: 937339
  # internal: 506988
  # internal: 797840
  # internal: 728605
  # internal: 551289
  # internal: 882786
  # internal: 695262
