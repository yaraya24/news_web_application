from django.core.management.base import BaseCommand
from news.models import NewsOrganisation, Category


class Command(BaseCommand):
    help =  """
            Command that will seed the required intial data for 
            the application including News Organisations and Categories
            """

    def handle(self, *args, **kwargs):
     
        categories = [
            'General',
            'Sports',
            'Technology',
            'Business',
            'Culture'
        ]
        NewsOrgs = [
            {
                'name' : 'The Guardian',
                'domain' : 'www.theguardian.com/international'
            },
            {
                'name' : 'The Conversation',
                'domain' : 'www.theconversation.com/global'
            },
             {
                'name' : 'NPR',
                'domain' : 'www.npr.org'
            },
             {
                'name' : 'Reuters',
                'domain' : 'https://www.reuters.com'
            },
            
        ]

        for category in categories:
            Category.objects.create(name=category)

        for News in NewsOrgs:
            NewsOrganisation.objects.create(name=News['name'], domain=News['domain'])

