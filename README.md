# companies-house-checker
Checks the UK's  Companies House Register for Director Appointments in the user's name.

This is a small django app, that utilizes BeautifulSoup4 to scrape the Companies House's Directors Register, in order to find out if they have been appointet director of a phony company. Users can subscribe, unsubcribe and export their data. It ispossible to register several users with the same email address. 

Deleteing data for one email address removes all entrys from the database, which are connected to this email address.

