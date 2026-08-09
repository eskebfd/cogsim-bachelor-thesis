from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from backend.workflow.state import CogSimState
from backend.workflow.nodes.scenario_nodes import (
    extract_dimension_context,
    extract_dimensions,
    extract_environment_dimension_signals,
    extract_interface_dimension_signals,
    extract_task_dimension_signals,
    merge_dimension_signals,
)
from backend.workflow.nodes.model_nodes import (
    construct_base_models,
    construct_task_model,
    construct_interface_model,
    construct_environment_model,
)
from backend.workflow.nodes.planning_nodes import (
    construct_computed_parameters,
)
from backend.workflow.nodes.simulation_nodes import (
    initialize_simulation,
    run_simulation_step,
    log_state,
    check_finished,
)
from backend.workflow.nodes.result_nodes import (
    generate_results,
    prepare_visualization,
)
from backend.workflow.nodes.review_nodes import prepare_revision_instruction_node
from backend.workflow.routing import (
    update_state_router,
    route_after_revision_instruction,
    route_after_task_model,
    route_after_interface_model,
)


memory = MemorySaver()


def build_memory_graph():
    builder = StateGraph(CogSimState)

    builder.add_node("extract_dimensions", extract_dimensions)
    builder.add_node("extract_dimension_context", extract_dimension_context)
    builder.add_node(
        "extract_task_dimension_signals",
        extract_task_dimension_signals,
    )
    builder.add_node(
        "extract_interface_dimension_signals",
        extract_interface_dimension_signals,
    )
    builder.add_node(
        "extract_environment_dimension_signals",
        extract_environment_dimension_signals,
    )
    builder.add_node("merge_dimension_signals", merge_dimension_signals)
    builder.add_node("construct_base_models", construct_base_models)
    builder.add_node("construct_task_model", construct_task_model)
    builder.add_node("construct_interface_model", construct_interface_model)
    builder.add_node("construct_environment_model", construct_environment_model)
    builder.add_node("construct_computed_parameters", construct_computed_parameters)
    builder.add_node("initialize_simulation", initialize_simulation)
    builder.add_node("run_simulation_step", run_simulation_step)
    builder.add_node("log_state", log_state)
    builder.add_node("generate_results", generate_results)
    builder.add_node("prepare_visualization", prepare_visualization)
    builder.add_node(
        "prepare_revision_instruction",
        prepare_revision_instruction_node,
    )

    builder.set_conditional_entry_point(
        update_state_router,
        {
            "extract_dimensions": "extract_dimensions",
            "extract_dimension_context": "extract_dimension_context",
            "construct_base_models": "construct_base_models",
            "construct_task_model": "construct_task_model",
            "construct_interface_model": "construct_interface_model",
            "construct_environment_model": "construct_environment_model",
            "construct_computed_parameters": "construct_computed_parameters",
            "initialize_simulation": "initialize_simulation",
            "prepare_revision_instruction": "prepare_revision_instruction",
            "finished": END,
        },
    )

    builder.add_edge("extract_dimensions", END)
    builder.add_edge("extract_dimension_context", "extract_task_dimension_signals")
    builder.add_edge(
        "extract_dimension_context",
        "extract_interface_dimension_signals",
    )
    builder.add_edge(
        "extract_dimension_context",
        "extract_environment_dimension_signals",
    )
    builder.add_edge(
        [
            "extract_task_dimension_signals",
            "extract_interface_dimension_signals",
            "extract_environment_dimension_signals",
        ],
        "merge_dimension_signals",
    )
    builder.add_edge("merge_dimension_signals", END)
    builder.add_edge("construct_base_models", END)
    builder.add_edge("construct_environment_model", END)
    builder.add_edge("construct_computed_parameters", END)

    builder.add_conditional_edges(
        "prepare_revision_instruction",
        route_after_revision_instruction,
        {
            "construct_task_model": "construct_task_model",
            "construct_base_models": "construct_base_models",
            "construct_interface_model": "construct_interface_model",
            "construct_environment_model": "construct_environment_model",
            "finished": END,
        },
    )

    builder.add_conditional_edges(
        "construct_task_model",
        route_after_task_model,
        {
            "construct_interface_model": "construct_interface_model",
            "finished": END,
        },
    )

    builder.add_conditional_edges(
        "construct_interface_model",
        route_after_interface_model,
        {
            "construct_environment_model": "construct_environment_model",
            "finished": END,
        },
    )

    builder.add_edge("initialize_simulation", "run_simulation_step")
    builder.add_edge("run_simulation_step", "log_state")

    builder.add_conditional_edges(
        "log_state",
        check_finished,
        {
            "run_simulation_step": "run_simulation_step",
            "generate_results": "generate_results",
        },
    )

    builder.add_edge("generate_results", "prepare_visualization")
    builder.add_edge("prepare_visualization", END)

    return builder.compile(checkpointer=memory)
