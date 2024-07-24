# Serverless App written in Python
The following is a very simple serverless app, written in Python using Flask. It demonstrates handling http requests
concurrently.

## What is a serverless application?
Serverless applications are web applications running in a cloud environment, where the infrastructure is abstracted from the application,
and the developer focuses on code which handles specific events. Code is written as functions which gets invoked as a response to an event.

Once deployed, the application is invoked as many times as necessary to serve incoming request. 
Serverless applications respond to demand, scaling up and down automatically. The cloud provider is responsible for dynamically allocating
the needed computational resources to scale up and down.

## Requirements
The application receives '/sleep_and_sum' http requests with two integers, responding with their sum.
According to specification, each request should be carried out by a separate process. 

In addition, the app supports two monitoring requests: 
1. '/active_processes' displays the pids (process IDs) of all current workers.
2. '/request_counter' displays the total number of 'sleep_and_sum' requests completed.

## Usage
### Set up the virtual environment
In order to run the application, we'll first need to setup a virtual environment - an enclosed and contained packing of dependencies.
We'll be using venv which is a part of the Python standard library to create a virtual environment:

1. Once you're in the application's directory, to set up a new virtual environment:
```SHELL
python3 -m venv venv
```

2. Activate the virtual environment:
```SHELL
source venv/bin/activate
```

3. Install Flask:
```SHELL
pip install Flask
```

### Running the application
1. If the virtual environment isn't already activated, active it.
2. To run the application run:

```SHELL
python serverless.py
```

3. To run the test, in another terminal activate the virtual environment and run:

```SHELL 
python test.py
```
