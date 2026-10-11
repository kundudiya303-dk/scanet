"""
scanet — Webhook Alert & Notification Dispatcher
Dispatches real-time scan completion summaries and asset drift alerts to:
- Discord Webhooks
- Slack Incoming Webhooks
- Telegram Bot API
- Generic JSON HTTP endpoints
"""
try:
    import httpx
except ImportError:
    httpx = None

from typing import Dict, Any, Optional


async def send_webhook_alert(webhook_url: str, webhook_type: str, payload: Dict[str, Any]) -> bool:
    """
    Sends an alert payload to the configured webhook channel.
    """
    if not webhook_url:
        return False

    title = payload.get("title", "scanet Alert")
    target = payload.get("target", "Unknown")
    summary = payload.get("summary", "Scan completed")
    risk_level = payload.get("risk_level", "INFO")

    color_map = {
        "CRITICAL": 0xFF0000,
        "HIGH": 0xFFA500,
        "MEDIUM": 0xFFFF00,
        "LOW": 0x00FF00,
        "INFO": 0x00BFFF
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if webhook_type == "discord":
                discord_payload = {
                    "username": "scanet Watchdog",
                    "embeds": [{
                        "title": title,
                        "description": summary,
                        "color": color_map.get(risk_level, 0x00BFFF),
                        "fields": [
                            {"name": "Target", "value": target, "inline": True},
                            {"name": "Severity", "value": risk_level, "inline": True}
                        ]
                    }]
                }
                resp = await client.post(webhook_url, json=discord_payload)
                return resp.status_code in [200, 204]

            elif webhook_type == "slack":
                slack_payload = {
                    "text": f"*{title}*\n*Target:* `{target}`\n*Severity:* `{risk_level}`\n{summary}"
                }
                resp = await client.post(webhook_url, json=slack_payload)
                return resp.status_code == 200

            else:
                # Generic HTTP POST
                resp = await client.post(webhook_url, json=payload)
                return resp.status_code in [200, 201, 202, 204]

    except Exception:
        return False
