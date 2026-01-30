from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Host, Log, Play, Task
from .serializers import (
    HostSerializer,
    LogCreateSerializer,
    LogSerializer,
    TaskSerializer,
)
from .services.log_parser import LogParserService, determine_status


class LogViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet for viewing and creating logs.

    create: Upload and parse a new Ansible log
    retrieve: Get a specific log with all hosts and plays
    hosts: Get all hosts for a specific log
    """

    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return LogCreateSerializer
        return LogSerializer

    def get_queryset(self):
        return Log.objects.all().prefetch_related("hosts__plays")

    def create(self, request, *args, **kwargs):
        """
        Create a new log by uploading and parsing Ansible output.

        The log content is stored and parsed to extract hosts and plays.
        On success, returns the created log with all parsed data.
        On parsing failure, returns a 500 error with detailed information.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the log first to store raw content
        log = serializer.save()

        # Parse the log content
        parser_service = LogParserService()
        result = parser_service.parse(log.raw_content)

        if not result.success:
            # Delete the log on parsing failure
            log.delete()

            error_response = {
                "error": result.error or "Log parsing failed",
                "detail": result.detail or "Unknown parsing error",
                "raw_content_preview": log.raw_content[:500]
                if log.raw_content
                else None,
                "parser_type": result.parser_type,
            }

            if result.traceback_str:
                error_response["traceback"] = result.traceback_str

            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Create Host and Play entities from parsed data
        # Build a map of (hostname, play_name) -> Play for task association
        play_map = {}  # (hostname, play_name) -> Play instance

        for parsed_host in result.hosts:
            host = Host.objects.create(log=log, hostname=parsed_host.hostname)

            # Create a Play for each parsed play with line number and order
            for parsed_play in result.plays:
                play = Play.objects.create(
                    host=host,
                    name=parsed_play.name,
                    date=result.timestamp,
                    status=determine_status(parsed_host),
                    tasks_ok=parsed_host.ok,
                    tasks_changed=parsed_host.changed,
                    tasks_failed=parsed_host.failed,
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

        # Refresh log to include newly created hosts and plays
        log.refresh_from_db()

        # Return the full log with nested hosts and plays
        output_serializer = LogSerializer(log)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def hosts(self, request, pk=None):
        """
        List all hosts for a specific log.

        Returns:
            List of hosts with their plays for the specified log.
        """
        log = self.get_object()
        hosts = Host.objects.filter(log=log).prefetch_related("plays")
        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)


class PlayViewSet(viewsets.GenericViewSet):
    """
    ViewSet for Play-related operations.

    tasks: List all tasks for a specific play with optional status filtering
    """

    queryset = Play.objects.all()

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        """
        List all tasks for a specific play.

        Query Parameters:
            status (optional): Filter by task status
                (ok|changed|failed|skipping|unreachable|ignored|rescued)

        Returns:
            List of tasks ordered by execution order.
            Returns 400 if invalid status provided.
            Returns 404 if play UUID not found.
        """
        play = self.get_object()
        tasks = Task.objects.filter(play=play).order_by("order")

        status_filter = request.query_params.get("status")
        if status_filter:
            valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
            if status_filter not in valid_statuses:
                return Response(
                    {
                        "error": f"Invalid status '{status_filter}'",
                        "valid_statuses": valid_statuses,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Include both "failed" and "fatal" when filtering on "failed"
            if status_filter == "failed":
                tasks = tasks.filter(status__in=["failed", "fatal"])
            else:
                tasks = tasks.filter(status=status_filter)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
