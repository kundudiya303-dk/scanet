"""
Tests for subdomain_takeover analyzer module.
"""
from analyzers.subdomain_takeover import (
    TAKEOVER_SIGNATURES,
    check_subdomain_takeover,
    check_dns_zone_transfer,
    audit_subdomains_takeover
)


def test_takeover_signatures_completeness():
    providers = [sig["provider"] for sig in TAKEOVER_SIGNATURES]
    assert "GitHub Pages" in providers
    assert "Amazon AWS S3 Bucket" in providers
    assert "Heroku" in providers
    assert "Shopify" in providers
    assert "AWS CloudFront" in providers
    assert "Microsoft Azure Web Apps" in providers


def test_takeover_detection_clean_domain():
    # Test safe domain with non-matching CNAME
    result = check_subdomain_takeover("safe.example.com", "primary-lb.example.com")
    assert result["is_vulnerable"] is False
    assert result["provider"] is None


def test_dns_zone_transfer_structure():
    result = check_dns_zone_transfer("example.com", "127.0.0.1")
    assert "axfr_permitted" in result
    assert "status" in result
    assert "remediation" in result
    assert result["axfr_permitted"] is False


def test_audit_subdomains_takeover_batch():
    subdomains = [
        {"domain": "safe1.example.com", "cname": "prod.corp.com"},
        {"domain": "safe2.example.com", "cname": "cdn.internal.net"}
    ]
    findings = audit_subdomains_takeover(subdomains)
    assert isinstance(findings, list)
    assert len(findings) == 0
