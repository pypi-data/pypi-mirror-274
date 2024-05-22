from typing import Optional, Dict, Any
import datetime

class Group:
    def __init__(
            self,
            device_group_no: str,
            device_group_name: str,
            house_no: str,
            room_no: str,
            icon: str,
            is_favorite: bool,
            favorite_time: str,
            create_time: str,
            update_time: str,
            execute_way: int,
            device_group_type: str,
            seq: int,
            value: Optional[Dict[str, Any]] = None,
            sync_host_sequences: Optional[list] = None
    ):
        self.device_group_no: str = device_group_no
        self.device_group_name: str = device_group_name
        self.house_no: str = house_no
        self.room_no: str = room_no
        self.icon: str = icon
        self.is_favorite: bool = is_favorite
        self.favorite_time: datetime.datetime = self.safe_parse_datetime(favorite_time)
        self.create_time: datetime.datetime = self.safe_parse_datetime(create_time)
        self.update_time: datetime.datetime = self.safe_parse_datetime(update_time)
        self.execute_way: int = execute_way
        self.device_group_type: str = device_group_type
        self.seq: int = seq
        self.value: Optional[Dict[str, Any]] = value
        self.sync_host_sequences: Optional[list] = sync_host_sequences

    @staticmethod
    def safe_parse_datetime(datetime_str: str) -> datetime.datetime | None:
        if datetime_str == "" or datetime_str is None:
            return None
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return (f"Device Group No: {self.device_group_no}, "
                f"Device Group Name: {self.device_group_name}, "
                f"House No: {self.house_no}, "
                f"Room No: {self.room_no}, "
                f"Icon: {self.icon}, "
                f"Is Favorite: {self.is_favorite}, "
                f"Favorite Time: {self.favorite_time}, "
                f"Create Time: {self.create_time}, "
                f"Update Time: {self.update_time}, "
                f"Execute Way: {self.execute_way}, "
                f"Device Group Type: {self.device_group_type}, "
                f"Seq: {self.seq}, "
                f"Value: {self.value}, "
                f"Sync Host Sequences: {self.sync_host_sequences}")
