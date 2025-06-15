import pyhtml

def get_page_html(form_data):
    print("About to return page 2")

    selected_state = form_data.get('state')
    lat_min = form_data.get('lat_min')
    lat_max = form_data.get('lat_max')

    if isinstance(lat_min, list):
        lat_min = lat_min[0]
    if isinstance(lat_max, list):
        lat_max = lat_max[0]
    if isinstance(selected_state, list):
        selected_state = selected_state[0]

    page_html = f"""<!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <title>Filtered Locations</title>
    </head>
    <body>
        <h1>Location Filter</h1>
        <form action="/page2a" method="GET">
            <label for="state">State:</label>
            <select name="state">
    """

    state_query = "SELECT DISTINCT State FROM Location ORDER BY State;"
    state_results = pyhtml.get_results_from_query("database/BOM2.db", state_query)
    for row in state_results:
        state = row[0]
        selected = ' selected' if selected_state == state else ''
        page_html += f'<option value="{state}"{selected}>{state}</option>\n'

    page_html += f"""
            </select><br><br>
            <label for="lat_min">Min Latitude:</label>
            <input type="text" name="lat_min" value="{lat_min or ''}"><br><br>
            <label for="lat_max">Max Latitude:</label>
            <input type="text" name="lat_max" value="{lat_max or ''}"><br><br>
            <input type="submit" value="Filter Locations">
        </form>
    """

    if selected_state and lat_min and lat_max:
        try:
            lat_min_val = float(lat_min)
            lat_max_val = float(lat_max)
            lat_min_val, lat_max_val = min(lat_min_val, lat_max_val), max(lat_min_val, lat_max_val)

            safe_state = selected_state.replace("'", "''")

            location_query = f"""
            SELECT Site, Name, Region, Lat
            FROM Location
            WHERE TRIM(State) LIKE '{safe_state}' AND CAST(Lat AS REAL) BETWEEN {lat_min_val} AND {lat_max_val}
            ORDER BY CAST(Lat AS REAL) ASC;
            """

            print("Running query:", location_query)
            results = pyhtml.get_results_from_query("database/BOM2.db", location_query)
            print("Results fetched:", results)

            page_html += f"""
            <h3>Results for {selected_state} between latitudes {lat_min_val} and {lat_max_val}</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr><th>Site</th><th>Name</th><th>Region</th><th>Latitude</th></tr>
            """
            for row in results:
                site, name, region, lat = row
                page_html += f"<tr><td>{site}</td><td>{name}</td><td>{region}</td><td>{lat}</td></tr>"

            page_html += "</table>"
        except ValueError:
            page_html += "<p style='color:red;'>Please enter valid numeric latitude values.</p>"

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
