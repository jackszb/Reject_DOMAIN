import requests
import json

# 下载广告域名列表
URL = "https://raw.githubusercontent.com/REIJI007/AdBlock_Rule_For_Sing-box/main/adblock_reject_domain.txt"
response = requests.get(URL)
response.raise_for_status()
lines = response.text.splitlines()

# 提取域名，忽略空行和注释行
domains = set()
for line in lines:
    line = line.strip()
    if line and not line.startswith("#"):
        line = line.strip('"').strip(',').strip()
        domains.add(line)

# 排序
domains = sorted(domains)

# 生成 reject-domain.txt
with open("reject-domain.txt", "w", encoding="utf-8") as f:
    for domain in domains:
        f.write(domain + "\n")

# 生成 reject-domain.json (Sing-box 格式)
json_data = {
    "version": 3,
    "rules": [
        {
            "domain_suffix": domains
        }
    ]
}

with open("reject-domain.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print(f"生成完成: reject-domain.txt 和 reject-domain.json，共 {len(domains)} 个域名")
