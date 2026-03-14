"""Service for creating Log/Host/Play/Task database records from parsed results."""

from ..models import Host, Play, Task
from .log_parser import (
    ParseResult,
    compute_play_host_counts,
    determine_play_status,
)


def create_log_entities(log, result: ParseResult) -> None:
    """
    Create Host, Play, and Task records from a ParseResult.

    Per-play task counts are computed from individual parsed tasks,
    not from the PLAY RECAP aggregate (which is global per host).

    Args:
        log: The Log instance (already saved) to attach entities to
        result: The parsed log result containing hosts, plays, and tasks
    """
    # Pre-compute per-play, per-host task counts from individual tasks
    play_host_counts = compute_play_host_counts(result.tasks)

    # Build play_map for task association
    play_map = {}  # (hostname, play_name) -> Play instance

    for parsed_host in result.hosts:
        host = Host.objects.create(log=log, hostname=parsed_host.hostname)

        for parsed_play in result.plays:
            counts = play_host_counts.get(
                (parsed_play.name, parsed_host.hostname),
                {"ok": 0, "changed": 0, "failed": 0},
            )

            play = Play.objects.create(
                host=host,
                name=parsed_play.name,
                date=result.timestamp,
                status=determine_play_status(
                    counts["ok"], counts["changed"], counts["failed"]
                ),
                tasks_ok=counts["ok"],
                tasks_changed=counts["changed"],
                tasks_failed=counts["failed"],
                line_number=parsed_play.line_number,
                order=parsed_play.order,
            )
            play_map[(parsed_host.hostname, parsed_play.name)] = play

    # Create Task entities from parsed tasks
    for parsed_task in result.tasks:
        for task_result in parsed_task.results:
            play = play_map.get((task_result.hostname, parsed_task.play_name))
            if play:
                Task.objects.create(
                    play=play,
                    name=parsed_task.name,
                    order=parsed_task.order,
                    line_number=parsed_task.line_number,
                    status=task_result.status,
                    failure_message=task_result.message,
                )
