# Mission to Mars - Web Scraping Challenge

In this challenge, we scrape several different websites about mars and compile a single website that can be updated with the latest data.  The following files work together to produce the webpage:

1.  In a CLI, we run the python program **app.py**.  
    * This is a Python program that uses Flask to create routes for our webpage and connects to our MongoDB.
    
2.  Next, navigate to the URL produced in the CLI when app.py is run (http://127.0.0.1:5000/).  
    * The website at **Index.HTML** initially only displays the section headings and the button to initiate the scrape.

3.  Click the "Scrape New Data" button.  **App.py** runs the functions in the **scraping.py** file based on the defined scrape route   
    *  **Scraping.py** scrapes the webpages using the Chrome Extension and compiles the data into our MongoDB.  
    *  **Index.HTML** file renders the page using HTML, Flask, Boostrap and MongoDB data.
    * **Scraping.py** was created using exported code from our Jupyter Notebook code in **Mission_to_Mars_Challenge.ipynb**.  We utilize the Jupyter Notebook so we can test our code prior to putting it into a Python program.
