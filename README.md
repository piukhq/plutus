# Plutus 
Plutus is a service for facilitating communication between Harmonia and our data warehouse.
Reads Harmonia's audit logs from a message queue, translates the data to a format required by the data warehouse and
puts it onto another queue. 

### Pre-requisites
* Python >= 3.10
* [poetry](https://python-poetry.org/docs/master/) 

### Configuration
Project configuration is done through environment variables. A convenient way
to set these is via the `.env` file in the project root. See `settings.py` for
configuration options that can be set in this file.

Your code editor should support loading environment variables from the `.env`
file either out of the box or with a plugin. For shell usages, you can have poetry
automatically load these environment variables by using
[poetry-dotenv-plugin](https://github.com/mpeteuil/poetry-dotenv-plugin), or
use a tool like [direnv](https://direnv.net/).

### Running the Project
```bash
python consumer.py
```
The consumer module can be found in the project's root directory.

### Deployment
There is a Dockerfile provided in the project root. Build an image from this to
get a deployment-ready version of the project.

### Unit Tests
```bash
pytest tests
```
Tests will be autodiscovered.