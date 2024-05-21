from utils.config_utils import ConfigUtils
from vital_ai_vitalsigns.service.graph.virtuoso_service import VirtuosoGraphService
from vital_ai_vitalsigns.service.vital_service import VitalService


def main():
    print('Hello World')

    config = ConfigUtils.load_config()

    virtuoso_username = config['graph_database']['virtuoso_username']
    virtuoso_password = config['graph_database']['virtuoso_password']
    virtuoso_endpoint = config['graph_database']['virtuoso_endpoint']

    virtuoso_graph_service = VirtuosoGraphService(
        username=virtuoso_username,
        password=virtuoso_password,
        endpoint=virtuoso_endpoint
    )

    graph_list = virtuoso_graph_service.get_graph_list()

    for g in graph_list:
        print(g.get_graph_uri())

    vital_service = VitalService(graph_service=virtuoso_graph_service)


if __name__ == "__main__":
    main()
