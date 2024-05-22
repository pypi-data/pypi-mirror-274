import scrapy
import json
import re

class AsunnotrentapispiderSpider(scrapy.Spider):

    name = "asunnotrentapispider"
    base_url = "https://asunnot.oikotie.fi/vuokra-asunnot?pagination={}&cardType=101"

    def __init__(self, page_limit=10, *args, **kwargs):
        super(AsunnotrentapispiderSpider, self).__init__(*args, **kwargs)
        self.page_limit = int(page_limit)
        self.current_page = 1
        self.start_urls = [self.base_url.format(self.current_page)]

    def parse(self, response):
        # Extract necessary tokens from the page content
        ota_cuid = response.xpath('//meta[@name="cuid"]/@content').get()
        ota_token = response.xpath('//meta[@name="api-token"]/@content').get()
        ota_loaded = response.xpath('//meta[@name="loaded"]/@content').get()

        # Extract cookies
        cookies = response.headers.getlist('Set-Cookie')
        cookies_dict = {}
        for cookie in cookies:
            cookie_parts = cookie.decode().split(';')[0].split('=')
            cookies_dict[cookie_parts[0]] = cookie_parts[1]
        url = response.url

        # Prepare headers for the API request
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Ota-Cuid': ota_cuid,
            'Ota-Loaded': ota_loaded,
            'Ota-Token': ota_token,
            'Pragma': 'no-cache',
            'Priority': 'u=1, i',
            'Referer': url,
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Model': '""',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        offset = (self.current_page - 1) * 24

        api_url = f'https://asunnot.oikotie.fi/api/search?cardType=100&limit=24&offset={offset}&sortBy=published_sort_desc'

        yield scrapy.Request(url=api_url, headers=headers, cookies=cookies_dict, callback=self.parse_api, cb_kwargs={"url":url})

    def parse_api(self, response, url= None):

        data = response.json()

        for item in data['cards']:  # Adjust this according to the actual JSON structure
            link = item.get('url')
            
            headers ={
                'referer' : url
            }

            yield scrapy.Request(url = link, callback = self.parse_property,headers=headers)

        # Handle pagination
        if self.current_page < self.page_limit:
            self.current_page += 1
            next_page_url = self.base_url.format(self.current_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_property(self,response):

        property_info = {}
        
        property_info['source'] = response.url

        if 'vuokra' in property_info['source']:

            property_info['property_listing_type'] = 'rent'

        else:

            property_info['property_listing_type'] = 'sell'

        property_info['property_is_new_construction'] = False

        try:

            property_info['property_description'] = " ".join(response.css('div.listing-overview p::text').getall())
        except:

            pass
        
        try:
            property_info['property_floor_number'] = re.search(r'\d+', response.css('dt:contains("Kerros") + dd::text').get()).group() if response.css('dt:contains("Kerros") + dd::text').get() else None
        
        except:
            pass

        try:
            property_info['property_layout'] = response.css('dt:contains("Huoneiston kokoonpano") + dd::text').get()

        except:
            pass

        try:
            property_info['property_condition'] = response.css('dt:contains("Kunto") + dd::text').get()

        except:
            pass

        try:
            property_info['property_kitchen_features'] = response.css('dt:contains("Keittiön varusteet") + dd::text').get()
        
        except:
            pass

        try:
            property_info['property_bathroom_features'] = response.css('dt:contains("Kylpyhuoneen varusteet") + dd::text').get()

        except:
            pass

        try:
            property_info['property_renovation_info'] = response.css('dt:contains("Tehdyt remontit") + dd::text').get()

        except:
            pass

        try:
            property_info['property_additonal_terms'] = response.css('dt:contains("Muut ehdot") + dd::text').get()
        except:
            pass

        try:
            property_info['property_sauna'] = response.css('dt:contains("Taloyhtiössä on sauna") + dd::text').get()

        except:
            pass

        try:
            property_info['property_heating'] = response.css('dt:contains("Lisätietoja lämmityksestä") + dd::text').get()

        except:
            pass

        try:
            image_urls = response.css('div.tabs-content a::attr(href)').getall()
            filtered_image_urls = [url for url in image_urls if url.startswith('https://cdn.asunnot.oikotie.fi/')]

            property_info['media_set'] = filtered_image_urls

        except:
            pass

        # Iterate through each script tag
        for script_text in response.css("script::text").getall():
            # Check if the script text contains 'analytics'
            if 'analytics' in script_text:
                # Extract JSON data from the script
                json_data = script_text.split("window.page=")[0].strip().rstrip(';')[script_text.split("window.page=")[0].strip().rstrip(';').find('{'):]
                json_data = json.loads(json_data)
                
                # Populate property_info dictionary with extracted data
                property_info['cardid'] = json_data['analytics']['cardId']
                property_info['property_housing_type'] = json_data['analytics']['apartmentType']
                property_info['address_full'] = json_data['address']
                property_info['property_living_area_sqm'] = json_data['analytics']['size']
                property_info['property_rental_price'] = json_data['analytics']['price']
                property_info['timeline_advertisement_creation'] = json_data['analytics']['published']
                try:

                    property_info['address_postal_code'] = json_data['analytics']['zipCode']

                except KeyError:

                    property_info['address_postal_code'] = None
                    
                property_info['property_construction_year'] = json_data['analytics']['apartmentBuildYear']
                
                # Break the loop after finding the relevant script
                break
        
        match = re.match(r'^(.*?)(\d+)(.*)\,', property_info['address_full'])
        if match:
            property_info['address_street'] = match.group(1).strip()
            property_info['address_house_number'] = match.group(2).strip()
            property_info['address_addition'] = match.group(3).strip()
        else:
            property_info['address_street'] = re.match(r'^([^,]*)', property_info['address_full'])[0].strip()

        # Iterate through each script tag again to find additional data
        for script_text in response.css("script::text").getall():
            # Check if the script text contains additional data (assuming it has 'numberOfRooms' and 'geo' keys)
            if 'numberOfRooms' in script_text and 'geo' in script_text:
                # Extract JSON data from the script
                json_data_1 = json.loads(script_text)
                
                # Populate property_info dictionary with additional data
                property_info['property_rooms_amount'] = json_data_1['numberOfRooms']
                property_info['latitude'] = json_data_1['geo']['latitude']
                property_info['longitude'] = json_data_1['geo']['longitude']
                property_info['address_country'] = json_data_1['address']['addressCountry']
                # Break the loop after finding the relevant script
                break

        yield property_info
