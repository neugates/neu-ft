from data.error_codes import *

def add_nodes(node_data_templates, add_node, config):
    for node_data in node_data_templates:
        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")