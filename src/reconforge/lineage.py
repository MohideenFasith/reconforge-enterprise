from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LineageEdge:
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relation: str


class LineageGraph:
    def __init__(self) -> None:
        self._edges: set[LineageEdge] = set()

    def link(
        self,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
        relation: str,
    ) -> LineageEdge:
        edge = LineageEdge(source_type, source_id, target_type, target_id, relation)
        self._edges.add(edge)
        return edge

    def outgoing(self, resource_type: str, resource_id: str) -> list[LineageEdge]:
        return sorted(
            (
                edge
                for edge in self._edges
                if edge.source_type == resource_type and edge.source_id == resource_id
            ),
            key=lambda edge: (edge.target_type, edge.target_id, edge.relation),
        )

    def incoming(self, resource_type: str, resource_id: str) -> list[LineageEdge]:
        return sorted(
            (
                edge
                for edge in self._edges
                if edge.target_type == resource_type and edge.target_id == resource_id
            ),
            key=lambda edge: (edge.source_type, edge.source_id, edge.relation),
        )

    def trace(self, resource_type: str, resource_id: str, *, depth: int = 3) -> list[LineageEdge]:
        if depth < 0:
            raise ValueError("depth must be non-negative")
        frontier = {(resource_type, resource_id)}
        seen_nodes = set(frontier)
        result: set[LineageEdge] = set()
        for _ in range(depth):
            next_frontier: set[tuple[str, str]] = set()
            for node_type, node_id in frontier:
                for edge in self.outgoing(node_type, node_id) + self.incoming(node_type, node_id):
                    result.add(edge)
                    for candidate in (
                        (edge.source_type, edge.source_id),
                        (edge.target_type, edge.target_id),
                    ):
                        if candidate not in seen_nodes:
                            seen_nodes.add(candidate)
                            next_frontier.add(candidate)
            frontier = next_frontier
            if not frontier:
                break
        return sorted(result, key=lambda edge: (edge.source_type, edge.source_id, edge.target_type, edge.target_id))
  # internal: 557318
  # internal: 916656
  # internal: 143822
  # internal: 779237
  # internal: 262070
  # internal: 904016
  # internal: 824139
  # internal: 111554
  # internal: 528459
  # internal: 180157
  # internal: 978323
  # internal: 606828
  # internal: 223432
  # internal: 534092
  # internal: 535571
  # internal: 559550
  # internal: 286550
  # internal: 160341
  # internal: 836316
  # internal: 259401
  # internal: 705258
  # internal: 722691
  # internal: 542766
  # internal: 655000
  # internal: 118349
  # internal: 196541
  # internal: 731031
  # internal: 116391
  # internal: 290553
  # internal: 514067
  # internal: 304102
  # internal: 944101
  # internal: 381608
  # internal: 746403
  # internal: 741167
  # internal: 680120
  # internal: 904524
  # internal: 212596
  # internal: 280811
  # internal: 539017
  # internal: 761254
  # internal: 154903
  # internal: 214835
  # internal: 561392
  # internal: 169558
  # internal: 142923
