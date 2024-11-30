import json
import sys


def generate_message(context):
    event_name = context["event_name"]
    repo_name = context["repository"]

    messages = {
        "push": lambda: generate_push_message(context, repo_name),
        "issues": lambda: generate_issue_message(context, repo_name),
        "pull_request": lambda: generate_pr_message(context, repo_name),
    }

    # Fallback message for unknown events
    default_message = f"💡 Unknown event: {event_name} in {repo_name}."
    return messages.get(event_name, lambda: default_message)()


def generate_push_message(context, repo_name):
    event = context.get("event", {})
    commits = event.get("commits", [])
    branch = context["ref"].split("/")[
        -1
    ]  # Extract branch name from 'refs/heads/branch-name'
    commit_links = [f"- [{commit['message']}]({commit['url']})" for commit in commits]
    commit_messages = (
        "\n".join(commit_links) if commit_links else "No commits available."
    )
    return f"🚀 Push to branch `{branch}` in *{repo_name}* with {len(commits)} commits:\n{commit_messages}"


def generate_issue_message(context, repo_name):
    event = context.get("event", {})
    issue = event.get("issue", {})
    title = issue.get("title", "")
    url = issue.get("html_url", "")
    action = event.get("action", "")
    return f"🐛 Issue *{action}* in *{repo_name}*: [{title}]({url})"


def generate_pr_message(context, repo_name):
    event = context.get("event", {})
    pr = event.get("pull_request", {})
    title = pr.get("title", "")
    url = pr.get("html_url", "")
    action = event.get("action", "")
    return f"📬 Pull Request *{action}* in *{repo_name}*: [{title}]({url})"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_message.py <github_context_json>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        # Load GitHub context JSON
        github_context = json.loads(f.read())

    # Generate and print the message
    print(generate_message(github_context))
