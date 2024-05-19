
def test_minify(plugin):
    source_html = """
        <!DOCTYPE html>
        <html>
          <head>
          <body>
            <h1>Hola Mundo!</h1>
          </body>
        </html>
    """

    result = plugin.minify(source_html)

    expected_html = "<!doctypehtml><body><h1>Hola Mundo!</h1>"
    assert result == expected_html


def test_minify_ignore_image(plugin, load_image):
    image = load_image

    assert plugin.is_valid_minify(image) is False
    assert plugin.minify(image) == image
