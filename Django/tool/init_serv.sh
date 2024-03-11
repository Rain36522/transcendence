
echo "Preparing django server"

# while ! psql -U postgres; do
#         sleep 1
#         echo "Wait for postgresql..."
# done
python3 manage.py migrate
python3 manage.py runserver
echo "Start django server"
python3 manager.py runserver 0.0.0.0:8000
