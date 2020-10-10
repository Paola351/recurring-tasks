# recurring-tasks
This script reminds you on recurring tasks via email
## Requirements
Python version >= 3.3 is required
## Configuration
Rename `config.ini.template` to `config.ini` and set your email configuration
## Installation
Run `python3 checkTasks.py` as daily cronjob.

Example if you want to run it at 9:00 am:

`00 9 * * * python3 checkTasks.py`
## Usage
Notifications are configured in `tasks.ini`.

There are different task types: daily, weekly, monthly, weekdayofmonth, yearly and free. You can find examples for all types in the file. Don't forget to uncomment the sections (remove ;)
