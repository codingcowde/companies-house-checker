# companies-house-checker
Checks the UK's  Companies House Register for Director Appointments in the user's name.

This is a small django app, that utilizes BeautifulSoup4 to scrape th Companies House. Users can subscribe, unsubcribe and export theri data. It ispossible to register several users with the same email address. 

Deleteing data for one email address removes all entrys from the database, which are connected to this email address.

