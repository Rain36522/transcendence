source ./test/bin/activate
pip3 install psycopg2-binary
python3 ./test/manage.py migrate
python3 ./test/manage.py runserver