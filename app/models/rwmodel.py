from datetime import datetime, timezone

from pydantic import ConfigDict, BaseModel


class RWModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat().replace("+00:00", "Z")
        }
    )
