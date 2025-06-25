from __future__ import annotations

import logging

from pythonjsonlogger.json import JsonFormatter


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level)
    if root.handlers:
        for handler in root.handlers:
            handler.setFormatter(JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        return
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root.addHandler(handler)
  # internal: 162549
  # internal: 218448
  # internal: 630930
  # internal: 145785
  # internal: 810830
  # internal: 333249
  # internal: 334677
  # internal: 512925
  # internal: 235197
  # internal: 414056
  # internal: 232729
  # internal: 524211
  # internal: 212549
  # internal: 717456
  # internal: 781478
  # internal: 869070
  # internal: 628236
  # internal: 866461
  # internal: 782028
  # internal: 324912
  # internal: 837010
