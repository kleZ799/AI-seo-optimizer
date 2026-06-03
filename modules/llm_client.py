"""
Shared helper: call Claude (Anthropic) API and return the text response.
"""

import anthropic


def ask_claude(api_key: str, prompt: str, system: str = "", max_tokens: int = 1500) -> str:
    """Send a prompt to Claude and return the reply as a string."""
    client = anthropic.Anthropic(api_key=api_key)
    messages = [{"role": "user", "content": prompt}]
    kwargs = dict(
        model="claude-opus-4-5",
        max_tokens=max_tokens,
        messages=messages,
    )
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text
