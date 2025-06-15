import pyhtml
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
        <h3 style="text-align: center;">Top 3 region with the most site</h3>
    """


    # sql for region with the most site
    sql_query = """
    SELECT Region, COUNT(Site) AS site_count
    FROM Location
    GROUP BY Region
    ORDER BY site_count DESC
    LIMIT 3;
 
    """
    results = pyhtml.get_results_from_query("database/BOM2.db",sql_query)


    if results:
        for row in results:
            page_html += f"""  
        <p style="text-align: center;">{row}</p>"""
    
    # data range
    page_html += """<body>
        <h3 style= "text-align: center;">Our data range for both station AAT and AET</h3>
    """
    sql_query3 = """SELECT MIN(DMY) AS oldest_date, MAX(DMY) AS newest_date
    FROM (
    SELECT DMY FROM AAT WHERE DMY IS NOT NULL
    UNION ALL
    SELECT DMY FROM AET WHERE DMY IS NOT NULL
    );
    """

    results3 = pyhtml.get_results_from_query("database/BOM2.db",sql_query3)
    if results3:
        for row in results3:
            page_html += f"""  
        <p style="text-align: center;">{row}</p>"""

    # Top 3 day with max temp in AAT
    page_html += """
    <body>
        <h3 style="text-align: center;">Top 3 day with the highest temperature in AAT</h3>
        <p style= "text-align: center;">Read by (Site, Date, Min Temperature, Max Temperature</p>
    """
            
    sql_query1 = """SELECT Location, DMY, MinTemp, MaxTemp
    FROM AAT
    WHERE MaxTemp IS NOT NULL
    ORDER BY MaxTemp * 1.0 DESC
    LIMIT 3;
        """
    results1 = pyhtml.get_results_from_query("database/BOM2.db",sql_query1)
    if results1:
        for row in results1:
            page_html += f"""  
        <p style="text-align: center;">{row}</p>"""
            
            
    # Top 3 day with max temp in AET
    page_html += """ 
    <body>
        <h3 style="text-align: center;">Top 3 day with the highest temperature in AET</h3>
        <p style= "text-align: center;">Read by (Site, Date, Min Temperature, Max Temperature</p>
    """
            
    sql_query2 = """SELECT Location, DMY, MinTemp, MaxTemp
    FROM AET
    WHERE MaxTemp IS NOT NULL
    ORDER BY MaxTemp * 1.0 DESC
    LIMIT 3;
        """
    results2 = pyhtml.get_results_from_query("database/BOM2.db",sql_query2)
    if results2:
        for row in results2:
            page_html += f"""  
        <p style="text-align: center;">{row}</p>"""



            

    page_html += """
        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
        <p style="text-align: center;">Data covered our website</p>
        <img src="images/data snapshot.png" style="width: 30%; height: auto; display: block; margin: 0 auto;">
    </body>
    </html>
    """
    return page_html