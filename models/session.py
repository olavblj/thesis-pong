import requests

from config import URL, ch_names
from system_manager import SystemManager
from utils.prints import Print

sys_manager = SystemManager.get_instance()


class Session:
    def __init__(self, id, **kwargs):
        self.id = id
        self.ch_names = kwargs["ch_names"]
        self.ch_count = len(self.ch_names)
        self.time_frames = list()

    @classmethod
    def create(cls):
        url = URL.sessions

        payload = dict(
            person=sys_manager.person.id,
            ch_names=ch_names,
            is_real_data=sys_manager.is_real_data
        )

        r = requests.post(url, data=payload)
        json_resp = r.json()

        obj = cls(**json_resp)

        if r.status_code == 201:
            Print.api("Created New Session ({})".format(obj.id))
        else:
            Print.failure("Something went wrong")

        return obj
