import json
import requests
import os

def send_slack_notification():
    webhook_url = os.environ["SLACK_QA_WEBHOOK_URL"]
    apps = ["wisp", "fdr"]
    base_path = "public"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🚀 pagoPA Platform Integration Test", "emoji": True}
        },
        {"type": "divider"}
    ]

    for app in apps:
        app_title = app.upper() + " Tests"
        stats_file = f"{base_path}/{app}-tests/last-history/stats.json"
        summary_file = f"{base_path}/{app}-tests/last-history/widgets/summary.json"

        if os.path.exists(stats_file) and os.path.exists(summary_file):
            with open(stats_file) as f:
                stats = json.load(f)
            with open(summary_file) as f:
                summary = json.load(f)

            passed = stats.get("passed", 0)
            failed = stats.get("failed", 0)
            skipped = stats.get("skipped", 0)
            duration_ms = summary.get("time", {}).get("duration", 0)
            duration_sec = duration_ms // 1000
            minutes = duration_sec // 60
            seconds = duration_sec % 60
            duration_formatted = f"{minutes}m {seconds}s"

            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{app_title}*\n• ✅ Passed: {passed}\n• ❌ Failed: {failed}\n• ⚡ Skipped: {skipped}\n• ⏱️ Duration: {duration_formatted}"
                }
            })
            blocks.append({"type": "divider"})
        else:
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{app_title}*\n⚠️ No data available."}
            })
            blocks.append({"type": "divider"})

    payload = {"blocks": blocks}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Failed to send message to Slack: {response.text}")
        exit(1)

if __name__ == "__main__":
    send_slack_notification()
