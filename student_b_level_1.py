def get_page_html(form_data):
    print("About to return page home page...")
    
    page_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Database Web-App Demo</title>
    </head>
    <body>
        <h1>About us</h1>
        <h3>Our purpose:</h3>
        <p>Our website was created to inform knowledge about the global weather and climate. </p>
        <p>As climate change poses a major threat to ecosystems, communities, and economies. This website provides users resources about climate, fulfill their needs whether for ordianry weather info or insights about the climate.</p>

        <h3>How the site can be use? </h3>
        <p>Our website gives users free access to a diversity range of data in the form of graph, statistics, etc.</p>
        <p>User can use these data for basic weather check, eduction or even insightful researches. The website gives users wide possibilities to work with our resources. </p>

    <head>
        <script>
            function toggleImage(id) {{
                var img = document.getElementById(id);
                if (img.style.display === "none") {{img.style.display = "block";}} 

                else {{img.style.display = "none";}} }}

        </script>
    </head>
    <body>

        <h3>Our personas</h3>
        <button onclick="toggleImage('personaA')">Show/Hide Persona A</button><br>
        <img id="personaA" src="images/Persona_A" alt="Persona A" style="width:40%; height:auto; display:none;"><br><br>

        <button onclick="toggleImage('personaB')">Show/Hide Persona B</button><br>
        <img id="personaB" src="images/Persona_B" alt="Persona B" style="width:40%; height:auto; display:none;"><br>

        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
        <img src="images/rmit.png" style="width: 30%; height: auto;">
    </body>
    </html>
    """
    return page_html