#I found this while looking for a way to deal with token authentecation for timing
#out with website requests

#We can't use it now but it may come in handy
#https://stackoverflow.com/questions/28771174/scrapy-scraped-website-authentication-token-expires-while-scraping
# override Request object in order to set new authorization token into the header when the token expires
authorization_token = None

class AuthTokenRequest(Request):
    @property
    def headers(self):
        global authorization_token
        return Headers({'Authorization': 'BEARER {}'.format(authorization_token)}, encoding=self.encoding)

    @headers.setter
    def headers(self, value):
        pass

def error_handler(self, failure):
    global authorization_token
    status = failure.value.response.status
    if status == 401:
        form_data = {'grant_type': 'assertion', 'assertion_type': 'public', 'client_id': 'WDPRO-MOBILE.CLIENT-PROD'}
        auth_site_request = requests.post(url=AUTHORIZATION_URL, data=form_data)
        auth_site_response = json.loads(auth_site_request.text)
        disney_authorization_token = '{}'.format(auth_site_response['access_token'])

        yield failure.request

def start_requests(self):
    form_data = {'grant_type': 'assertion', 'assertion_type': 'public', 'client_id': 'WDPRO-MOBILE.CLIENT-PROD'}
    return [FormRequest(url=AUTHORIZATION_URL, formdata=form_data,
                        callback=self.start_first_run)]

def start_first_run(self, response):
    self.handle_auth(response)
    return self.request_ride_times()

def handle_auth(self, response):
    global authorization_token

    data = json.loads(response.body)

    # get auth token
    authorization_token = '{}'.format(data['access_token'])

def request_ride_times(self):
    # note: this probably isn't really necessary but it doesn't hurt (all the sites we are scraping are in EST)
    now = get_current_time_for_timezone("US/Eastern")

    # get ending timeframe for scraping dates - 190 days out
    until = now + SCRAPE_TIMEFRAME

    for filter_type in FILTER_TYPES:
        filter_url_query_attr = '&filters={}'.format(filter_type)

        scrape_date = now

        while scrape_date <= until:
            url = urljoin(SCRAPE_BASE_URL,
                          '{}{}&date={}'.format(SCRAPE_BASE_URL_QUERY_STRING,
                                                filter_url_query_attr, scrape_date.strftime("%Y-%m-%d")))
            yield AuthTokenRequest(url, callback=self.parse_ride_times, errback=self.error_handler, dont_filter=True,
                                meta={"scrape_date": scrape_date})

            scrape_date += timedelta(days=1)

def parse_ride_times(self, response):
    # parse json data
    data = json.loads(response.body)
    # process data...
