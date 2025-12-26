# Getting started with AirFlow

---

1. Create a folder and create these directories ```config```, ```dags```, ```logs```, ```plugins```

```bash 
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

```


2. Then we need docker desktop. (refer docs.docker.com to install)
3. Next, download ```docker-compose.yaml``` file of airflow latest release . For more information read. [Running Airflow in Docker &mdash; Airflow 3.1.5 Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
4. Run docker compose

``` bash
 docker compose up airflow-init
 ```  

 5. Once again, run 

 ```bash
docker compose up

 ```

 6. Access web ui at localhost:8080