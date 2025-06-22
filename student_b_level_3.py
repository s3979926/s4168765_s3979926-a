import pyhtml

def convert_dmy_to_tuple(dmy):
    try:
        day, month, year = map(int, dmy.split("/"))
        return year, month, day
    except:
        return None

def get_page_html(form_data):
    ref_metric = form_data.get('ref_metric')
    start_year = form_data.get('start_year')
    end_year = form_data.get('end_year')
    num_metrics = form_data.get('num_metrics')

    if isinstance(ref_metric, list): ref_metric = ref_metric[0]
    if isinstance(start_year, list): start_year = start_year[0]
    if isinstance(end_year, list): end_year = end_year[0]
    if isinstance(num_metrics, list): num_metrics = num_metrics[0]

    page_html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Task 3B - Similar Metrics by Trend</title>
    </head>
    <body>
        <h1>Find metrics with similar change to the reference metric</h1>
        <form action="/page3b" method="GET">
            <label for="ref_metric">Select reference metric:</label>
            <select name="ref_metric">
    """

    metric_columns = ['RainDaysNum', 'MaxTemp', 'MinTemp', 'Precipitation', 'PrecipQual', 'Evaporation', 'EvapQual']
    for m in metric_columns:
        selected = 'selected' if ref_metric == m else ''
        page_html += f'<option value="{m}" {selected}>{m}</option>'
    
    page_html += f"""
            </select><br><br>
            <label>Select start year (min =1970):</label>
            <input type="number" name="start_year" value="{start_year or ''}" min="1970" max="2020"><br><br>
            <label>Select end year (max = 2020):</label>
            <input type="number" name="end_year" value="{end_year or ''}" min="1970" max="2020"><br><br>
            <label for="num_metrics">Number of similar metrics to compare:</label>
            <input type="number" name="num_metrics" value="{num_metrics or '3'}"><br><br>
            <input type="submit" value="Find similar metrics">
        </form>
    """
# Filtering time period
    if ref_metric and start_year and end_year and num_metrics:
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            mid_year = (start_year + end_year) // 2
            num_metrics = int(num_metrics)

            start1 = (start_year, 1, 1)
            end1 = (mid_year, 12, 31)
            start2 = (mid_year + 1, 1, 1)
            end2 = (end_year, 12, 31)

            query = f"""
                SELECT Location, DMY, {', '.join(metric_columns)}
                FROM States_combined
                WHERE DMY IS NOT NULL
            """
            results = pyhtml.get_results_from_query("database/Stations_combined.db", query)

            metric_data = {metric: [] for metric in metric_columns}
            for row in results:
                _, dmy, *values = row
                date = convert_dmy_to_tuple(dmy)
                if date:
                    for i, metric in enumerate(metric_columns):
                        val = values[i]
                        if val is not None:
                            try:
                                val = float(val)
                                metric_data[metric].append((date, val))
                            except:
                                continue

# Defining dunction to calculate average value of each metrics
            def avg(vals, start, end):
                data = [v for d, v in vals if start <= d <= end]
                return sum(data) / len(data) if data else None

            ref_vals = metric_data.get(ref_metric, [])
            ref_avg1 = avg(ref_vals, start1, end1)
            ref_avg2 = avg(ref_vals, start2, end2)

            if ref_avg1 is not None and ref_avg2 is not None and ref_avg1 != 0:
                ref_change = (ref_avg2 - ref_avg1) / ref_avg1 * 100
                metric_diffs = []

                for metric, values in metric_data.items():
                    if metric == ref_metric:
                        continue
                    avg1 = avg(values, start1, end1)
                    avg2 = avg(values, start2, end2)
                    if avg1 is not None and avg2 is not None and avg1 != 0:
                        change = (avg2 - avg1) / avg1 * 100
                        diff = abs(change - ref_change)
                        metric_diffs.append((metric, round(avg1, 2), round(avg2, 2), round(change, 2), round(diff, 2)))

                metric_diffs.sort(key=lambda x: x[4])
                top_similar = metric_diffs[:num_metrics]

                # Show reference metric at the top
                page_html += f"""
                <h3>Most similar metrics (Compared to {ref_metric} from {start_year} to {end_year})</h3>
                <p>Split into two periods: ({start_year}-{mid_year}) and ({mid_year + 1}-{end_year})</p>
                <table border="1" style="border-collapse: collapse;">
                    <tr>
                        <th>Metric</th>
                        <th>Avg value in Period 1</th>
                        <th>Avg value in Period 2</th>
                        <th>% Change</th>
                        <th>Difference from {ref_metric} (%)</th>
                    </tr>
                        <td>{ref_metric}</td>
                        <td>{round(ref_avg1, 2)}</td>
                        <td>{round(ref_avg2, 2)}</td>
                        <td>{round(ref_change, 2)}</td>
                        <td>0.00 (selected)</td>
                    </tr>
                """
                for row in top_similar:
                    page_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
                page_html += "</table>"
            else:
                page_html += "<p style='color:red;'>Reference metric lacks valid data for both periods.</p>"

        except Exception as e:
            page_html += f"<p style='color:red;'>Error: {str(e)}</p>"

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