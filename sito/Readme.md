Prima di lanciare il progetto commentare le due righe in app.py (71-72)
avviare con il docker-compose up e dopo avviare le migrazioni con Flask all'interno della Docker.

```
flask db migrate -m "Initial migration."
flask db upgrade
```