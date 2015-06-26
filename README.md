# Bag of Holding

The **Bag of Holding** is an application security utility to assist in the organization and prioritization of software security activities.

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
