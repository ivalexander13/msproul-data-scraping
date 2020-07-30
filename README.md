# Data Scraping for Middle Sproul
The source code for scraping UC Berkeley's Callink website, to obtain publicly available information on all ~1400 Registered Student Organizations on campus. 

## Usage
1. Ensure the packages in requirements.txt are installed, and the virtualenv activated.
2. Extract the html from callink.berkeley.edu/organizations, and save the most recent common parent <div> that contains all the organizations' div's. Name this all-cut.html and save it in rso_htmls/, alongside all-cut-sample.html.
3. Fill start_urls in thescrape/spiders/rso_getlinks.py with the absolute path to all-cut.html.
4. At the root, run in a terminal (bash):
    ```bash
    scrapy crawl rso-links
    ```
5. Make sure all-links.txt is present in the root folder, alongside all-links-sample.txt.
6. At the root, run in a terminal (bash):
    ```bash
    scrapy crawl rso
    ```
7. Output file is in the root folder, called all-rso.csv. Enjoy.

## Fun Facts
- Look at the *-sample files to see what the corresponding files should contain.
- Obtaining all-cut.html involves hand-clicking "load more" (a lot). The website disallows bots from sending those button requests and I'm not trying to break any rules.
- The .jsons aren't produced in this version of the script but is very helpful to look at.
- In 2018, someone by the name of Daniel Beadle scraped his high school organization's website that happens to use the same CampusLabs platform as UC Berkeley. You can check it out [here](https://danielbeadle.net/post/2018-04-14-scraping-react-with-python/) 
- The link/dir containing all the orgs is /organizations/, but the one for each org is /organization/XXXXX. Notice the plural v. singular.

## Known Issues
- Currently does not include 40 organizations, for some reason.

## Next Steps
I will clean the data and will link the repo to the script here.
