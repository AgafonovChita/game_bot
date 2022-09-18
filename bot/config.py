from dataclasses import dataclass

admins = [707453011, 101249590]

@dataclass
class Config:
    bot_token: str = "5759693042:AAHCTi4GbWqQdS5ZoAW2kAE6WkT-wRFJ4P0"
    db_name: str = 'travel_game.db'
    db_url: str = 'sqlite+aiosqlite:///travel_game.db'


