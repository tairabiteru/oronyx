# Oronyx - Cron for humans
Oronyx is a little scheduling library I wrote that allows you to run things on a schedule using easy to understand, human readable strings.

## How it works
Oronyx is based around the concept something internally referred to as a *future*. A future is exactly what it sounds like: some point in the future. Oronyx accomplishes this with schedulers; functions that interpret a "cron string" and apply their logic to a *now*. The application of this logic to a now will result in a future. Oronyx schedulers as a rule must **always** return a future. That is, the following case:
```Python
now < future
```
Must always be true.

As an example:
```Python
import datetime
import oronyx

# August 8th 2025 at midnight
now = datetime.datetime(2025, 8, 26, 0, 0, 0)

future = oronyx.get_future(now, "every 30 minutes")

# August 8th 2025, 30 minutes after midnight
assert future == datetime.datetime(2025, 8, 26, 0, 30, 0)
```
## Installation
Requires Python >=3.10:
```
pip install git+https://github.com/tairabiteru/oronyx.git
```
## FAQ
- **Why?**
  - The primary reason I wrote this is because existing scheduling libraries out there won't work for my use case. To be clear, I'm not blaming nor condemning any of them, there's plenty of good ones out there. It's just...time is complicated, man.

    Oronyx's outward facing purpose is to produce "futures" from "nows" given English, and the reason I wanted that is ultimately to incorporate into [Elysia](https://github.com/tairabiteru/elysia), a bot designed to nag me into doing chores. The "time strings" need to be easy to understand because ultimately, this is a part of the bot that's public facing. You shouldn't need to be a programmer to create a task for her to remind you of.
    
    But looking under the hood of oronyx, you'll find a framework that allows you to apply this logic to almost any English sentence like this. *That's the point*. Easy to interpret English is ***a*** goal, but a broader goal is being able to apply this concept to new formats of "time string" moving forward.
- **What's the name mean?**
  - [Oronyx](https://honkai-star-rail.fandom.com/wiki/Oronyx) is the titan of ***time*** from Honkai: Star Rail. 

