from backend.workflow.graph import build_memory_graph


def test_memory_graph_can_be_built():
    graph = build_memory_graph()

    assert graph is not None
