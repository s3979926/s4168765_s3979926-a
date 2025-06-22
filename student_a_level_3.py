import pyhtml

def convert_dmy_to_tuple(dmy):
    try:
        day, month, year = map(int, dmy.split("/"))
        return year, month, day
    except:
        return None

def get_page_html(form_data):
    print("About to return page 3")

    ref_station = form_data.get('station')
    start_year = form_data.get('start_year')
    end_year = form_data.get('end_year')
    metric = form_data.get('metric')
    num_similar = form_data.get('num_similar')

    if isinstance(ref_station, list): ref_station = ref_station[0]
    if isinstance(metric, list): metric = metric[0]
    if isinstance(num_similar, list): num_similar = num_similar[0]
    if isinstance(start_year, list): start_year = start_year[0]
    if isinstance(end_year, list): end_year = end_year[0]

    page_html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Page 3A - Similar Weather Station Trends</title>
    </head>
    <body>
        <h1>Compare Climate Change Across Weather Stations</h1>
        <form action="/page3a" method="GET">
            <label for="station">Select Reference Station:</label>
            <select name="station">
    """

    station_query = """
        SELECT DISTINCT Location FROM (
            SELECT Location FROM AAT
            UNION
            SELECT Location FROM AET
        ) ORDER BY Location;
    """
    stations = pyhtml.get_results_from_query("database/BOM2.db", station_query)
    for (station,) in stations:
        selected = 'selected' if ref_station == station else ''
        page_html += f'<option value="{station}" {selected}>{station}</option>'

    page_html += f"""
            </select><br><br>
            <label>Select Start Year:</label>
            <input type="number" name="start_year" value="{start_year or ''}" min="1970" max="2020"><br><br>
            <label>Select End Year:</label>
            <input type="number" name="end_year" value="{end_year or ''}" min="1970" max="2020"><br><br>
            <label for="metric">Select Metric:</label>
            <select name="metric">
                <option value="MaxTemp">MaxTemp</option>
                <option value="MinTemp">MinTemp</option>
                <option value="Precipitation">Precipitation</option>
            </select><br><br>
            <label for="num_similar">Number of Similar Stations to Find:</label>
            <input type="number" name="num_similar" value="{num_similar or '2'}"><br><br>
            <input type="submit" value="Find Similar Stations">
        </form>
    """

    if ref_station and start_year and end_year and metric and num_similar:
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            mid_year = (start_year + end_year) // 2

            start1 = (start_year, 1, 1)
            end1 = (mid_year, 12, 31)
            start2 = (mid_year + 1, 1, 1)
            end2 = (end_year, 12, 31)

            query = f"""
                SELECT Location, DMY, {metric}
                FROM AAT
                WHERE {metric} IS NOT NULL
                UNION ALL
                SELECT Location, DMY, {metric}
                FROM AET
                WHERE {metric} IS NOT NULL
            """
            data = pyhtml.get_results_from_query("database/BOM2.db", query)

            records = []
            for loc, dmy, val in data:
                date = convert_dmy_to_tuple(dmy)
                if date:
                    try:
                        val = float(val)
                        records.append((loc, date, val))
                    except:
                        continue

            station_data = {}
            for loc, date, val in records:
                if loc not in station_data:
                    station_data[loc] = []
                station_data[loc].append((date, val))

            def avg(data, start, end):
                vals = [v for d, v in data if start <= d <= end]
                return sum(vals) / len(vals) if vals else None

            ref_data = station_data.get(ref_station, [])
            avg1 = avg(ref_data, start1, end1)
            avg2 = avg(ref_data, start2, end2)

            if avg1 is not None and avg2 is not None and avg1 != 0:
                ref_change = (avg2 - avg1) / avg1 * 100.0
                comparisons = []

                for station, data in station_data.items():
                    if station == ref_station:
                        continue
                    a1 = avg(data, start1, end1)
                    a2 = avg(data, start2, end2)
                    if a1 is not None and a2 is not None and a1 != 0:
                        change = (a2 - a1) / a1 * 100.0
                        diff = abs(change - ref_change)
                        comparisons.append((station, round(a1, 2), round(a2, 2), round(change, 2), round(diff, 2)))

                comparisons.sort(key=lambda x: x[4])
                top_similar = comparisons[:int(num_similar)]

                page_html += f"""
                <h3>Most Similar Weather Stations (Compared to site {ref_station} from {start_year} to {end_year}, in form of {metric})</h3>
                <p>Split into two periods: ({start_year}-{mid_year}) and ({mid_year + 1}-{end_year})</p>
                <table border="1" style="border-collapse: collapse;">
                    <tr>
                        <th>Station</th>
                        <th>Avg in Period 1</th>
                        <th>Avg in Period 2</th>
                        <th>% Change</th>
                        <th>Difference from Reference</th>
                    </tr>
                """
                for row in top_similar:
                    page_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
                page_html += "</table>"
            else:
                page_html += "<p style='color:red;'>Reference station does not have valid data in both periods.</p>"

        except Exception as e:
            page_html += f"<p style='color:red;'>Error occurred: {str(e)}</p>"

    page_html += """
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
