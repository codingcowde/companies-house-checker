import requests
from bs4 import BeautifulSoup

## replace + or " " with space before comparing with def filter_officers_by_exact_name(name)



class CHeckerScraper():
    def __init__(self) -> None:
        self.url = "https://find-and-update.company-information.service.gov.uk"
        self.query = "/search/officers?q="
        print("Scraper ready.")        

    def search_officers_by_name(self, name) -> list:
        """ gets the search results from the company house by name
            and returns a list of BeautifulSoup Objects
        """ 
        name = name.replace("+", "%20").replace(" ", "%20")
        # search request url
        search_request = self.url+self.query+name
        # get the search result as html
        search_result_html = requests.get(search_request)
        # parse result
        parser = BeautifulSoup(search_result_html.content, "html.parser")
        return article_results.find_all("li", class_="type-officer") if (article_results := parser.find(id="services-information-results")) else []

    def prepare_name(self, name) -> str:
        """ The last name in the directory profile is written in uppercase letters
            this function prepares the name for filter_officers_by_exact_name
        """        
        tmp_names = name.split("+")
        tmp_names[-1] = tmp_names[-1].upper()
        return " ".join(tmp_names)

    def filter_officers_by_exact_name(self, name:str, officers:list) -> BeautifulSoup:
        """ filters the search results from search_officers_by_name()
            and returns the link to the first discovered Profile that 
            matches exact the name, as a BeautifulSoup Object
        """ 
        name = self.prepare_name(name)
        for officer in officers:        
            if link := officer.find("a", text=name):
                return link
        # return false if nothing goes            
        return False

        

    def get_profile_by_officer(self,profile_link) -> BeautifulSoup:
        """ get's the directors profile using the link obtained by 
            filter_officers_by_exact_name()    
        """
        ###get the link from the filtered officers <a href>
        href = profile_link['href']
        # get a response
        response = requests.get(self.url+href)
        # parse result
        parser = BeautifulSoup(response.content, "html.parser")  
        profile = parser.find(id="content-container")
        for l in profile: 
            if l == ", '\n',":
                l = ""

        return profile

    def fix_links(self, html:BeautifulSoup) -> BeautifulSoup:
        """ as all links in results are relative, we have to fix them somehow
            adds the base url to all links
        """
        if html.has_attr('href'):
            link = html['href']
            html['href'] = self.url + link
        for a in html.find_all('a'):
            link = a['href']
            a['href'] = self.url+link
        return html


    def run(self, name) -> dict: 
        officers = self.search_officers_by_name(name)
        result = {}
        if filtered := self.filter_officers_by_exact_name(name, officers):
            # get the profile
            profile = self.get_profile_by_officer(filtered)
            profile = profile.find_next("div", class_="appointments")     
            #fill the dict
            result["html"] = self.fix_links(profile)
            result["text"] = profile.text.strip()
            result["link"] = self.fix_links(filtered)           
        else:
            result = False             
        return result

