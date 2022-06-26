# Applifting Task

## Development
0. Clone the repository:
```Bash
git clone git@github.com:kappyn/applifting-task.git
```

1. Setup the environment:
```Bash
python -m venv venv
source venv/bin/activate
```
2. Install pip packages:
```Bash
pip install -r requirements-dev.txt
pip install -r requirements.txt
```
3. Build the containers using:
```Bash
docker-compose up --build
```
Multiple containers will start. The API will be available at [`http://localhost:8000`](http://localhost:8000). 

## Testing

To run tests in a separate, non-persistent container, run the following script:
```Bash
bash run-tests clean
```