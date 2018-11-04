# slack-progress

[![PyPI version](https://badge.fury.io/py/slack-progress.svg)](https://badge.fury.io/py/slack-progress)

A realtime progress bar for Slack

![screencap][screencap]

![screencap-full][screencap-full]

## Installing

```bash
pip install slack-progress
```

## Usage

Create a SlackProgress object with your Slack token and channel name:
```python
from slack_progress import SlackProgress
sp = SlackProgress('SLACK_TOKEN', 'CHANNEL_NAME')
```

Now you can simply wrap any iterator:
```python
for i in sp.iter(range(500)):
    time.sleep(.2)
```

The bar position can also be set manually:

```python
pbar = sp.new() # create new bar where 100% == pos 100
pbar.pos = 10
time.sleep(1)
pbar.pos = 100

pbar = sp.new(total=500) # create new bar where 100% == pos 500
pbar.pos = 100 # 20% complete
time.sleep(1)
pbar.pos = 500 # 100% complete
```

You can add logging messages too:
```python
pbar.pos = 50
pbar.log("Step 1 complete")
pbar.pos = 100
pbar.log("Step 2 complete")
```

The bar can be also rendered always with full width:

```python
sp = SlackProgress('SLACK_TOKEN', 'CHANNEL_NAME', full_width=True)
```

The bar characters (fill and empty) can also be customized:
```python
sp = SlackProgress('SLACK_TOKEN', 'CHANNEL_NAME', full_width=True, fill_char='X', empty_char='_')
```


[screencap]: https://i.imgur.com/cDkKIYW.gif "slack-progress"
[screencap-full]: https://i.imgur.com/UmGFHdI.gif "slack-progress-full"
