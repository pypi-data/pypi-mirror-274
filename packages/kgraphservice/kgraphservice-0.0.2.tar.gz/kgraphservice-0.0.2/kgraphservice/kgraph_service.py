from typing import List, TypeVar, Type

from ai_haley_kg_domain.model.KGInteraction import KGInteraction
from ai_haley_kg_domain.model.KGNode import KGNode
from vital_ai_vitalsigns.query.result_list import ResultList
from vital_ai_vitalsigns.service.vital_namespace import VitalNamespace
from vital_ai_vitalsigns.service.vital_service import VitalService
from vital_ai_vitalsigns.service.vital_service_status import VitalServiceStatus


G = TypeVar('G', bound='GraphObject')
KGN = TypeVar('KGN', bound='KGNode')


class KGraphService:
    def __init__(self, vital_service: VitalService):
        self.vital_service = vital_service

    def get_interaction_list(self, account_uri: str, limit=100, offset=0) -> ResultList:
        pass

    def get_interaction_graph(self, interaction: KGInteraction) -> ResultList:
        pass

    def get_interaction_frames(self, interaction: KGInteraction) -> ResultList:
        pass

    def get_interaction_nodes(self, interaction: KGInteraction, kgnode_type: Type[KGN]) -> ResultList:
        pass

    def get_graph(self, graph_uri: str) -> VitalNamespace:
        return self.vital_service.get_graph(graph_uri)

    def list_graphs(self) -> List[VitalNamespace]:
        return self.vital_service.list_graphs()

    def check_create_graph(self, graph_uri: str) -> bool:
        return self.vital_service.check_create_graph(graph_uri)

    def create_graph(self, graph_uri: str) -> bool:
        return self.vital_service.create_graph(graph_uri)

    def delete_graph(self, graph_uri: str) -> bool:
        return self.vital_service.delete_graph(graph_uri)

    def purge_graph(self, graph_uri: str) -> bool:
        return self.vital_service.purge_graph(graph_uri)

    def get_graph_all_objects(self, graph_uri: str, limit=100, offset=0) -> ResultList:
        return self.vital_service.get_graph_all_objects(graph_uri, limit=limit, offset=offset)

    def insert_object(self, graph_uri: str, graph_object: G) -> VitalServiceStatus:
        return self.vital_service.insert_object(graph_uri, graph_object)

    def insert_object_list(self, graph_uri: str, graph_object_list: List[G]) -> VitalServiceStatus:
        return self.vital_service.insert_object_list(graph_uri, graph_object_list)

    def update_object(self, graph_object: G) -> VitalServiceStatus:
        return self.vital_service.update_object(graph_object)

    def update_object_list(self, graph_object_list: List[G]) -> VitalServiceStatus:
        return self.vital_service.update_object_list(graph_object_list)

    def get_object(self, object_uri: str) -> G:
        return self.vital_service.get_object(object_uri)

    def get_object_list(self, object_uri_list: List[str]) -> ResultList:
        return self.vital_service.get_object_list(object_uri_list)

    def delete_object(self, object_uri: str) -> VitalServiceStatus:
        return self.vital_service.delete_object(object_uri)

    def delete_object_list(self, object_uri_list: List[str]) -> VitalServiceStatus:
        return self.vital_service.delete_object_list(object_uri_list)

    def filter_query(self, sparql_query: str) -> ResultList:
        return self.vital_service.filter_query(sparql_query)

    def query(self, sparql_query: str) -> ResultList:
        return self.vital_service.query(sparql_query)



