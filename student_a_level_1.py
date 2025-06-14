import pyhtml
def get_page_html(form_data):
    print("About to return page home page...")

    # sql for AET lowest temperature
    sql_query = """
    SELECT DMY, Location, MaxTemp, MinTemp
    FROM AET
    WHERE minTemperature = (
        SELECT MIN(minTemperature)
        FROM AET
    );
    """
    results = pyhtml.get_results_from_query("database/BOM2.db",sql_query)


    page_html="""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Database Web-App Demo</title>
    </head>
    <body>
        <h1 style="text-align: center;">Weather Website</h1>
        <p style= "text-align: center;">Our website aim to help user know more about their weather and to have better choice</p>
    """
    if results:
        for row in results:
            page_html += f"""
        <h3 style="text-align: center;">Lowest Temperature Recorded In AET</h3>
        <p style="text-align: center;">{row}</p>"""

    page_html += """
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