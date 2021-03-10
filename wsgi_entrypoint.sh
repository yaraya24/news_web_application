#!/bin/sh

until cd /backend
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done
until ./manage.py seed_initial_data
do 
    echo "populating db..."
done
until cd news_scraper
do
    echo "Getting ready to retrieve articles"
done


until scrapy crawl guardian_spider
do
    echo "retrieving articles from The Guardian"
done

until scrapy crawl conversation_spider
do
    echo "retrieving articles from The Conversation"
done

until scrapy crawl npr_spider
do
    echo "retrieving articles from NPR"
done
until scrapy crawl reuters_spider
do
    echo "retrieving articles from Reuters"
done
cd /backend


gunicorn news_app_project.wsgi --bind 0.0.0.0:8000 --workers 2