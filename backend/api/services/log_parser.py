"""Service module for parsing Ansible logs using ansible-output-parser."""

import re
import tempfile
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ansible_parser.logs import Logs
from ansible_parser.play import Play


@dataclass
class ParsedHost:
    """Represents parsed host data from Ansible output."""

    hostname: str
    ok: int = 0
    changed: int = 0
    failed: int = 0
    unreachable: int = 0
    skipped: int = 0
    rescued: int = 0
    ignored: int = 0


@dataclass
class ParsedPlay:
    """Represents parsed play data from Ansible output."""

    name: str
    order: int
    line_number: Optional[int] = None


@dataclass
class ParsedTaskResult:
    """Represents a single task execution result on a host."""

    hostname: str
    status: str  # ok, changed, failed, fatal, skipping, unreachable, ignored, rescued
    message: Optional[str] = None


@dataclass
class ParsedTask:
    """Represents a parsed task from Ansible output."""

    name: str
    order: int
    play_name: str
    line_number: Optional[int] = None
    results: list[ParsedTaskResult] = field(default_factory=list)


@dataclass
class ParseResult:
    """Result of parsing an Ansible log."""

    success: bool
    hosts: list[ParsedHost] = field(default_factory=list)
    plays: list[ParsedPlay] = field(default_factory=list)
    tasks: list[ParsedTask] = field(default_factory=list)
    timestamp: Optional[datetime] = None
    error: Optional[str] = None
    detail: Optional[str] = None
    parser_type: Optional[str] = None
    traceback_str: Optional[str] = None

    @property
    def play_names(self) -> list[str]:
        """Return list of play names for backwards compatibility."""
        return [p.name for p in self.plays]


class LogParserService:
    """Service to parse Ansible logs using ansible-output-parser."""

    # Pattern to detect timestamped log format: "YYYY-MM-DD HH:MM:SS,mmm | "
    TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} \|")
    # Pattern to match PLAY lines and extract play name
    PLAY_PATTERN = re.compile(r"PLAY \[([^\]]+)\]")
    # Pattern to match TASK lines and extract task name
    TASK_PATTERN = re.compile(r"TASK \[([^\]]+)\]")

    def parse(self, raw_content: str) -> ParseResult:
        """
        Auto-detect format and parse log content.

        Args:
            raw_content: Raw Ansible log content (stdout or timestamped log)

        Returns:
            ParseResult with hosts/plays data or error details
        """
        if not raw_content or not raw_content.strip():
            return ParseResult(
                success=False,
                error="Empty log content",
                detail="The provided log content is empty or contains only whitespace",
            )

        # Normalize line endings (CRLF -> LF) for consistent parsing
        # Browser textareas may submit with Windows-style line endings
        raw_content = raw_content.replace("\r\n", "\n").replace("\r", "\n")

        parser_type = self._detect_format(raw_content)

        try:
            if parser_type == "logs":
                return self._parse_log_file(raw_content)
            else:
                return self._parse_play_output(raw_content)
        except Exception as e:
            return ParseResult(
                success=False,
                error="Log parsing failed",
                detail=str(e),
                parser_type=parser_type,
                traceback_str=traceback.format_exc(),
            )

    def _detect_format(self, content: str) -> str:
        """
        Detect if content is raw stdout or timestamped log format.

        Args:
            content: Raw log content

        Returns:
            'logs' for timestamped format, 'play' for raw stdout
        """
        first_line = content.strip().split("\n")[0] if content.strip() else ""
        if self.TIMESTAMP_PATTERN.match(first_line):
            return "logs"
        return "play"

    def _parse_play_output(self, content: str) -> ParseResult:
        """
        Parse using ansible_parser.play.Play class for raw stdout format.

        Args:
            content: Raw Ansible playbook stdout output

        Returns:
            ParseResult with extracted hosts, plays, and tasks
        """
        parser = Play(play_output=content)

        # Extract play names from parser
        play_names = list(parser.plays().keys())

        # Find line numbers for each play
        plays = self._extract_plays_with_line_numbers(content, play_names)

        # Extract hosts from recap
        hosts = self._extract_hosts_from_recap(parser)

        # Extract tasks from plays
        tasks = self._extract_tasks_from_plays(parser, content)

        if not hosts:
            return ParseResult(
                success=False,
                error="No hosts found in log",
                detail="The parser could not find any PLAY RECAP section",
                parser_type="play",
            )

        return ParseResult(
            success=True,
            hosts=hosts,
            plays=plays,
            tasks=tasks,
            timestamp=None,  # Raw stdout doesn't have timestamps
            parser_type="play",
        )

    def _parse_log_file(self, content: str) -> ParseResult:
        """
        Parse using ansible_parser.logs.Logs class for timestamped log format.

        Args:
            content: Timestamped log file content

        Returns:
            ParseResult with extracted hosts, plays, and tasks
        """
        # Logs class requires a file path, so we write to a temp file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".log", delete=False
        ) as tmp_file:
            tmp_file.write(content)
            tmp_file.flush()
            tmp_path = tmp_file.name

        try:
            log_parser = Logs(log_file=tmp_path)

            # Collect all hosts, plays, and tasks from all parsed plays
            all_hosts: dict[str, ParsedHost] = {}
            all_play_names: list[str] = []
            all_tasks: list[ParsedTask] = []

            for play in log_parser.plays:
                # Get play names
                play_names = list(play.plays().keys())
                for name in play_names:
                    if name not in all_play_names:
                        all_play_names.append(name)

                # Get hosts from recap
                hosts = self._extract_hosts_from_recap(play)
                for host in hosts:
                    if host.hostname in all_hosts:
                        # Aggregate counts
                        existing = all_hosts[host.hostname]
                        existing.ok += host.ok
                        existing.changed += host.changed
                        existing.failed += host.failed
                        existing.unreachable += host.unreachable
                        existing.skipped += host.skipped
                        existing.rescued += host.rescued
                        existing.ignored += host.ignored
                    else:
                        all_hosts[host.hostname] = host

                # Extract tasks from this play
                tasks = self._extract_tasks_from_plays(play, content)
                all_tasks.extend(tasks)

            if not all_hosts:
                return ParseResult(
                    success=False,
                    error="No hosts found in log",
                    detail="The parser could not find any PLAY RECAP section",
                    parser_type="logs",
                )

            # Find line numbers for each play
            plays = self._extract_plays_with_line_numbers(content, all_play_names)

            return ParseResult(
                success=True,
                hosts=list(all_hosts.values()),
                plays=plays,
                tasks=all_tasks,
                timestamp=log_parser.last_processed_time,
                parser_type="logs",
            )

        finally:
            # Clean up temp file
            import os

            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    def _extract_plays_with_line_numbers(
        self, content: str, play_names: list[str]
    ) -> list[ParsedPlay]:
        """
        Extract plays with their line numbers from raw content.

        Args:
            content: Raw log content
            play_names: List of play names to find

        Returns:
            List of ParsedPlay objects with name, order, and line_number
        """
        plays: list[ParsedPlay] = []
        lines = content.split("\n")

        # Track which plays we've found to maintain order
        order = 0
        found_plays: set[str] = set()

        for line_num, line in enumerate(lines, start=1):
            match = self.PLAY_PATTERN.search(line)
            if match:
                play_name = match.group(1)
                # Only add if this play name is in our expected list
                if play_name in play_names and play_name not in found_plays:
                    plays.append(
                        ParsedPlay(name=play_name, order=order, line_number=line_num)
                    )
                    found_plays.add(play_name)
                    order += 1

        # Add any plays that weren't found in the content (shouldn't happen normally)
        for name in play_names:
            if name not in found_plays:
                plays.append(ParsedPlay(name=name, order=order, line_number=None))
                order += 1

        return plays

    def _extract_hosts_from_recap(self, parser: Play) -> list[ParsedHost]:
        """
        Extract host data from parser._recap attribute.

        Args:
            parser: Play parser instance

        Returns:
            List of ParsedHost objects with task counts
        """
        hosts = []

        # Access the internal _recap dict
        recap = getattr(parser, "_recap", {})

        for hostname, counts in recap.items():
            host = ParsedHost(
                hostname=hostname,
                ok=counts.get("ok", 0),
                changed=counts.get("changed", 0),
                failed=counts.get("failed", 0),
                unreachable=counts.get("unreachable", 0),
                skipped=counts.get("skipped", 0),
                rescued=counts.get("rescued", 0),
                ignored=counts.get("ignored", 0),
            )
            hosts.append(host)

        return hosts

    def _extract_tasks_from_plays(self, parser: Play, content: str) -> list[ParsedTask]:
        """
        Extract task-level data from parsed plays.

        Args:
            parser: Play parser instance with parsed data
            content: Raw log content for line number extraction

        Returns:
            List of ParsedTask objects with executions per host
        """
        tasks: list[ParsedTask] = []
        task_order = 0

        # parser.plays() returns Dict[play_name, Dict[task_name, Tasks]]
        plays_data = parser.plays()

        for play_name, play_tasks in plays_data.items():
            for task_name, task_obj in play_tasks.items():
                results: list[ParsedTaskResult] = []

                # task_obj.results returns List[{host, status, failure_message}]
                task_results = getattr(task_obj, "results", [])
                for result in task_results:
                    hostname = result.get("host", "")
                    status = result.get("status", "ok")
                    message = result.get("failure_message") or None

                    results.append(
                        ParsedTaskResult(
                            hostname=hostname,
                            status=status,
                            message=message,
                        )
                    )

                # Find line number for this task
                line_number = self._find_task_line_number(content, task_name)

                tasks.append(
                    ParsedTask(
                        name=task_name,
                        order=task_order,
                        play_name=play_name,
                        line_number=line_number,
                        results=results,
                    )
                )
                task_order += 1

        return tasks

    def _find_task_line_number(self, content: str, task_name: str) -> Optional[int]:
        """
        Find the line number where a task is defined.

        Args:
            content: Raw log content
            task_name: Name of the task to find

        Returns:
            Line number (1-indexed) or None if not found
        """
        for line_num, line in enumerate(content.split("\n"), start=1):
            match = self.TASK_PATTERN.search(line)
            if match and match.group(1) == task_name:
                return line_num
        return None


def determine_status(host: ParsedHost) -> str:
    """
    Determine the overall status for a host based on task counts.

    Args:
        host: ParsedHost with task counts

    Returns:
        'failed' if any failed/unreachable, 'changed' if any changed, else 'ok'
    """
    if host.failed > 0 or host.unreachable > 0:
        return "failed"
    if host.changed > 0:
        return "changed"
    return "ok"
