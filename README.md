# Ping Monitor

### Installation

Install dependencies:

`pip install pyyaml`

### Configuration

Create your own YAML configuration file:

`cp config_template.yml config.yml`

### Execution

To run the script:

`python exec.py`

### Schedule

Create a Crontab task:

```cron
# Schedule Pingmonitor
@hourly source ~/.bashrc; cd /home/cetinajero/pingmonitor/; python exec.py > crontab.log 2>&1
```
