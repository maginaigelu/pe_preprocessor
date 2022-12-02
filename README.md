## Webapp cluster for preprocessing PE files via Pyspark

### Deploy: 
*`dependencies: docker>=20.10.21, docker-compose>=1.29.2`

#### Via Makefile:
From project directory:
1. Start: `make build up`
2. Check cluster availability: `make ps`
3. Kill: `make down`
4. More tools: `make list`

#### Via docker-compose:
From project directory:
1. Set compose file env: `export COMPOSE_FILE=./ci/compose/docker-compose.yml`
2. Start: `docker-compose up -d --build`
3. Set migrations: `docker-compose run --rm app bash -c 'alembic upgrade head'`
4. Check cluster availability: `docker-compose ps`
5. Kill: `docker-compose down`

### Use cases:

Use cases are located in `test_main.http` file


#### Refactoring, questions, optimizations:

- Bloom filter from mmh3 file content hashes?
- Database transactions/mutexes/barriers for pyspark?
- Is Pyspark reading S3 list files concurrently?
- Apache hive, hdfs etc. to speed up big data read/write database operations.
- What else I forgot?