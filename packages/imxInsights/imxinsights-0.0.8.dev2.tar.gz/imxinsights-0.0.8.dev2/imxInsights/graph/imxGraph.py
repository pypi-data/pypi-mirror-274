import heapq
from typing import List, Optional

import matplotlib.pyplot as plt
import networkx as nx
from networkx import NetworkXNoPath
from shapely import LineString, MultiLineString, Point
from shapely.ops import linemerge

from imxInsights.graph.imxGraphModels import (
    DirectionEnum,
    GraphRoute,
    MicroLinkConnection,
    MicroLinkConnectionRepo,
    MicroLinkRepo,
    MicroNodeRepo,
    PathEdge,
    PathEdgeData,
    RailConnectionRepo,
)
from imxInsights.graph.imxGraphSituationProtocol import ImxSituationRepoMinimalProtocol
from imxInsights.utils.log import logger
from imxInsights.utils.shapely_helpers import cut, cut_profile, offset_linestring


class ImxGraph:
    def __init__(
        self,
        graph: nx.DiGraph,
        imx_situation: ImxSituationRepoMinimalProtocol,
        micro_link_repo: MicroLinkRepo,
        micro_node_repo: MicroNodeRepo,
        rail_connections_repo: RailConnectionRepo,
        micro_link_connections: MicroLinkConnectionRepo,
    ):
        self.g = graph
        self.imx_situation = imx_situation
        self.micro_link_repo = micro_link_repo
        self.micro_node_repo = micro_node_repo
        self.rail_connections_repo = rail_connections_repo
        self.micro_link_connections = micro_link_connections
        self._path_finding_cash = {}

    def _get_plot(self):
        fig, ax = plt.subplots()
        length = 2
        for edge in self.g.edges:
            edge_data = self.g.get_edge_data(edge[0], edge[1])
            line_source = self.micro_link_repo.get_by_puic(edge[0]).get_shapely()
            line_target = self.micro_link_repo.get_by_puic(edge[1]).get_shapely()

            if edge_data["current_direction"] == "UPSTREAM":
                point_1 = line_source.interpolate(length)
            elif edge_data["current_direction"] == "DOWNSTREAM":
                point_1 = line_source.interpolate(line_source.length - length)
            else:
                raise ValueError()

            if edge_data["next_direction"] == "UPSTREAM":
                point_2 = line_target.interpolate(line_target.length - length)
            elif edge_data["next_direction"] == "DOWNSTREAM":
                point_2 = line_target.interpolate(length)
            else:
                raise ValueError()

            edge_line = offset_linestring(LineString([Point(point_1.x, point_1.y), Point(point_2.x, point_2.y)]), 0.25, "down")
            plt.annotate("", xy=edge_line.coords[0], xytext=edge_line.coords[-1], arrowprops=dict(facecolor="red", arrowstyle="->"))

        for node in self.g.nodes:
            line = self.micro_link_repo.get_by_puic(node).get_shapely()
            x, y = line.xy
            ax.plot(x, y, linewidth=7.0)

        plt.axis("equal")
        return fig

    def draw_graph(self, path: Optional[List[str]] = None):
        """Draws the graph, optionally highlighting a specified path.

        Args:
            path (Optional[List[str]]): A list of PUICs representing the path to highlight. If None, no path is highlighted.
        """
        plt = self._get_plot()
        plt.show()

    def get_edges_path(self, path: List[str], data: bool = True) -> List[PathEdge]:
        edges = []
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]
            if data:
                edge_data = self.g.get_edge_data(source, target)
                # Assuming edge_data contains keys that exactly match the PathEdgeData fields
                # and values that can be directly used to instantiate PathEdgeData
                path_edge_data = PathEdgeData(
                    source_direction=DirectionEnum[edge_data["current_direction"]],
                    target_direction=DirectionEnum[edge_data["next_direction"]],
                    junction_ref=edge_data["junction"],
                    graph_junction=edge_data["graph_junction"],
                    jumper=edge_data["jumper"],
                )
                edge = PathEdge(source, target, path_edge_data)
            else:
                edge = PathEdge(source, target)
            edges.append(edge)
        return edges

    @staticmethod
    def has_cutback_in_path(edges_in_path: List[PathEdge]) -> bool:
        cutback_in_route = False
        for idx, item in enumerate(edges_in_path):
            if idx < len(edges_in_path) - 1:
                if item.data.junction_ref == edges_in_path[idx + 1].data.junction_ref:
                    cutback_in_route = True
        return cutback_in_route

    @staticmethod
    def check_if_not_multiline(rail_con_geometry: List[LineString]) -> bool:
        tester = linemerge(rail_con_geometry)
        if isinstance(tester, MultiLineString):
            return False
        return True

    def get_objects_on_route(
        self,
        micro_link_ref: str,
        measure: Optional[float] = None,
    ) -> List[MicroLinkConnection]:
        if measure:
            return [_ for _ in self.micro_link_connections.get_by_puic(micro_link_ref) if _.measure <= measure]
        else:
            return [_ for _ in self.micro_link_connections.get_by_puic(micro_link_ref)]

    @staticmethod
    def append_objects_on_route(direction: DirectionEnum, objects_on_path, object_on_route):
        if direction == DirectionEnum.UPSTREAM:
            objects_on_path.extend(reversed(object_on_route))
        elif direction == DirectionEnum.DOWNSTREAM:
            objects_on_path.extend(object_on_route)

    def cut_geometry(self, path_edge, mirco_link, measure, target=False):
        line_source = self.micro_link_repo.get_by_puic(mirco_link).get_shapely()
        direction = path_edge.data.source_direction if not target else path_edge.data.target_direction
        line_cut = cut(line_source, measure)

        if measure == 0 or line_source.length == line_cut[0].length:
            return line_cut[0]
        elif direction == DirectionEnum.DOWNSTREAM:
            return line_cut[1] if not target else line_cut[0]
        elif direction == DirectionEnum.UPSTREAM:
            return line_cut[0] if not target else line_cut[1]
        else:
            raise ValueError("should have at least one cut on start mirco_link")

    def _find_paths_without_revisiting_nodes(self, G, source, target, weight="weight", max_weight_increase=0.1, cutoff=15):
        """
        Finds paths from source to target in graph G without revisiting nodes and with a length cutoff.

        Only considers paths with a total weight within 10% of the shortest path's weight and under the specified cutoff.

        Parameters:
        - G: The graph
        - source: Source node
        - target: Target node
        - weight: The edge attribute to use as weight
        - max_weight_increase: Maximum allowed weight increase over the shortest path (as a fraction)
        - cutoff: Maximum number of edges (hops) a path can have

        Returns:
        - A list of tuples, where each tuple contains a path and its weight.
        """
        # Cache key based on function parameters that affect the output
        cache_key = (source, target, weight, max_weight_increase, cutoff)

        # Check if the result is in cache
        if cache_key in self._path_finding_cash.keys():
            return self._path_finding_cash[cache_key]

        # Find the shortest path weight to determine the threshold
        try:
            shortest_path_weight = nx.dijkstra_path_length(G, source, target, weight=weight)
        except Exception as e:
            logger.warning(f"no path {e}")
            return []

        weight_threshold = shortest_path_weight * (1 + max_weight_increase)

        # Initialize the priority queue with the starting point
        paths_queue = [(0, [source], {source})]  # Each item: (total_weight, path, visited_nodes)

        # Store valid paths meeting the criteria
        valid_paths = []

        while paths_queue:
            current_weight, current_path, visited = heapq.heappop(paths_queue)
            last_node = current_path[-1]

            # Check if current path meets the target and weight criteria
            if last_node == target and current_weight <= weight_threshold:
                valid_paths.append((current_path, current_weight))

            # If cutoff is defined and the path length exceeds it, skip further extension
            if cutoff is not None and len(current_path) > cutoff:
                continue

            # Explore paths from the current node to its neighbors
            for neighbor in G[last_node]:
                if neighbor not in visited or neighbor == target:
                    new_weight = current_weight + G.edges[last_node, neighbor][weight]

                    # Continue only if the new path weight is within the threshold
                    if new_weight <= weight_threshold:
                        new_path = current_path + [neighbor]
                        new_visited = visited.copy()
                        new_visited.add(neighbor)

                        heapq.heappush(paths_queue, (new_weight, new_path, new_visited))
        # Cache the result before returning
        self._path_finding_cash[cache_key] = valid_paths
        return valid_paths

    def get_path(self, source_mirco_link, target_micro_link, start_measure, end_measure, cutoff=15) -> List[GraphRoute]:
        # todo: make cutoff should be input from query layer

        logger.trace(f"Routes finding between source: {source_mirco_link} {start_measure}, target: {target_micro_link} {end_measure}")
        output = []

        if source_mirco_link == target_micro_link:
            if source_mirco_link in self.micro_link_connections.get_keys():
                objects_on_route = [
                    _ for _ in self.micro_link_connections.get_by_puic(source_mirco_link) if _.measure >= start_measure and _.measure <= end_measure
                ]
                line_profile = cut_profile(self.micro_link_repo.get_by_puic(source_mirco_link).get_shapely(), start_measure, end_measure)
                return [GraphRoute([PathEdge(source_mirco_link, source_mirco_link)], line_profile, objects_on_route)]
            else:
                raise ValueError("MicroLink not in repo")

        # todo implement a own algorithm to find paths

        try:
            all_paths = list(nx.all_shortest_paths(self.g, source=source_mirco_link, target=target_micro_link, weight="weight"))  # , cutoff=cutoff
        except NetworkXNoPath:
            logger.warning(f"Found no routes between {source_mirco_link} and {target_micro_link}.")
            all_paths = []
        logger.info(f"Found {len(all_paths)} routes between {source_mirco_link} and {target_micro_link}.")

        tester = self._find_paths_without_revisiting_nodes(self.g, source_mirco_link, target_micro_link, weight="weight", max_weight_increase=0.1)
        all_paths = [_[0] for _ in tester]
        logger.info(f"(custom)) Found {len(all_paths)} routes between {source_mirco_link} and {target_micro_link}.")

        for path in all_paths:
            edges_in_path = self.get_edges_path(path)

            if self.has_cutback_in_path(edges_in_path):
                pass
                # logger.info(f"Route has cutback, not supported yet, will skip {edges_in_path}")
                # todo: cutback breaks below.... do we want to support this?
                # - objects on route: append them again in reversed order
                # - geometry: reverse cutback part

            else:
                logger.info(f"Processing route {edges_in_path}")

                objects_on_route = []  # this should be on route.... path edge is path.
                rail_con_geometry = []
                for idx, path_edge in enumerate(edges_in_path):
                    if idx == 0:
                        # first part of route, check measure what objects should be included.
                        object_in_route_segment = self.get_objects_on_route(path_edge.source, start_measure)
                        self.append_objects_on_route(path_edge.data.source_direction, objects_on_route, object_in_route_segment)

                        new_line = self.cut_geometry(path_edge, source_mirco_link, start_measure, target=False)
                        rail_con_geometry.append(new_line)

                        # all so can be the last part of route, check measure what objects should be included.
                        if len(edges_in_path) == 1:
                            object_in_route_segment = self.get_objects_on_route(path_edge.target, end_measure)
                            self.append_objects_on_route(path_edge.data.target_direction, objects_on_route, object_in_route_segment)

                            new_line = self.cut_geometry(path_edge, target_micro_link, end_measure, target=True)
                            rail_con_geometry.append(new_line)

                    elif len(edges_in_path) == idx + 1:
                        # last part of route, source all objects are included.
                        if path_edge.source in self.micro_link_connections.get_keys():
                            self.append_objects_on_route(
                                path_edge.data.source_direction, objects_on_route, self.micro_link_connections.get_by_puic(path_edge.source)
                            )
                        rail_con_geometry.append(self.micro_link_repo.get_by_puic(path_edge.source).get_shapely())

                        # target micro_link, check measure what objects should be included.
                        object_in_route_segment = self.get_objects_on_route(path_edge.target, end_measure)
                        self.append_objects_on_route(path_edge.data.target_direction, objects_on_route, object_in_route_segment)

                        # cut geometry
                        new_line = self.cut_geometry(path_edge, target_micro_link, end_measure, target=True)
                        rail_con_geometry.append(new_line)

                    else:
                        if path_edge.source in self.micro_link_connections.get_keys():
                            self.append_objects_on_route(
                                path_edge.data.source_direction, objects_on_route, self.micro_link_connections.get_by_puic(path_edge.source)
                            )
                        rail_con_geometry.append(self.micro_link_repo.get_by_puic(path_edge.source).get_shapely())

                output.append(GraphRoute(edges_in_path, linemerge(rail_con_geometry), objects_on_route))

        return output

    def get_paths_between_imx_objects(self, from_obj, to_obj) -> List[GraphRoute]:
        source_mirco_link = from_obj.rail_connection_infos.rail_infos[0].ref
        target_micro_link = to_obj.rail_connection_infos.rail_infos[0].ref
        start_measure = from_obj.rail_connection_infos.rail_infos[0].at_measure
        end_measure = to_obj.rail_connection_infos.rail_infos[0].at_measure

        paths = self.get_path(source_mirco_link, target_micro_link, start_measure, end_measure)
        return paths
