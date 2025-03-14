# recommender

## project setup

1- inside the project
```
cd recommender
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- create your env
```
cp .env.example .env
```

4- spin off docker compose
```
docker compose -f docker-compose.yml up -d
```
