# scanet wordlists directory
# Place wordlist .txt files here for FFUF and Gobuster integration.
# These wordlists are restricted to this directory by path validation.

Included:
- common.txt       — Common web directories and files (SecLists: Discovery/Web-Content/common.txt)
- big.txt          — Larger wordlist for deeper discovery
- api-endpoints.txt — REST API path discovery

Download recommended sources:
  SecLists: https://github.com/danielmiessler/SecLists
  DirBuster Wordlists: bundled with Kali Linux at /usr/share/dirbuster/wordlists/
