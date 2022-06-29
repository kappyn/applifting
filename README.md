# Applifting Task

## Development
1. Clone the repository:
```Bash
git clone git@github.com:kappyn/applifting-task.git
```

2. Setup the environment:
```Bash
python -m venv venv
source venv/bin/activate
```
3. Install pip packages:
```Bash
pip install -r requirements-dev.txt
pip install -r requirements.txt
```
4. Build the containers using:
```Bash
docker-compose up --build
```
Multiple containers will start. The API will be available at [`http://localhost:8000`](http://localhost:8000). 

## Testing

To run tests in a separate, non-persistent container, run the following script:
```Bash
sh run-tests clean
```

## Production

For production environment, configure `.env.prod` file from the given `example.env` template and then run the command:
```Bash
docker-compose -f docker-compose.prod.yml up --build
```

## Demo

You can find an actual preview of this project at [`applifting.kroupa.dev`](https://applifting.kroupa.dev).
