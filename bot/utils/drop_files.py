import os


async def drop_files():
    try:
        os.remove("current_protocol.xlsx")
        os.remove("final_protocol.xlsx")
    except FileNotFoundError:
        pass



