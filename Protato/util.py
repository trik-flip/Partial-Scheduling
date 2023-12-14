def format_time(time: float) -> str:
    if isinstance(time, str):
        return time
    if time == 0:
        return "N/A"
    if time > 1_000_000_000:
        return f"{time/1_000_000_000:.2f}s"
    if time > 1_000_000:
        return f"{time/1_000_000:.2f}ms"
    if time > 1_000:
        return f"{time/1_000:.2f}us"
    return f"{time:.2f}ns"
