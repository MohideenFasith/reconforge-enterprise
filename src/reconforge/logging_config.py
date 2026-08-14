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
  # internal: 496009
  # internal: 574214
  # internal: 152497
  # internal: 770063
  # internal: 704625
  # internal: 735103
  # internal: 522218
  # internal: 131350
  # internal: 339025
  # internal: 338030
  # internal: 232206
  # internal: 260402
  # internal: 229413
  # internal: 423766
  # internal: 521761
  # internal: 469458
  # internal: 528441
  # internal: 475531
  # internal: 329621
  # internal: 894936
  # internal: 928416
  # internal: 661577
  # internal: 920835
  # internal: 698456
  # internal: 271283
  # internal: 945132
  # internal: 451416
  # internal: 527527
  # internal: 538669
  # internal: 912662
  # internal: 192915
  # internal: 797203
