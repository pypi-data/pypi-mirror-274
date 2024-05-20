# Process Scheduler

A python implementation of a cron job scheduler.

## 1. Install from source then activate venv

Install `venv` to set up your virtual environment
```bash
pip install --upgrade pip setuptools wheel venv
```

Go to project root and create your virtual environment
```bash
cd <PROJECT_ROOT>
python -m venv venv
```

Activate your virtual environment
```bash
.\venv\Scripts\activate
```

Install project dependencies
```bash
pip install -r requirements.txt
```

Install module locally, so you can import it as a module
```bash
pip install -e .
```

## 2. Run it

First install from source (see above), then define your configuration in a YAML file
```yaml
loopRefreshSeconds: 15
maxWorkers: 10
schedulerLogDir: "C:\\Desktop\\apps\\process-scheduler\\logs\\scheduler"
processLogDir: "C:\\Desktop\\apps\\process-scheduler\\logs\\process"
processes:
  - id: test-job
    cron: "0 7 * * mon"                          # == 7:00 AM every Monday
    command: "python C:\\Desktop\\my-process.py" # Invoke my python script
    runAtStartup: true                           # Run immediately when scheduler starts, then follow cron definition
```

Run it
```bash
python -m process-scheduler C:\\Desktop\\config.yaml
```

## 3. Test

TODO

## 4. Build and upload

Install dependencies

```bash
pip install --upgrade setuptools wheel build twine
```

Build the package (wheel and sdist)
```bash
python -m build 
```

Ensure `.pypirc` in user folder is correct, then upload
```bash
twine upload dist/*
```
