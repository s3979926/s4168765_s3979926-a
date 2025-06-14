def get_page_html(form_data):
    print("About to return page home page...")
    page_html="""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Database Web-App Demo</title>
    </head>
    <body>
        <h1 style="text-align: center;">Weather Website</h1>
        <p style= "text-align: center;">Our website aim to help user know more about their weather and to have better choice</p>
        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
        <img src="images/data snapshot.png" style="width: 30%; height: auto; display: block; margin: 0 auto;">
    </body>
    </html>
    """
    return page_html