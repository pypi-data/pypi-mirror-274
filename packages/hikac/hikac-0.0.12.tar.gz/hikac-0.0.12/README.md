# HIKAC

This modest python package helps you to get events from HIKVISION AC terminals. 

## Installation

```sh
pip install hikac

```

## Usage in FastAPI

```sh

from hikac import get_data_from_ac_event

@attandance_router.post("/attandance/face-id", include_in_schema=False)
async def listen_for_ac_event(
    req: Request,
    db: Session = ActiveSession,
):
    try:

        # use the class to collect nececary items of dict
        eventData = await get_data_from_ac_event(req)

        if eventData.attendanceStatus:

            #you can use these attributes
            #eventData.deviceIpAddress
            #eventData.attendanceStatus
            #eventData.deviceName
            #eventData.dateTime
            #eventData.employeeId
            #eventData.employeeName

            # write  your logic here

            return "success"
    except Exception as e:
        print(e.args)
```

