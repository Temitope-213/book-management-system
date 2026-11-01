from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    username: str
    email: str
    password_hash: str
    role: str = "user"  # safe default
    id: Optional[int] = None
    created_at: Optional[datetime] = None