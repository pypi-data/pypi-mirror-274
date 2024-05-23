import json
import re
from datetime import datetime

from starlette.requests import Request


class HikvsionEvent:

    # device's ip address
    deviceIpAddress: str

    # type of attandance can be 'checkIn' or 'checkOut' or None
    attendanceStatus: str

    # name of the device
    deviceName: str

    # date and time of the event
    dateTime: str

    # employee id can be None if the event is not ac event
    employeeId: str

    # employee name can be None if the event is not ac event
    employeeName: str

    def __init__(self, data_dict: dict) -> None:
        ACEvent = data_dict['AccessControllerEvent']
        self.attendanceStatus = ACEvent['attendanceStatus']
        self.employeeId = ACEvent['employeeNoString']
        self.employeeName = ACEvent['name']
        self.deviceName = ACEvent['deviceName']
        self.deviceIpAddress = data_dict['ipAddress']
        date_str = data_dict['dateTime']
        date_obj = datetime.fromisoformat(date_str[:-6])
        self.dateTime = date_obj.strftime("%Y-%m-%d %H:%M:%S")


async def get_data_from_ac_event(request: Request):
      # receive the body of the data from the request
        data = await request.body()

        # decode the type of data from REQUST to str
        data_str = data.decode()

        # here we have to search the json inside the string
        match = re.search(r'\{.*\}', data_str, re.DOTALL)

        # after finding needy json from the str
        json_data = match.group(0) if match else None

        # Load JSON data into a Python dictionary
        data_dict = json.loads(json_data) if json_data else None

        # use the class to collect nececary items of dict
        eventData = HikvsionEvent(data_dict)

        return eventData
