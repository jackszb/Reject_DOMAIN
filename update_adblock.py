#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

ADLIST_URL = "https://raw.githubusercontent.com/REIJI007/AdBlock_Rule_For_Sing-box/main/adblock_reject_domain.txt"
TXT_FILE = "reject-domain.txt"
JSON_FILE = "reject-domain.json"

# 下载广告列表
response = requests.get(ADLIST_URL)
response.raise_for_status()
lines = response.text.splitlines()

domains = set()
for line in lines:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    # 去掉首尾引号和末尾逗号，彻底清理
    clean_line = line
    if clean_line.startswith('"') and clean_line.endswith('",'):
        clean_line = clean_line[1:-2]  # 去掉首尾引号和逗号
    elif clean_line.startswith('"') and clean_line.endswith('"'):
        clean_line = clean_line[1:-1]
    elif clean_line.endswith(','):
        clean_line = clean_line[:-1]
    clean_line = clean_line.strip()
    if clean_line:
        domains.add(clean_line)

domains = sorted(domains)

# 写入 TXT
with open(TXT_FILE, "w", encoding="utf-8") as f:
    for d in domains:
        f.write(d + "\n")

# 写入 JSON
singbox_json = {
    "version": 3,
    "rules": [
        {
            "domain_suffix": domains
        }
    ]
}

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(singbox_json, f, indent=2, ensure_ascii=False)

print(f"生成完成: {TXT_FILE} 和 {JSON_FILE}，共 {len(domains)} 个域名")
