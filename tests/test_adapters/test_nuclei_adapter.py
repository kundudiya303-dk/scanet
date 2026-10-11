"""
scanet — Unit Tests for Nuclei Adapter
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

from adapters.nuclei_adapter import NucleiAdapter


def test_nuclei_build_command():
    adapter = NucleiAdapter()
    cmd = adapter.build_command_args("example.com", {"tags": "ssl,misconfig", "rate_limit": 25})
    assert cmd[0] == "nuclei"
    assert "-target" in cmd
    assert "https://example.com" in cmd
    assert "-jsonl" in cmd
    assert "-tags" in cmd
    assert "ssl,misconfig" in cmd


def test_nuclei_parse_output():
    adapter = NucleiAdapter()
    sample_jsonl = '{"template-id":"http-missing-security-headers","info":{"name":"Missing Security Headers","severity":"info","description":"HTTP headers missing"},"matched-at":"https://example.com"}\n'
    result = adapter.parse_output(sample_jsonl, 0)
    assert result["total_findings"] == 1
    assert result["findings"][0]["template_id"] == "http-missing-security-headers"

