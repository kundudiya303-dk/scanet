"""
scanet — SSL Certificate Analyzer
Native Python TLS inspection without external tools.
Extracts: certificate chain, SANs, issuer, expiry, and cipher strength.
"""
import ssl
import socket
import datetime
from typing import Optional


async def inspect_ssl(hostname: str, port: int = 443, timeout: int = 10) -> dict:
    """
    Connects to hostname:port and extracts TLS certificate details.
    Zero external tool dependency — uses Python's built-in ssl module.
    """
    result = {
        "hostname":   hostname,
        "port":       port,
        "subject":    {},
        "issuer":     {},
        "san":        [],
        "not_before": None,
        "not_after":  None,
        "days_remaining": None,
        "expired":    False,
        "cipher":     {},
        "tls_version": None,
        "error":      None,
    }

    try:
        ctx = ssl.create_default_context()
        conn = ctx.wrap_socket(
            socket.create_connection((hostname, port), timeout=timeout),
            server_hostname=hostname,
        )
        cert     = conn.getpeercert()
        cipher   = conn.cipher()
        tls_ver  = conn.version()
        conn.close()

        result["subject"]    = dict(x[0] for x in cert.get("subject", []))
        result["issuer"]     = dict(x[0] for x in cert.get("issuer", []))
        result["tls_version"]= tls_ver
        result["cipher"]     = {"name": cipher[0], "protocol": cipher[1], "bits": cipher[2]}

        # Extract Subject Alternative Names
        for san_type, san_value in cert.get("subjectAltName", []):
            result["san"].append({"type": san_type, "value": san_value})

        # Parse validity dates
        not_before = datetime.datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
        not_after  = datetime.datetime.strptime(cert["notAfter"],  "%b %d %H:%M:%S %Y %Z")
        now        = datetime.datetime.utcnow()

        result["not_before"]     = not_before.isoformat()
        result["not_after"]      = not_after.isoformat()
        result["days_remaining"] = (not_after - now).days
        result["expired"]        = now > not_after

    except Exception as e:
        result["error"] = str(e)

    return result
