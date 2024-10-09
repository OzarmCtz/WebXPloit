# Project Overview: `obf_in_c`

The `obf_in_c` directory is designed to **obfuscate** the backend and API by converting them into C for secure production deployment on a server.

## Prerequisites

Ensure that **Microsoft Visual C++** and **Python 3.12.0** are installed before proceeding.

Before proceeding with the following steps, configure the two parameter files:
- `backend/WebXPloitBackend/config/params.py`
- `api/WebXPloitApi/config/params.py`

## Installation and Build Steps

Once the configuration is set, follow these steps to build and obfuscate the backend and API:

### 1. Navigate to the `obf_in_c` Directory

From the root directory of the project, navigate to the `obf_in_c` folder:
```bash
/obf_in_c> python setup.py
``` 

### 2. Navigate to the `WebXploitBackend` Directory

Move into the `WebXploitBackend` directory:
```bash
/obf_in_c> cd WebXploitBackend
```

### 3. Install Required Dependencies

Install the necessary dependencies for building the backend:
```bash
/obf_in_c/WebXploitBackend> pip install -r requirements_in_c.txt
```

### 4. Build the C Extensions for the Backend

Run the following command to build the C extensions and obfuscate the backend code:
```bash
/obf_in_c/WebXploitBackend> python setup.py build_ext --inplace
```

### 5. Obfuscate the API

Navigate to the `WebXploitApi` directory and build the C extensions for the API:
```bash
/obf_in_c> cd WebXploitApi
/obf_in_c/WebXploitApi> python setup_api.py build_ext --inplace
```
---

## Deployment

Once the build process is complete, follow these steps to deploy both the API and backend. **You must start the API before the backend** for proper functionality.

### 1. API Deployment

1. **Copy the `WebXploitApi` directory** to the production server.

2. **Install required dependencies**:
   ```bash
   /ubuntu/WebXploitApi> pip install -r requirements.txt
   ```

3. **Start the API application**:
   ```bash
   /ubuntu/WebXploitApi> python launch.py
   ```

### 2. Backend Deployment

After starting the API, deploy the backend by following these steps:

1. **Copy the `WebXploitBackend` directory** to the production server.

2. **Install required dependencies**:
   ```bash
   /ubuntu/WebXploitBackend> pip install -r requirements.txt
   ```

3. **Start the backend application**:
   ```bash
   /ubuntu/WebXploitBackend> python launch.py
   ```

