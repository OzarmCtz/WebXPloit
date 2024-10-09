# WebXPloitBackend

## Prerequisites

Before launching the backend, configure the following two parameter files:
- `backend/WebXPloitBackend/config/params.py`
- `api/WebXPloitApi/config/params.py`

Ensure that the **WebXPloitApi** is started first.

## How to Run

1. **If you are using the script after C obfuscation and server deployment**:
   ```bash
   /ubuntu/WebXploitBackend> pip install -r requirements.txt
   /ubuntu/WebXploitBackend> python launch.py
   ```

2. **Otherwise**:
   ```bash
   /backend/WebXploitBackend> pip install -r requirements.txt
   /backend/WebXploitBackend> python run.py
   ```

## Unit Test Requirements (for Developers Only)

- Database must be accessible with the following credentials:
  - **IP**: `127.0.0.1`
  - **Username**: `root`
  - **Password**: `''` (empty)
  - **Port**: `3306`

- Joomla repository (versions 4.0.0 to 4.2.7) should be accessible at:
  - [http://localhost/wxplt/joomla_427]

- A valid `.env` file with database credentials should be located at:
  - [http://localhost/wxplt/env/valid]

- Vulnerable Git repository should be available at:
  - [http://localhost/wxplt/git/dumping]
