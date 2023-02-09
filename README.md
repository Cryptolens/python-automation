# python-automation

## Getting started

There are two ways of running the scripts in this repository. Either you can use the pre-compiled binaries (Windows, Mac) or run it in Python. We cover the way it can run in Python below:

### Using pre-compiled binaries

As an example, to run the "block_expired_licenses" binaries, you can call it as follows on Windows:

```
block_expired_licenses.exe -t tokenHere -p productIdhere -b
```

or on Mac:

```
./block_inactive_licenses -t tokenHere -p productIdhere -b
```

You can add "-h" parameter to see more info and tips on how to use a script, i.e.

```
./block_inactive_licenses -h
```

### Using Python

In console/cmd, run the command below to install all required packages.

```
pip install -r requirements.txt
```

You can then call one of the scripts in this folder to perform an automation task.

> If you already have `licensing` package installed in your environmment, you may need to update it to the latest version. This script requires v_39 or above.
