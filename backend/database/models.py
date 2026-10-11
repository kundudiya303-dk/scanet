"""
scanet — SQLAlchemy ORM Models
Defines all database tables.
"""
from sqlalchemy import (
    Column, String, Integer, Text, Boolean,
    DateTime, ForeignKey, func
)
from sqlalchemy.orm import relationship
from database.connection import Base
import uuid


def new_uuid() -> str:
    return str(uuid.uuid4())


# ── Authorized Targets ────────────────────────────────────────────────────────
class Target(Base):
    __tablename__ = "targets"

    id          = Column(String, primary_key=True, default=new_uuid)
    name        = Column(String(128), nullable=False)
    value       = Column(String(256), nullable=False)   # IP, CIDR, or domain
    target_type = Column(String(32), nullable=False)     # 'ip', 'cidr', 'domain'
    is_approved = Column(Boolean, default=True)
    notes       = Column(Text, nullable=True)
    created_at  = Column(DateTime, server_default=func.now())
    created_by  = Column(String(128), nullable=False, default="admin")

    jobs = relationship("ScanJob", back_populates="target", cascade="all, delete-orphan")


# ── Scan Jobs ─────────────────────────────────────────────────────────────────
class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id            = Column(String, primary_key=True, default=new_uuid)
    target_id     = Column(String, ForeignKey("targets.id", ondelete="CASCADE"))
    tool_name     = Column(String(64), nullable=False)
    profile_name  = Column(String(128), nullable=False)
    status        = Column(String(32), nullable=False, default="queued")
    parameters    = Column(Text, nullable=False)          # JSON string
    pid           = Column(Integer, nullable=True)
    started_at    = Column(DateTime, nullable=True)
    completed_at  = Column(DateTime, nullable=True)
    exit_code     = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    target    = relationship("Target", back_populates="jobs")
    hosts     = relationship("Host", back_populates="job", cascade="all, delete-orphan")
    endpoints = relationship("Endpoint", back_populates="job", cascade="all, delete-orphan")
    findings  = relationship("Finding", back_populates="job", cascade="all, delete-orphan")


# ── Normalized: Hosts ─────────────────────────────────────────────────────────
class Host(Base):
    __tablename__ = "hosts"

    id             = Column(String, primary_key=True, default=new_uuid)
    job_id         = Column(String, ForeignKey("scan_jobs.id", ondelete="CASCADE"))
    ip_address     = Column(String(64), nullable=False)
    hostname       = Column(String(256), nullable=True)
    os_fingerprint = Column(String(256), nullable=True)
    status         = Column(String(16), nullable=False, default="up")
    created_at     = Column(DateTime, server_default=func.now())

    job   = relationship("ScanJob", back_populates="hosts")
    ports = relationship("Port", back_populates="host", cascade="all, delete-orphan")


# ── Normalized: Ports ─────────────────────────────────────────────────────────
class Port(Base):
    __tablename__ = "ports"

    id           = Column(String, primary_key=True, default=new_uuid)
    host_id      = Column(String, ForeignKey("hosts.id", ondelete="CASCADE"))
    port_number  = Column(Integer, nullable=False)
    protocol     = Column(String(8), nullable=False, default="tcp")
    state        = Column(String(16), nullable=False)
    service_name = Column(String(64), nullable=True)
    product      = Column(String(128), nullable=True)
    version      = Column(String(128), nullable=True)
    banner       = Column(Text, nullable=True)

    host = relationship("Host", back_populates="ports")


# ── Normalized: HTTP Endpoints ────────────────────────────────────────────────
class Endpoint(Base):
    __tablename__ = "endpoints"

    id             = Column(String, primary_key=True, default=new_uuid)
    job_id         = Column(String, ForeignKey("scan_jobs.id", ondelete="CASCADE"))
    url            = Column(String(2048), nullable=False)
    status_code    = Column(Integer, nullable=True)
    content_length = Column(Integer, nullable=True)
    title          = Column(String(512), nullable=True)
    tech_stack     = Column(Text, nullable=True)           # JSON array string
    created_at     = Column(DateTime, server_default=func.now())

    job = relationship("ScanJob", back_populates="endpoints")


# ── Normalized: Security Findings ────────────────────────────────────────────
class Finding(Base):
    __tablename__ = "findings"

    id          = Column(String, primary_key=True, default=new_uuid)
    job_id      = Column(String, ForeignKey("scan_jobs.id", ondelete="CASCADE"))
    target_id   = Column(String, ForeignKey("targets.id"))
    category    = Column(String(64), nullable=False)     # 'ssl', 'headers', 'misconfig'
    severity    = Column(String(16), nullable=False)     # 'info', 'low', 'medium', 'high'
    title       = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    evidence    = Column(Text, nullable=True)
    remediation = Column(Text, nullable=True)
    created_at  = Column(DateTime, server_default=func.now())

    job = relationship("ScanJob", back_populates="findings")


# ── Audit Logs ────────────────────────────────────────────────────────────────
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id            = Column(String, primary_key=True, default=new_uuid)
    user_id       = Column(String(128), nullable=False)
    action        = Column(String(64), nullable=False)
    resource_type = Column(String(64), nullable=False)
    resource_id   = Column(String, nullable=True)
    details       = Column(Text, nullable=True)           # JSON
    ip_address    = Column(String(64), nullable=False)
    timestamp     = Column(DateTime, server_default=func.now())
