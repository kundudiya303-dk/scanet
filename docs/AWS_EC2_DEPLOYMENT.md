# scanet — Complete AWS EC2 Cloud Deployment Guide

**Production-Hardened, Cost-Optimized Deployment for University Labs & Cloud Audits**  
*Compatibility: Amazon Linux 2023, Ubuntu 22.04 / 24.04 LTS | Architectures: ARM64 (Graviton) & x86_64 (AMD64)*

---

## ⚡ Quick 60-Second Start: Direct HTTP Access on EC2 (No Domain / No HTTPS Needed)

If you just want to run the single script on your EC2 instance and immediately view the colorful web dashboard over HTTP using your EC2 Public IP:

### 1. In AWS Console: Open Port 8000 in your EC2 Security Group
- Go to **EC2 Console** $\rightarrow$ **Instances** $\rightarrow$ select your instance $\rightarrow$ **Security** tab $\rightarrow$ click your **Security Group**.
- Click **Edit inbound rules** $\rightarrow$ **Add rule**:
  - **Type:** `Custom TCP`
  - **Port Range:** `8000`
  - **Source:** `0.0.0.0/0` (or `My IP` for enhanced privacy)
- Click **Save rules**.

### 2. On your EC2 Terminal: Run the One-Click Script
```bash
# Clone the repository
git clone https://github.com/kundudiya303-dk/scanet.git
cd scanet

# Run the universal launcher (auto-detects EC2 Public IP and binds to 0.0.0.0:8000)
./run.sh
```
*Tip: To run on a different port like 8080 or 80, simply pass the port number: `./run.sh 8080` or `sudo ./run.sh 80`.*

### 3. Open in your Browser:
```
http://<YOUR_EC2_PUBLIC_IP>:8000
```
*(The script will automatically detect and print your exact `http://<EC2-PUBLIC-IP>:8000` link in the terminal!)*

---

## 1. Cloud Architecture & Sizing Recommendation

`scanet` is engineered to operate efficiently with an ultra-lightweight memory footprint ($\le 120\text{ MB}$ idle, $\le 650\text{ MB}$ peak during active scans).

### Recommended EC2 Instance Types:
| Instance Type | vCPU | RAM | Architecture | Estimated Monthly Cost | Recommended Use Case |
|---|---|---|---|---|---|
| **`t4g.micro`** | 2 | 1.0 GB | ARM64 (AWS Graviton2) | **$\sim \$6.13$ / month** | **Recommended Production Choice (Best performance/price)** |
| **`t3.micro`** | 2 | 1.0 GB | x86_64 (Intel Xeon) | **$\sim \$7.60$ / month** | **AWS Free Tier Eligible (12 months free)** |
| **`t4g.small`** | 2 | 2.0 GB | ARM64 (AWS Graviton2) | $\sim \$12.26$ / month | High-concurrency classroom lab (10+ students) |

---

## 2. Step 1: EC2 Instance Launch & AWS Security Hardening

### 2.1 Enforce IMDSv2 (Critical Security Guardrail)
To prevent Server-Side Request Forgery (SSRF) attacks from extracting AWS IAM instance role credentials, you **MUST** enforce IMDSv2 with a hop limit of `1`.

When launching via AWS CLI:
```bash
aws ec2 run-instances \
    --image-id ami-04b70fa74e45c3917 \
    --instance-type t4g.micro \
    --key-name scanet-key \
    --security-group-ids sg-xxxxxx \
    --metadata-options "HttpTokens=required,HttpPutResponseHopLimit=1,HttpEndpoint=enabled" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=scanet-lab-node}]'
```

If configuring via AWS Console:
- Expand **Advanced Details** $\rightarrow$ **Metadata accessible**: *Enabled*
- **Metadata version**: *V2 only (token required)*
- **Metadata response hop limit**: `1`

---

### 2.2 Configure EC2 Security Group Rules

Create a dedicated Security Group named `scanet-secgroup`:

#### Inbound Rules:
| Protocol | Port Range | Source | Justification |
|---|---|---|---|
| **SSH** | `22` | `YOUR_CAMPUS_OR_HOME_IP/32` | Administrative shell access (never `0.0.0.0/0`) |
| **HTTPS** | `443` | `YOUR_CAMPUS_CIDR` or `0.0.0.0/0` | Secure SSL Web Dashboard |
| **HTTP** | `80` | `0.0.0.0/0` | Let's Encrypt Certbot challenge (redirects to 443) |

#### Outbound Rules:
| Protocol | Port Range | Destination | Justification |
|---|---|---|---|
| **All Traffic** or **TCP 80/443/DNS** | All | `0.0.0.0/0` | Target scanning & package updates |

---

## 3. Step 2: System Provisioning & Package Installation

Connect to your EC2 instance via SSH:
```bash
ssh -i scanet-key.pem ubuntu@<YOUR_EC2_PUBLIC_IP>
```

Update system packages and install prerequisites:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl ufw nginx nmap mtr-tiny
```

---

## 4. Step 3: Clone Repository & Install scanet

```bash
# 1. Clone the scanet repository
git clone https://github.com/kundudiya303-dk/scanet.git /opt/scanet-app
cd /opt/scanet-app

# 2. Run the automated multi-architecture installer
chmod +x scripts/install.sh scripts/health_check.sh
./scripts/install.sh
```

---

## 5. Step 4: Python Virtual Environment & Configuration

```bash
cd /opt/scanet-app/backend

# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Create production .env configuration
cat << 'EOF' > .env
HOST=127.0.0.1
PORT=8000
DEBUG=False
SECRET_KEY=generate-a-strong-random-key-here-for-production
DATABASE_URL=sqlite+aiosqlite:///./data/scanet.db
MAX_CONCURRENT_JOBS=2
DEFAULT_JOB_TIMEOUT=600
CORS_ORIGINS=["https://your-domain.com", "http://localhost:8000"]
EOF
```

---

## 6. Step 5: Systemd Daemon Service Configuration

Keep `scanet` running continuously in the background and auto-restart on crashes or reboot.

Create the service file `/etc/systemd/system/scanet.service`:
```bash
sudo bash -c 'cat << "EOF" > /etc/systemd/system/scanet.service
[Unit]
Description=scanet Cybersecurity Reconnaissance Platform
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/scanet-app/backend
Environment="PATH=/opt/scanet-app/backend/.venv/bin:/opt/scanet/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/scanet-app/backend/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF'
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable scanet
sudo systemctl start scanet
sudo systemctl status scanet --no-pager
```

---

## 7. Step 6: Nginx Reverse Proxy with Free HTTPS (Let's Encrypt)

Create Nginx site configuration `/etc/nginx/sites-available/scanet`:
```bash
sudo bash -c 'cat << "EOF" > /etc/nginx/sites-available/scanet
server {
    listen 80;
    server_name your-domain.com; # Or your EC2 Public IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Enable Server-Sent Events (SSE) streaming without buffering
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
EOF'

sudo ln -s /etc/nginx/sites-available/scanet /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

### Free SSL with Let's Encrypt (Certbot):
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 8. Step 7: Verification & Health Check

Run the built-in automated test suite:
```bash
cd /opt/scanet-app
python3 -c "import sys; sys.path.insert(0, './backend'); sys.path.insert(0, '.'); from tests.test_engine.test_scope_validator import test_loopback_is_blocked, test_aws_imds_is_blocked, test_approved_target_passes, test_non_whitelisted_target_blocked; from tests.test_adapters.test_nmap_adapter import test_parses_open_ports_only, test_parses_host_ip, test_parses_service_info, test_empty_output_no_crash; from tests.test_analyzers.test_ai_advisor import test_ai_advisor_port_exposure, test_ai_advisor_clean_target; from tests.test_analyzers.test_cve_correlator import test_correlate_openssh_regresshion, test_correlate_apache_path_traversal; from tests.test_adapters.test_nuclei_adapter import test_nuclei_build_command, test_nuclei_parse_output; from tests.test_analyzers.test_os_fingerprint import test_ttl_linux_deduction, test_ttl_windows_deduction, test_ttl_cisco_network_deduction, test_ssh_banner_deduction, test_http_iis_banner_deduction, test_port_profile_windows, test_composite_fingerprinting; test_loopback_is_blocked(); test_aws_imds_is_blocked(); test_approved_target_passes(); test_non_whitelisted_target_blocked(); test_parses_open_ports_only(); test_parses_host_ip(); test_parses_service_info(); test_empty_output_no_crash(); test_ai_advisor_port_exposure(); test_ai_advisor_clean_target(); test_correlate_openssh_regresshion(); test_correlate_apache_path_traversal(); test_nuclei_build_command(); test_nuclei_parse_output(); test_ttl_linux_deduction(); test_ttl_windows_deduction(); test_ttl_cisco_network_deduction(); test_ssh_banner_deduction(); test_http_iis_banner_deduction(); test_port_profile_windows(); test_composite_fingerprinting(); print('EC2 HEALTH CHECK: ALL 21 TESTS PASSED!')"
```

Verify backend live health endpoint:
```bash
curl -s http://127.0.0.1:8000/api/v1/system/health | jq .
curl -s http://127.0.0.1:8000/api/v1/system/tools | jq .
```

Access your web dashboard at: `https://your-domain.com` or `http://<EC2_PUBLIC_IP>`

---
*End of AWS EC2 Deployment Handbook.*
