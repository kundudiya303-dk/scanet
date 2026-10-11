"""
scanet — Base Tool Adapter Interface
All tool adapters must inherit from BaseToolAdapter.
Adding a new tool = implementing this interface. Nothing else changes.
"""
import abc
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ToolResult:
    """Standardized result returned by every tool adapter."""
    exit_code:       int
    raw_output:      str
    normalized_data: dict
    error:           Optional[str] = None


@dataclass
class AdapterMeta:
    """Metadata every adapter exposes for the system health dashboard."""
    tool_name:    str
    category:     str                 # 'port_scan', 'web_discovery', 'dns', 'http', 'ssl', 'assessment'
    tier:         int                 # 1 = core, 2 = extended, 3 = optional
    description:  str
    requires_root: bool = False
    supported_os: List[str] = field(default_factory=lambda: ["linux"])
    output_format: str = "json"       # 'json', 'xml', 'text'


class BaseToolAdapter(abc.ABC):
    """
    Abstract base class for all scanet tool adapters.

    To add a new tool:
    1. Create a new file in scanet/adapters/<toolname>_adapter.py
    2. Implement all abstract methods below
    3. Register the adapter in engine/tool_registry.py
    No other application code needs to change.
    """

    @property
    @abc.abstractmethod
    def meta(self) -> AdapterMeta:
        """Adapter metadata: name, category, tier, description."""
        pass

    def is_installed(self) -> bool:
        """
        Checks if the tool binary exists in system PATH
        or in /opt/scanet/bin/.
        """
        return shutil.which(self.meta.tool_name) is not None

    def get_version(self) -> str:
        """Returns version string from the tool binary."""
        if not self.is_installed():
            return "Not Installed"
        try:
            result = subprocess.run(
                [self.meta.tool_name, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            output = result.stdout or result.stderr
            return output.splitlines()[0].strip() if output else "Unknown"
        except Exception:
            return "Unknown"

    @abc.abstractmethod
    def build_command_args(self, target: str, options: dict) -> List[str]:
        """
        Constructs a safe argument list for the tool.

        RULES:
        - NEVER return a shell string (no 'shell=True' invocation).
        - NEVER concatenate user input directly into arguments.
        - Validate and whitelist all option values before including.
        - Always return a list of strings suitable for execve.
        """
        pass

    @abc.abstractmethod
    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        """
        Transforms raw tool output into scanet's normalized dictionary schema.
        Must return a valid dict even on parse failure (include 'parse_error' key).
        """
        pass

    def validate_options(self, options: dict) -> dict:
        """
        Sanitizes and validates incoming options against the adapter's
        allowed parameters. Override in subclasses for specific validation.
        """
        return options
