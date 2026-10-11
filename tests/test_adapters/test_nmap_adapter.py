"""
scanet — Nmap Adapter Unit Tests
Tests XML output parsing without requiring nmap to be installed.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

try:
    import pytest
except ImportError:
    class _PytestMock:
        def fixture(self, f):
            return f
    pytest = _PytestMock()

from adapters.nmap_adapter import NmapAdapter


SAMPLE_NMAP_XML = """<?xml version="1.0"?>
<nmaprun>
  <host>
    <address addr="192.168.1.10" addrtype="ipv4"/>
    <hostnames><hostname name="target.local" type="user"/></hostnames>
    <ports>
      <port protocol="tcp" portid="22">
        <state state="open"/>
        <service name="ssh" product="OpenSSH" version="8.9"/>
      </port>
      <port protocol="tcp" portid="80">
        <state state="open"/>
        <service name="http" product="nginx" version="1.24.0"/>
      </port>
      <port protocol="tcp" portid="8080">
        <state state="filtered"/>
        <service name="http-proxy"/>
      </port>
    </ports>
  </host>
</nmaprun>"""


@pytest.fixture
def adapter():
    return NmapAdapter()


def test_parses_open_ports_only(adapter=None):
    if adapter is None: adapter = NmapAdapter()
    result = adapter.parse_output(SAMPLE_NMAP_XML, 0)
    assert result["open_ports_count"] == 2


def test_parses_host_ip(adapter=None):
    if adapter is None: adapter = NmapAdapter()
    result = adapter.parse_output(SAMPLE_NMAP_XML, 0)
    assert result["hosts"][0]["ip"] == "192.168.1.10"


def test_parses_service_info(adapter=None):
    if adapter is None: adapter = NmapAdapter()
    result = adapter.parse_output(SAMPLE_NMAP_XML, 0)
    port_22 = result["hosts"][0]["ports"][0]
    assert port_22["service"] == "ssh"
    assert port_22["product"] == "OpenSSH"


def test_empty_output_no_crash(adapter=None):
    if adapter is None: adapter = NmapAdapter()
    result = adapter.parse_output("", 0)
    assert result["open_ports_count"] == 0



def test_command_args_no_shell_strings(adapter):
    args = adapter.build_command_args("192.168.1.10", {"speed": "3", "ports": "top-100"})
    assert isinstance(args, list)
    assert all(isinstance(a, str) for a in args)
    # No shell metacharacters in argument values
    for arg in args:
        assert "&&" not in arg and "|" not in arg and ";" not in arg
