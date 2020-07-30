import scrapy
from json import loads
import os
import csv

class RsoSpider(scrapy.Spider):
    # Extracts data for every RSO. Must have a populated all-links.txt file.
    # Must delete all-rso.csv and clear out .all-fail.txt!

    name = "rso"

    if os.path.exists('all-links.txt'):
        all_links = open("all-links.txt", "r").read().split('\n')
    else:
        all_links = []

    start_urls = [f'https://callink.berkeley.edu{linkdir}' for linkdir in all_links] # FIXME

    def parse(self, response):
        json_raw = response.css('script::text').getall()[1]
        
        rso_key = response.url.split('/')[-1]
        if "window.initialAppState" not in json_raw[0:25]:
            filename = f"./thescrape/fail-jsons/FAIL-{rso_key}.json"
            with open("./thescrape/fail-jsons/.all-fail.txt", 'a') as f:
                f.write(rso_key + '\n')
                f.close()

        jload: dict = loads(json_raw[25:-1])['preFetchedData']
        # filename = f"./thescrape/rso_jsons/rso-{rso_key}.json"

        fields: dict = {
            "id": jload['organization'].get('id', ''),
            "fullname": jload['organization'].get('name', ''),
            "keyname": jload['organization'].get('websiteKey', ''),
            "rso_email": jload['organization'].get('email', ''),
            "description": jload['organization'].get('description', ''),
            "summary": jload['organization'].get('summary', ''), # FIXME may need to scan for "Grant applications page"
            "active_status": jload['organization'].get('status', ''),
            "start_date": jload['organization'].get('startDate', ''),
            "end_date": jload['organization'].get('endDate', ''),
            "status_change_date": jload['organization'].get('statusChangeDateTime', ''),
            "callink_type_id": jload['organization'].get('organizationTypeId', ''),
            "callink_type_name": jload['organization']['organizationType'].get('name', ''),
            "social_web": jload['organization']['socialMedia'].get('externalWebsite', ''), 
            "social_insta": jload['organization']['socialMedia'].get('instagramUrl', ''), 
            "social_fb": jload['organization']['socialMedia'].get('facebookUrl', ''), 
            "social_twitter": jload['organization']['socialMedia'].get('twitterUrl', ''), 
            "social_linkedin": jload['organization']['socialMedia'].get('linkedInUrl', ''), 
            "social_flickr": jload['organization']['socialMedia'].get('flickrUrl', ''),
            "social_gcal": jload['organization']['socialMedia'].get('googleCalendarUrl', ''),
            "social_youtube": jload['organization']['socialMedia'].get('youtubeUrl', ''),
            "social_callink": response.url,
            "callink_profile_pic": jload['organization'].get('profilePicture', ''),
            "priv_privacy": jload['organization']['primaryContact'].get('privacy', ''),
            "priv_firstname": jload['organization']['primaryContact'].get('firstName', ''),
            "priv_prefname": jload['organization']['primaryContact'].get('preferredFirstName', ''),
            "priv_lastname": jload['organization']['primaryContact'].get('lastName', ''),
            "priv_email": jload['organization']['primaryContact'].get('primaryEmailAddress', ''),
            "priv_prefname": jload['organization']['primaryContact'].get('preferredFirstName', ''),
            "priv_phone": jload['organization']['contactInfo'][0].get('phoneNumber', ''),
            # exploratory data; they are all the same! Exclude.
            # "institution_id": jload['organization'].get('institutionId', ''),
            # "community_id": jload['organization'].get('communityId', ''),
        }

        file_exists = os.path.isfile("all-rso.csv")
        with open ("all-rso.csv", 'a') as csvfile:
            headers: list = fields.keys() 
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers
            )

            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header

            writer.writerow(fields)



