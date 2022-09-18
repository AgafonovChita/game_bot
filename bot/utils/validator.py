
async def timeout_validator(timeout: int):
    try:
        timeout = int(timeout)
    except ValueError:
        return False
    else:
        return True
