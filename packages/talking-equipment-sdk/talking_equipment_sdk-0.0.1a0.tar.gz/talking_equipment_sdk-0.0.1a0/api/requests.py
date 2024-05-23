from typing import Callable
from concurrent.futures import ThreadPoolExecutor


class TalkingEquipmentRequest:
    def __init__(self, request_handler: Callable[..., any], **kwargs):
        self.ossit_api_requestor = request_handler
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.ossit_api_requestor(**self.kwargs)


class ThreadRequestPool:
    def __init__(self, max_threads: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=max_threads)
        self._talking_equipment_requests: list = []

    def add_request(self, request_handler: Callable[..., any], **kwargs):
        self._talking_equipment_requests.append(TalkingEquipmentRequest(request_handler, **kwargs))

    def execute(self):
        for talking_equipment_request in self._talking_equipment_requests:
            self.executor.submit(talking_equipment_request)
        self.shutdown()

    def shutdown(self):
        self.executor.shutdown(wait=False)