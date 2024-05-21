from typing import List, TypeVar
from vital_ai_vitalsigns.query.result_list import ResultList
from vital_ai_vitalsigns.service.base_service import BaseService
from vital_ai_vitalsigns.service.graph.graph_service import VitalGraphService
from vital_ai_vitalsigns.service.vector.vector_service import VitalVectorService
from vital_ai_vitalsigns.service.vital_namespace import VitalNamespace
from vital_ai_vitalsigns.service.vital_service_status import VitalServiceStatus


G = TypeVar('G', bound='GraphObject')


class VitalService(BaseService):
    def __init__(self, graph_service: VitalGraphService = None, vector_service: VitalVectorService = None):
        self.graph_service = graph_service
        self.vector_service = vector_service

    # wrap combination of a vector store and graph store
    # or graph store individually or vector store individually

    # init namespace on or off
    # namespace primarily uses graph URI with vector namespace derived from this

    # graph store has separate graph for the namespaces

    def get_graph(self, graph_uri: str) -> VitalNamespace:

        name_graph = self.graph_service.get_graph(graph_uri)

        namespace = VitalNamespace()

        return namespace

    def list_graphs(self) -> List[VitalNamespace]:

        name_graph_list = self.graph_service.list_graphs()

        namespace_list = []

        return namespace_list

    # create graph
    # store name graph in vital service graph and in the graph itself
    # a graph needs to have some triples in it to exist

    def check_create_graph(self, graph_uri: str) -> bool:

        return self.graph_service.check_create_graph(graph_uri)

    def create_graph(self, graph_uri: str) -> bool:
        return self.graph_service.create_graph(graph_uri)

    # delete graph
    # delete graph itself plus record in vital service graph

    def delete_graph(self, graph_uri: str) -> bool:
        return self.graph_service.delete_graph(graph_uri)

    # purge graph (delete all but name graph)

    def purge_graph(self, graph_uri: str) -> bool:
        return self.graph_service.purge_graph(graph_uri)

    def get_graph_all_objects(self, graph_uri: str, limit=100, offset=0) -> ResultList:
        return self.graph_service.get_graph_all_objects(graph_uri, limit=limit, ffset=offset)

    # insert object into graph (scoped to vital service graph uri, which must exist)

    # insert object list into graph (scoped to vital service graph uri, which must exist)

    def insert_object(self, graph_uri: str, graph_object: G) -> VitalServiceStatus:

        graph_status = self.graph_service.insert_object(graph_uri, graph_object)

        service_status = VitalServiceStatus(graph_status.get_status(), graph_status.get_message())

        service_status.set_changes(graph_status.get_changes())

        return service_status

    def insert_object_list(self, graph_uri: str, graph_object_list: List[G], vital_managed=True) -> VitalServiceStatus:

        graph_status = self.graph_service.insert_object_list(graph_uri, graph_object_list)

        service_status = VitalServiceStatus(graph_status.get_status(), graph_status.get_message())

        service_status.set_changes(graph_status.get_changes())

        return service_status

    # update object into graph (scoped to vital service graph uri, which must exist)
    # delete old, replace with new

    # update object list into graph (scoped to vital service graph uri, which must exist)
    # delete old, replace with new

    def update_object(self, graph_object: G) -> VitalServiceStatus:

        graph_status = self.graph_service.update_object(graph_object)

        service_status = VitalServiceStatus(graph_status.get_status(), graph_status.get_message())

        service_status.set_changes(graph_status.get_changes())

        return service_status

    def update_object_list(self, graph_object_list: List[G]) -> VitalServiceStatus:

        graph_status = self.graph_service.update_object_list(graph_object_list)

        service_status = VitalServiceStatus(graph_status.get_status(), graph_status.get_message())

        service_status.set_changes(graph_status.get_changes())

        return service_status

    def get_object(self, object_uri: str) -> G:

        graph_object = self.graph_service.get_object(object_uri)

        return graph_object

    def get_object_list(self, object_uri_list: List[str]) -> ResultList:

        return self.graph_service.get_object_list(object_uri_list)

    def delete_object(self, object_uri: str) -> VitalServiceStatus:

        graph_status = self.graph_service.delete_object(object_uri)

        service_status = VitalServiceStatus(graph_status.get_status(), graph_status.get_message())

        service_status.set_changes(graph_status.get_changes())

        return service_status

    def delete_object_list(self, object_uri_list: List[str]) -> VitalServiceStatus:

        graph_status = self.graph_service.delete_object(object_uri_list)

        service_status = VitalServiceStatus(graph_status.get_status(), graph_status.get_message())

        service_status.set_changes(graph_status.get_changes())

        return service_status

    # filter graph

    def filter_query(self, sparql_query: str, uri_binding='uri', resolve_objects=True) -> ResultList:

        return self.graph_service.filter_query(sparql_query, uri_binding=uri_binding, resolve_objects=resolve_objects)

    # query graph

    def query(self, sparql_query: str, uri_binding='uri', resolve_objects=True) -> ResultList:

        return self.graph_service.query(sparql_query, uri_binding=uri_binding, resolve_objects=resolve_objects)

