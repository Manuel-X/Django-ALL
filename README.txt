dynamic include tag:

<h1>
    Hey {{name}} you're awesome!
    <small>Not really...</small>
</h1>

Usage in another html: {% include 'awesome.html' with name="Aziz" %} 

