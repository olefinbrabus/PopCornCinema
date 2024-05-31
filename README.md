# PopCornCinema
## http://popcorncinema.website/

## About The App
Cinema service for booking and watching the latest movies
using the Django framework 

## Features
- Admin Panel
- Cart through a user session without authentication
- creating a ticket reservation
- downloading tickets to a pdf file with a barcode

## Technologies
- Python 3.9 
- Django 4.2.8
- Bootstrap 
- Jquery
- AJAX
- POSTGRESQL
- Amazon Ec2

## Home Page
![plot](PopCornCinema/demo_img/demo_img1.png)
## Catalog of films
![plot](PopCornCinema/demo_img/demo_img2.png)
## Films
![plot](PopCornCinema/demo_img/demo_img3.png)
## Selection of tickets
![plot](PopCornCinema/demo_img/demo_img4.png)
## Cart
![plot](PopCornCinema/demo_img/demo_img5.png)
## Pdf file order
![plot](PopCornCinema/demo_img/demo_img6.png)



## Installing the application via Github
```bash
git clone  https://github.com/olefinbrabus/PopCornCinema
cd PopCornCinema
python -m venv venv
pip install -r requirements.txt
```

## Setting environment keys:
- Rename the File Sample.env to .env
- Enter the values you need in the keys

## Launching the application through a local server
```bash
python manage.py runserver 127.0.0.1:8000
```

## Launching an application via Docker
```bash
docker-compose build
docker-compose up
```
