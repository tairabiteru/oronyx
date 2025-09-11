# Oronyx - Cron for humans
Oronyx is a little scheduling library I wrote that allows you to run things on a schedule using easy to understand, human readable strings.

## How it works
Oronyx is based around the concept of a *timeline*, a special object which acts as a (mostly) infinite iterable. Let's lead by example:
```Python
import datetime
import oronyx

# Aug 26th, 2025 @ 12:00 AM
now = datetime.datetime(2025, 8, 26, 0, 0, 0)
timeline = oronyx.get_timeline(now, "every 30 minutes")

assert timeline[0] == datetime.datetime(2025, 8, 26, 0, 30, 0)
```
Oronyx conflates the idea of a timeline and a list. That is, a timeline is sort of like a list which can be stepped through. So the "0th" element of a timeline is the next occurance of the timeline. In our example, 30 minutes after the reference time.

When a timeline is created, it has a function which is capable of answering the question "when is the next occurrence?" And thus, a timeline solves the problem of finding the next occurrence, and the one after that, and the one after that. It solves it for every occurance for now, to the heat death of the universe. (You're out of luck after that)

However, that's not all. Via Python's ability to have lists take negative indicies, Oronyx can also look back in time. Whereas a negative index in Python is a shorthand for iterating backwards through a list, in Oronyx, a negative index refers to occurrences of the past. Thus:
```Python
now = datetime.datetime(2025, 8, 26, 0, 0, 0)
timeline = oronyx.get_timeline(now, "every 30 minutes")

assert timeline[-1] == datetime.datetime(2025, 8, 25, 23, 30, 0)
```
The -1st element refers to the previous occurrence to the reference date. The -2nd, to the one before that, and so on.
## Installation
Requires Python >=3.10:
```
pip install git+https://github.com/tairabiteru/oronyx.git
```
## FAQ
- **Why?**
  - The primary reason I wrote this is because existing scheduling libraries are a difficult sell for my use case. To be clear, I'm not blaming nor condemning any of them, there's plenty of good ones out there. It's just...time is complicated, man.

    Oronyx got its start as a small library to obtain "futures" for [Elysia](https://github.com/tairabiteru/elysia), a bot designed to nag me into doing chores. It used a similar logic, but only solved the problem for "future" occurrences. But one day, I found myself programming around the concept of a "task," an object with some due date, and a similar English string to denote some time *BEFORE* which one should be notified of the task. I initially wanted to solve this problem with Oronyx, but of course, I couldn't: Oronyx dealt exclusively with "futures" and I was looking for a way to determine the past. 
    
    Thus, I set out to rewrite Oronyx to allow this. I messed around with having different functions which allow the creation of "pasts" instead of "futures" with time strings, but it never seemed quite right to me. Finally, late one evening, it hit me: rather than separate pasts and futures, unite them under one concept: a timeline. Oronyx in its current form, was born.

    Oronyx's original purpose is to allow easy to understand English scheduling of chores, but looking under the hood of oronyx, you'll find a framework that allows you to apply this logic to almost any English sentence like this. *That's the point*. Easy to interpret English is ***a*** goal, but a broader goal is being able to apply this concept to new formats of "time string" moving forward.
- **What's the name mean?**
  - [Oronyx](https://honkai-star-rail.fandom.com/wiki/Oronyx) is the titan of ***time*** from Honkai: Star Rail. 

