"""
scanet — Scope Validator Unit Tests
Tests that blocked ranges are correctly rejected and valid targets pass.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

import pytest
from engine.scope_validator import ScopeValidator


@pytest.fixture
def validator():
    return ScopeValidator(approved_targets=["192.168.1.10", "10.0.0.5"])


def test_loopback_is_blocked(validator):
    result = validator.validate_target("127.0.0.1")
    assert result["valid"] is False
    assert "blocked" in result["reason"].lower()


def test_aws_imds_is_blocked(validator):
    result = validator.validate_target("169.254.169.254")
    assert result["valid"] is False


def test_approved_target_passes(validator):
    result = validator.validate_target("192.168.1.10")
    assert result["valid"] is True


def test_non_whitelisted_target_blocked(validator):
    result = validator.validate_target("192.168.1.99")
    assert result["valid"] is False
    assert "whitelist" in result["reason"].lower()


def test_empty_target_rejected(validator):
    result = validator.validate_target("")
    assert result["valid"] is False
