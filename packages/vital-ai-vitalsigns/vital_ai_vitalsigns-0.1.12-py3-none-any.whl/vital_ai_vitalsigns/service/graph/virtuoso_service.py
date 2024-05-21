from typing import List, TypeVar
from SPARQLWrapper import SPARQLWrapper, DIGEST, JSON, POST

from vital_ai_vitalsigns.query.result_list import ResultList
from vital_ai_vitalsigns.service.graph.graph_service import VitalGraphService
from vital_ai_vitalsigns.service.graph.name_graph import VitalNameGraph
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.service.graph.vital_graph_status import VitalGraphStatus

G = TypeVar('G', bound='GraphObject')


class VirtuosoGraphService(VitalGraphService):

    def __init__(self, username: str = None, password: str = None, endpoint: str = None):
        self.username = username
        self.password = password
        self.endpoint = endpoint.rstrip('/')
        self.sparql_auth_endpoint = f"{self.endpoint}/sparql-auth"
        self.graph_crud_auth_endpoint = f"{self.endpoint}/sparql-graph-crud-auth"
        super().__init__()

    def list_graphs(self, vital_managed=True) -> List[VitalNameGraph]:
        sparql = SPARQLWrapper(self.sparql_auth_endpoint)
        sparql.setCredentials(self.username, self.password)
        sparql.setHTTPAuth(DIGEST)

        query = """
            SELECT DISTINCT ?g WHERE { GRAPH ?g {?s ?p ?o} } ORDER BY ?g
        """

        sparql.setQuery(query)
        sparql.setMethod(POST)
        sparql.setReturnFormat(JSON)

        results = sparql.query().convert()

        graph_uris = []
        for result in results["results"]["bindings"]:
            graph_uri = result["g"]["value"]
            graph_uris.append(graph_uri)
            print(graph_uri)

        name_graph_list = []

        for g_uri in graph_uris:
            name_graph = VitalNameGraph(g_uri)
            name_graph_list.append(name_graph)

        return name_graph_list

    def get_graph(self, graph_uri: str, vital_managed=True) -> VitalNameGraph:
        pass

    # create graph
    # store name graph in vital service graph and in the graph itself
    # a graph needs to have some triples in it to exist

    def check_create_graph(self, graph_uri: str, vital_managed=True) -> bool:
        pass

    def create_graph(self, graph_uri: str, vital_managed=True) -> bool:
        pass

    # delete graph
    # delete graph itself plus record in vital service graph

    def delete_graph(self, graph_uri: str, vital_managed=True) -> bool:
        pass

    # purge graph (delete all but name graph)

    def purge_graph(self, graph_uri: str, vital_managed=True) -> bool:
        pass

    def get_graph_all_objects(self, graph_uri: str, limit=100, offset=0, vital_managed=True) -> ResultList:
        pass

    # insert object into graph (scoped to vital service graph uri, which must exist)

    # insert object list into graph (scoped to vital service graph uri, which must exist)

    def insert_object(self, graph_uri: str, graph_object: G, vital_managed=True) -> VitalGraphStatus:
        pass

    def insert_object_list(self, graph_uri: str, graph_object_list: List[G], vital_managed=True) -> VitalGraphStatus:
        pass

    # update object into graph (scoped to vital service graph uri, which must exist)
    # delete old, replace with new

    # update object list into graph (scoped to vital service graph uri, which must exist)
    # delete old, replace with new

    def update_object(self, graph_object: G, graph_uri=None, graph_uri_list=None,
                      vital_managed=True) -> VitalGraphStatus:
        pass

    def update_object_list(self, graph_object_list: List[G], graph_uri=None, graph_uri_list=None,
                           vital_managed=True) -> VitalGraphStatus:
        pass

    # get object (scoped to all vital service graphs)

    # get object (scoped to specific graph, or graph list)

    # get objects by uri list (scoped to all vital service graphs)

    # get objects by uri list (scoped to specific graph, or graph list)

    def get_object(self, object_uri: str, graph_uri=None, graph_uri_list=None, vital_managed=True) -> G:
        pass

    def get_object_list(self, object_uri_list: List[str], graph_uri=None, graph_uri_list=None,
                        vital_managed=True) -> ResultList:
        pass

    # delete uri (scoped to all vital service graphs)

    # delete uri list (scoped to all vital service graphs)

    # delete uri (scoped to graph or graph list)

    # delete uri list (scoped to graph or graph list)

    def delete_object(self, object_uri: str, graph_uri=None, graph_uri_list=None,
                      vital_managed=True) -> VitalGraphStatus:
        pass

    def delete_object_list(self, object_uri_list: List[str], graph_uri=None, graph_uri_list=None,
                           vital_managed=True) -> VitalGraphStatus:
        pass

    # filter graph

    def filter_query(self, sparql_query: str, uri_binding='uri', resolve_objects=True,
                     vital_managed=True) -> ResultList:
        pass

    # query graph

    def query(self, sparql_query: str, uri_binding='uri', resolve_objects=True, vital_managed=True) -> ResultList:
        pass

"""

use this style for crud operations:
except use rdf ntriples or nquads instead of turtle
probably n-triples since the graph uri is determined
application/n-triples
this would be for incremental updates rather than bulk
updates to multiple graphs would be split over N requests

curl -X PUT   -H "Content-Type: text/turtle"   --digest -u "user:password"   --data-binary @update.ttl   http://localhost:8890/sparql-graph-crud-auth?graph-uri=http://example.org/test3

"""
