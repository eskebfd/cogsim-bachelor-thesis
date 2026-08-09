from backend.domains.simulation.results import (
    task_step_display_name,
    task_success_score_value,
)


def build_timeline_visualization(timeline: list[dict]) -> dict:
    visualization_data = [
        {
            "timestamp": item["timestamp"],
            "timestamp_seconds": item["timestamp_seconds"],
            "task_step": task_step_display_name(item["current_task_step"]),
            "task_progress": item.get("task_progress", 0),
            "base_step_duration": item.get("base_step_duration", 0),
            "actual_step_duration": item.get("actual_step_duration", 0),
            "reading_speed": item["reading_speed"],
            "attention": item["attention"],
            "fatigue": item["fatigue"],
            "cognitive_load": item["cognitive_load"],
            "error_risk": item["error_risk"],
            "task_success_score": task_success_score_value(item),
            "completion_efficiency": item["completion_efficiency"],
        }
        for item in timeline
    ]

    return {
        "type": "time_discrete_timeline",
        "data": visualization_data,
    }
