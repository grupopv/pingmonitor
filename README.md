# Ping Monitor

### Installation

Install dependencies:

```bash
pipenv install
```

### Configuration

Create your own YAML configuration file:

```bash
cp config_template.yml config.yml
```

### Execution

To run the script:

```bash
pipenv run python exec.py
```

### Schedule

Create a Crontab task:

```cron
# Schedule Pingmonitor
@hourly source ~/.bashrc; cd ~/pingmonitor/; pipenv run python exec.py > crontab.log 2>&1
```
