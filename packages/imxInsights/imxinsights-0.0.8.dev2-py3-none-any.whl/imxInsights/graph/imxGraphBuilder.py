from typing import Dict, List, Optional

import networkx as nx

from imxInsights.graph.imxGraph import ImxGraph
from imxInsights.graph.imxGraphJunction import ImxGraphJunction
from imxInsights.graph.imxGraphModels import (
    DirectionEnum,
    GraphMicroLink,
    ImxMicroLink,
    ImxMicroNode,
    ImxRailConnection,
    MicroLinkConnection,
    MicroLinkConnectionRepo,
    MicroLinkRepo,
    MicroNodeRepo,
    RailConnectionRepo,
)
from imxInsights.graph.imxGraphSituationProtocol import ImxSituationRepoMinimalProtocol


class ImxGraphBuilder:
    """Builds a directed graph (DiGraph) from IMX insight data.

    Attributes:
        imx_situation (SituationRepo): The repository containing situation data.
        g (nx.DiGraph): The directed graph object being built.
        micro_link_repo (MicroLinkRepo): Repository of micro links.
        micro_node_repo (MicroNodeRepo): Repository of micro nodes.
        rail_connections_repo (RailConnectionRepo): Repository of rail connections.
        micro_link_connections (MicroLinkConnectionRepo): Micro link connections extracted from the data.
    """

    def __init__(self, imx_situation: ImxSituationRepoMinimalProtocol):
        """Initializes the GraphBuilder with a situation repository.

        Args:
            imx_situation (SituationRepo): The repository containing situation data.
        """
        self.imx_situation = imx_situation
        self.g = nx.DiGraph()
        self.micro_link_repo = self._get_micro_link_repo()
        self.micro_node_repo = self._get_micro_node_repo()
        self.rail_connections_repo = self._get_rail_connection_repo()
        self.micro_link_connections = self._get_micro_link_connections_repo()

    def _get_micro_link_repo(self) -> MicroLinkRepo:
        """Creates a micro link repository from the situation data.

        Returns:
            MicroLinkRepo: The micro link repository.
        """
        return MicroLinkRepo([ImxMicroLink(_) for _ in self.imx_situation.get_by_types(["MicroLink"])])

    def _get_micro_node_repo(self) -> MicroNodeRepo:
        """Creates a micro node repository from the situation data.

        Returns:
            MicroNodeRepo: The micro node repository.
        """
        return MicroNodeRepo([ImxMicroNode(_) for _ in self.imx_situation.get_by_types(["MicroNode"])])

    def _get_rail_connection_repo(self) -> RailConnectionRepo:
        """Creates a rail connection repository from the situation data.

        Returns:
            RailConnectionRepo: The rail connection repository.
        """
        return RailConnectionRepo([ImxRailConnection(_) for _ in self.imx_situation.get_by_types(["RailConnection"])])

    def _get_linked_micro_links(self, input_micro_link: ImxMicroLink, node_type: str) -> Dict[str, GraphMicroLink]:
        """Finds micro links connected to a given micro link through 'from_node' or 'to_node'.

        This method processes the specified 'from_node' or 'to_node' of an input micro link to find all other micro links that
        are connected through jumpers, which are essentially connections between nodes. It considers the passages refs
        and the transferability of jumpers, their directionality, and the presence of passages to establish connections.

        Args:
            input_micro_link (ImxMicroLink): The micro link to find connections for.
            node_type (str): The node type to consider for connections ('from_node' or 'to_node').

        Returns:
            Dict[str, GraphMicroLink]: A dictionary mapping the input micro link's PUIC to a list of connected GraphMicroLinks.
        """
        output = []  # Initialize an empty list to store the connected GraphMicroLinks.

        # Get the specified 'from_node' or 'to_node' of the input micro link.
        to_or_from_node = getattr(input_micro_link, node_type)

        # Retrieve the micro node object using the reference from the 'to_or_from_node'.
        micro_node = self.micro_node_repo.get_by_puic(to_or_from_node.ref)
        imx_implementation = self.imx_situation.get_by_puic(to_or_from_node.ref)
        graph_junction = ImxGraphJunction.from_element(imx_implementation.element)

        # Iterate through each jumper (connection) of the micro node.
        for jumper in micro_node.jumpers:
            # Skip the jumper if it is not traversable.
            if not jumper.is_traversible:
                continue

            # Filter the passages that are present and not present in the input micro link and in the jumper.
            passages_from_input_micro_link = [_ for _ in jumper.passage_refs if _ in input_micro_link.passage_refs]
            passages_from_other_micro_link = [_ for _ in jumper.passage_refs if _ not in input_micro_link.passage_refs]

            # Check if there are any passages from the input micro link present in the jumper.
            if passages_from_input_micro_link:
                # Iterate through all micro links in the repository to find potential connections.
                for micro_link in self.micro_link_repo.micro_links:
                    for passage_ref in micro_link.passage_refs:
                        # If a passage reference matches and it's not the input micro link, we have a connection.
                        if passage_ref in passages_from_other_micro_link and micro_link != input_micro_link:
                            # Skip if the jumper is not two-way and the connection does not match the current node processing logic.
                            if not jumper.is_two_way:
                                if node_type == "to_node" and micro_link.from_node.ref == micro_node.junctionRef:
                                    continue
                                if node_type == "from_node" and micro_link.to_node.ref == micro_node.junctionRef:
                                    continue

                            # Determine the direction of the connection based on the node references.
                            to_direction = DirectionEnum.DOWNSTREAM if micro_link.from_node.ref == to_or_from_node.ref else DirectionEnum.UPSTREAM

                            # Add the connected GraphMicroLink to the output list.
                            output.append(
                                GraphMicroLink(
                                    imx_micro_link=micro_link,
                                    from_direction=DirectionEnum.UPSTREAM if node_type == "from_node" else DirectionEnum.DOWNSTREAM,
                                    to_direction=to_direction,
                                    junction=micro_node,
                                    graph_junction=graph_junction,
                                    jumper=jumper,
                                )
                            )

        # Return a dictionary with the input micro link's PUIC as the key and the list of connected GraphMicroLinks as the value.
        return {input_micro_link.puic: output}

    def _get_micro_link_graph_mapping(self) -> Dict[str, List[GraphMicroLink]]:
        """Generates a mapping of micro links to their connected GraphMicroLinks in the graph.

        This method iterates over all micro links in the repository, obtaining connected micro links for each
        by processing both 'from_node' and 'to_node'. It combines these connections to form a comprehensive mapping
        that represents all possible micro link connections within the graph.

        Returns:
            Dict[str, List[GraphMicroLink]]: A dictionary mapping each micro link's PUIC to a list of connected GraphMicroLinks.
        """
        mapping_from = {}  # Initialize a dictionary to store connections originating from the 'from_node'.
        mapping_to = {}  # Initialize a dictionary to store connections originating from the 'to_node'.

        # Iterate over all micro links in the repository.
        for micro_link in self.micro_link_repo.micro_links:
            # Update the 'mapping_from' dictionary with connections found from the 'from_node' and 'from_node'
            mapping_from.update(self._get_linked_micro_links(micro_link, "from_node"))
            mapping_to.update(self._get_linked_micro_links(micro_link, "to_node"))

        # Combine the 'from' and 'to' mappings to create a comprehensive mapping.
        # This step merges connections from both directions for each micro link.
        common_dict = {key: mapping_from[key] + mapping_to[key] for key in mapping_from if key in mapping_to}

        # Return the comprehensive mapping of micro link connections.
        return common_dict

    def _get_micro_link_connections_repo(self, object_types: Optional[List[str]] = None) -> MicroLinkConnectionRepo:
        output: Dict[str, List[MicroLinkConnection]] = {}
        imx_objects = self.imx_situation.get_by_types(object_types) if object_types else self.imx_situation.get_all()

        for imx_object in imx_objects:
            if imx_object.rail_connection_infos:
                for rail_con_info in imx_object.rail_connection_infos.rail_infos:
                    # Use the new method to simplify creation of MicroLinkConnection objects.
                    connections = MicroLinkConnection.create_from_rail_info(rail_con_info, imx_object)
                    if rail_con_info.ref in output:
                        output[rail_con_info.ref].extend(connections)
                    else:
                        output[rail_con_info.ref] = connections

        # Sort the connections by measure for each reference key.
        for key, connections in output.items():
            output[key] = sorted(connections, key=lambda x: x.measure)

        return MicroLinkConnectionRepo(output)

    def build_graph(self) -> ImxGraph:
        """Builds the graph from the repositories."""
        [self.g.add_node(_.puic, pos=_.get_centroid_as_xy()) for _ in self.micro_link_repo.micro_links]
        mapping = self._get_micro_link_graph_mapping()

        for key, value in mapping.items():
            from_micro_link = self.micro_link_repo.get_by_puic(key)
            from_geometry_weight = from_micro_link.get_shapely().length / 2

            for item in value:
                to_geometry_weight = item.imx_micro_link.get_shapely().length / 2
                self.g.add_edge(
                    key,
                    item.imx_micro_link.puic,
                    weight=from_geometry_weight + to_geometry_weight,
                    current_direction=item.from_direction.name,
                    junction=item.junction.junctionRef,
                    next_direction=item.to_direction.name,
                    graph_junction=item.graph_junction,
                    jumper=item.jumper,
                )

        return ImxGraph(
            self.g, self.imx_situation, self.micro_link_repo, self.micro_node_repo, self.rail_connections_repo, self.micro_link_connections
        )
