import time
import anthropic

client = anthropic.Anthropic()

def call_with_retry(max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            wait = 15 * (attempt + 1)
            print(f"[retry] Rate limited, retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
        except anthropic.APIStatusError as e:
            # Don't retry on billing/auth errors — they won't resolve themselves
            if e.status_code in (400, 401, 403):
                print(f"[error] Non-retryable API error ({e.status_code}): {e.message}")
                raise
            # Retry on 500s, 529 (overloaded), etc.
            wait = 15 * (attempt + 1)
            print(f"[retry] API error {e.status_code}, retrying in {wait}s...")
            time.sleep(wait)
    raise Exception("Max retries exceeded")