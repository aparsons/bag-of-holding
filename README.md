# Bag of Holding

The **Bag of Holding** is an application to assist in the organization and prioritization of software security activities.

Check out these talks which cover building your own AppSec pipeline:
* [Matt Tesauro - Taking AppSec to 11: Pipelines, DevOps and making things better](https://www.youtube.com/watch?v=LfVhB3EiDDs)
* [Aaron Weaver - Building An AppSec Pipeline: Keeping Your Program, And Your Life, Sane](https://www.youtube.com/watch?v=1CDSOSl4DQU)
* [Matt Tesauro - Lessons From DevOps: Taking DevOps Practices Into Your AppSec Life](https://www.youtube.com/watch?v=tDnyFitE0y4)

## Releases

For information about **what's new** as well as **known issues**, see [RELEASES.md](RELEASES.md)

## Development Setup

For information on setting up a development environment, see [INSTALL.md](INSTALL.md).

## Commands

#### ThreadFix
The following command will retrieve the latest metrics from ThreadFix for connected applications. We recommend this be run daily as a Cron job.

```
python manage.py cron --threadfix
```

## License

* [Licensed under the Apache License, Version 2.0](LICENSE.md).
