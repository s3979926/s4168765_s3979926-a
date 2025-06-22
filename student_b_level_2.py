import pyhtml


def get_page_html(form_data):
    print("About to return page 2")


    selected_metric = form_data.get('field')
    location_min = form_data.get('location_min')
    location_max = form_data.get('location_max')
    page = form_data.get('page', 1)


    if isinstance(location_min, list): location_min = location_min[0]
    if isinstance(location_max, list): location_max = location_max[0]
    if isinstance(selected_metric, list): selected_metric = selected_metric[0]
    if isinstance(page, list): page = page[0]


    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1


    page_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Filtered Stations</title>
    </head>
    <body>
        <h1>Station Filter</h1>
        <form action="/page2b" method="GET">
            <label for="field">Metric:</label>
            <select name="field">
    """


    metric_columns = ['RainDaysNum', 'MaxTemp', 'MinTemp', 'Precipitation', 'PrecipQual', 'Evaporation', 'EvapQual']
    for metric in metric_columns:
        selected = ' selected' if selected_metric == metric else ''
        page_html += f'<option value="{metric}"{selected}>{metric}</option>\n'


    page_html += f"""
            </select><br><br>
            <label for="location_min">Min Location ID:</label>
            <input type="text" name="location_min" value="{location_min or ''}"><br><br>
            <label for="location_max">Max Location ID:</label>
            <input type="text" name="location_max" value="{location_max or ''}"><br><br>
            <input type="submit" value="Filter Locations">
        </form>
    """


    if selected_metric and location_min and location_max:
        try:
            loc_min_val = float(location_min)
            loc_max_val = float(location_max)
            loc_min_val, loc_max_val = min(loc_min_val, loc_max_val), max(loc_min_val, loc_max_val)


            if selected_metric not in metric_columns:
                raise ValueError("Invalid metric selected.")


            query = f"""
            SELECT Location, DMY, {selected_metric}
            FROM States_combined
            WHERE CAST(Location AS REAL) BETWEEN {loc_min_val} AND {loc_max_val}
            ORDER BY CAST(Location AS REAL), DMY;
            """


            results = pyhtml.get_results_from_query("database/Stations_combined.db", query)
            filtered_results = [row for row in results if row[2] is not None and str(row[2]).strip() != '']


#Creating tabs, showing filtered data from 40 unique cells for each tab
            per_page = 40
            total_results = len(filtered_results)
            total_pages = (total_results + per_page - 1) // per_page
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            page_results = filtered_results[start_index:end_index]


            if page_results:
                page_html += f"""
                <h3>Results for {selected_metric} between location ID {loc_min_val} and {loc_max_val}</h3>
                <p>Page {page} of {total_pages} pages</p>
                <table border="1" style="border-collapse: collapse;">
                    <tr><th>Location</th><th>Date</th><th>{selected_metric}</th></tr>
                """
                for row in page_results:
                    location, dmy, value = row
                    page_html += f"<tr><td>{location}</td><td>{dmy}</td><td>{value}</td></tr>"
                page_html += "</table>"


                page_html += "<div style='margin-top:10px;'>"


                base_url = f"/page2b?field={selected_metric}&location_min={loc_min_val}&location_max={loc_max_val}"
#Adding ordered tabs to organise the page
                max_visible_pages = 10
                start_page = max(1, page - max_visible_pages // 2)
                end_page = min(total_pages, start_page + max_visible_pages - 1)


                if end_page - start_page < max_visible_pages:
                    start_page = max(1, end_page - max_visible_pages + 1)


                if page > 1:
                    page_html += f"""<a href="{base_url}&page={page - 1}">&lt;</a> """


                for p in range(start_page, end_page + 1):
                    if p == page:
                        page_html += f"<strong>{p}</strong> "
                    else:
                        page_html += f"""<a href="{base_url}&page={p}">{p}</a> """


                if page < total_pages:
                    page_html += f"""<a href="{base_url}&page={page + 1}">&gt;</a>"""


                page_html += "</div>"


            else:
                page_html += "<p>No valid results found for the selected metric and location range.</p>"


        except ValueError as ve:
            page_html += "<p style='color:red;'>Invalid input or metric. Please enter numeric location IDs.</p>"


    page_html += """<p><a href="/">Go to Page 1A</a></p>
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