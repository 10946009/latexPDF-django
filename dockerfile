FROM sd030/ubuntu-latex:latest
# run django manage.py runserver

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8080"]