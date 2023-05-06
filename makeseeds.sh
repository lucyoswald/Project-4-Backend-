python manage.py dumpdata posts --output posts/seeds.json --indent=2;
python manage.py dumpdata comments --output comments/seeds.json --indent=2;
python manage.py dumpdata jwt_auth --output jwt_auth/seeds.json --indent=2;