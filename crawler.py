import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from sqlalchemy import create_engine
def main_function(txt_req, usr_id):
    def get_source(url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def scrape_google(query):

        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.co.uk/search?q=" + query)

        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        return links
    def get_results(query):
        
        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.co.uk/search?q=" + query)
        
        return response

    def parse_results(response):
        df = pd.DataFrame()
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".VwiC3b"
        
        results = response.html.find(css_identifier_result)

        output_title = []
        output_link = []
        output_link_text = []
        for result in results:
            output_title.append(result.find(css_identifier_title, first=True).text)
            output_link.append(result.find(css_identifier_link, first=True).attrs['href'])
            output_link_text.append(result.find(css_identifier_text, first=True).text)

        df['title']=output_title
        df['link']=output_link
        df['link_text']=output_link_text
        df['usr_id']=usr_id
        df['txt_req']=txt_req
        engine = create_engine('mysql+pymysql://root:12@localhost:3306/NJS', echo = False)
        df.to_sql(name = 'Research_1', con = engine, if_exists = 'append', index = False) 
        
        return df

    def google_search(query):
        response = get_results(query)
        return parse_results(response)

    results = google_search(txt_req)
    print('Nice',results)
    return results
