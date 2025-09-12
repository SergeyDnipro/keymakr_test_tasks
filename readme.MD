<u>TASK 1</u>

<b>Run application (build docker container and run uvicorn):</b>

 cd task_1<br>
 docker-compose up --build


<b>Run tests inside running docker container:</b> 

docker exec -it fastapi-tasks pytest -v
<br>

<b>Access to Swagger API:</b><br>
http://localhost:8000/docs

<u>TASK 2</u>

<b>Run application (build docker container and run uvicorn, redis, celery workers):</b>

cd task_2<br>
docker-compose up --build<br>

 After launching containers fetching, processing URL, logging and saving to CSV file  (1 minute interval).<br>
http://localhost:8000/fetch forced run celery task. <br>

Log and processed 'csv' file saved to /data
