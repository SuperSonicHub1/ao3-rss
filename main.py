from ao3_rss import create_app

app = create_app()
app.run("0.0.0.0", 8080)
