from datetime import datetime

from pydantic import BaseModel


class USGAAPAccount(BaseModel):
    """DataClass for US-GAAP taxonomy based account instances"""
    name: str
    context_ref: str
    decimals: str
    id: str
    unit_ref: str  # TODO: change to a dataclass
    value: float
    entity_id: str
    start_date: datetime
    end_date: datetime
