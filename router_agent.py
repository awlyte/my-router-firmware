import os
import json
import requests

def get_router_metrics():
    with open('/proc/loadavg', 'r') as f:
        load = f.read().split()
    try:
        with open('/var/lib/misc/dnsmasq.leases', 'r') as f:
            devices = len(f.readlines())
    except FileNotFoundError:
        devices = 0
    return {
        "cpu_load_1min": load[0],
        "connected_devices": devices
    }

def consult_ai(metrics):
    api_url = "https://openrouter.ai"
    api_key = "YOUR_OPENROUTER_API_KEY" # Replace with your real key later
    
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a local network optimization AI. Analyze metrics and reply with a 1-sentence diagnostic update."},
            {"role": "user", "content": f"CPU Load: {metrics['cpu_load_1min']}, Active Devices: {metrics['connected_devices']}."}
        ]
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Telemetry failed: {str(e)}"

if __name__ == "__main__":
    stats = get_router_metrics()
    print("AI Analysis Profile:\n", consult_ai(stats))
