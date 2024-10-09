# WebXPloitApi

## Prerequisites

Before launching the api, configure the following two parameter files:
- `backend/WebXPloitBackend/config/params.py`
- `api/WebXPloitApi/config/params.py`

Dont run WebXPloitBackend Before WebXPloitApi

## How to Run

1. **If you are using the script after C obfuscation and server deployment**:
   ```bash
   /ubuntu/WebXPloitApi> pip install -r requirements.txt
   /ubuntu/WebXPloitApi> python launch.py
   ```

2. **Otherwise**:
   ```bash
   /ubuntu/WebXPloitApi> pip install -r requirements.txt
   /ubuntu/WebXPloitApi> python router.py
   ```