## how to use

```bash
$ docker build . -t auto_submit_daily_report
$ docker run -it --rm -v [LOCAL_REPORT_DIRECTORY]:/user/src/app/report:ro auto_submit_daily_report report/[REPORT_FILE] [YOUR_NAME]
```
