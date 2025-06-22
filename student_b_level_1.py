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
        <p>As climate change poses a major threat to ecosystems, communities, and economies, our website was created to inform knowledge and insights about the global weather and climate. 
        Using a database that collects various of climate metrics from multiple places, across Australia, other than aiming for education purposes, users can also use our resources for 
        insight studies, daily needs like weather checking, etc . </p>


        <h3>How the site can be use? </h3>
        <p>Our website gives users free access to a diversity range of climate data through our filtering models that spread across both A and B sections of page 1 and 2.</p>
        <p>User can use our resources for basic weather check, eduction or even insightful researches. The usage possibilities of the website is diverse for the user to work with, fulfill their needs and goals. </p>

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


        <h3>Our members</h3>
        <button onclick="toggleImage('Members')">Show/Hide Members info </button><br>
        <img id="Members" src="images/members_detail" alt="Members" style="width:40%; height:auto; display:none;"><br><br>


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