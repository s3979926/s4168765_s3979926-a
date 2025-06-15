import pyhtml
#def get_page_html(form_data):
    #print("About to return page 2")
    
    #page_html=f"""<!DOCTYPE html>
    #<html lang="en">
    #<head>
        #<title>Reading from a .db file</title>
    #</head>
    #<body>
        #<h1>Page 2B - Example of retrieving data from a .db file...</h1>
    #"""
    #sql_query = "select * from movie;"
    #page_html+= f"<h2>Result from \"{sql_query}\"</h2>"
    
    #Run the query in sql_query and get the results
    #results = pyhtml.get_results_from_query("database/movies.db",sql_query)
    
    #Adding results to the web page without any beautification. Try turning it into a nice table!
    #for row in results:
        #page_html+="<p>"+str(row)+"</p>\n"
    #page_html+="""'''

def get_page_html(form_data):
    print("About to return page 2")

    selected_dmy = form_data.get('dmy')
    ran_min = form_data.get('id_min')
    ran_max = form_data.get('id_max')

    if isinstance(ran_min, list):
        ran_min = ran_min[0]
    if isinstance(ran_max, list):
        ran_max = ran_max[0]
    if isinstance(selected_dmy, list):
        selected_dmy = selected_dmy[0]

    page_html = f"""<!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <title>Filtered Locations</title>
    </head>
    <body>
        <h1>Location Filter</h1>
        <form action="/page2a" method="GET">
            <label for="metric">Metric:</label>
            <select name="metric">
    """

    dmy_query = "SELECT DISTINCT DMY FROM AET ORDER BY DMY;"
    dmy_results = pyhtml.get_results_from_query("database/BOM2.db", dmy_query)
    for row in dmy_results:
        dmy = row[0]
        selecteddmy = ' selected' if selected_dmy == dmy else ''
        page_html += f'<option value="{dmy}"{selected}>{dmy}</option>\n'

    page_html += f"""
            </select><br><br>
            <label for="ran_min">Min ID:</label>
            <input type="text" name="ran_min" value="{ran_min or ''}"><br><br>
            <label for="ran_max">Max ID:</label>
            <input type="text" name="ran_max" value="{ran_max or ''}"><br><br>
            <input type="submit" value="Filter Locations">
        </form>
    """

    if selected_dmy and ran_min and ran_max:
        try:
            ran_min_val = float(ran_min)
            ran_max_val = float(ran_max)
            ran_min_val, ran_max_val = min(ran_min_val, ran_max_val), max(ran_min_val, ran_max_val)

            safe_dmy = selected_dmy.replace("'", "''")

            location_query = f"""
            SELECT Location, DMY, MaxTemp, MinTemp
            FROM AET
            WHERE TRIM(DMY) LIKE '{safe_dmy}' AND CAST(Location AS REAL) BETWEEN {ran_min_val} AND {ran_max_val}
            ORDER BY CAST(Location AS REAL) ASC;
            """

            print("Running query:", location_query)
            results = pyhtml.get_results_from_query("database/BOM2.db", location_query)
            print("Results fetched:", results)

            page_html += f"""
            <h3>Results for {selected_dmy} between latitudes {ran_min_val} and {ran_max_val}</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr><th>Site</th><th>Name</th><th>Region</th><th>Latitude</th></tr>
            """
            for row in results:
                location, dmy, maxtemp, mintemp = row
                page_html += f"<tr><td>{location}</td><td>{dmy}</td><td>{maxtemp}</td><td>{mintemp}</td></tr>"

            page_html += "</table>"
        except ValueError:
            page_html += "<p style='color:red;'>Please enter valid numeric latitude values.</p>"

        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
    </body>
    </html>
    """
    return page_html