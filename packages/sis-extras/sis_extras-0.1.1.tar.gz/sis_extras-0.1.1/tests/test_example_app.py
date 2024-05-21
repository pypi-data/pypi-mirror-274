from streamlit.testing.v1 import AppTest

at = AppTest.from_file("example_app_formatting.py")

at.run()

assert not at.exception

assert at.tabs[0].label == "Chart"

assert at.tabs[1].label == "Data Preview"

assert list(at.tabs[1].children[0].value.x.values) == list(range(10))
assert list(at.tabs[1].children[0].value.y.values) == list(range(10))

assert at.tabs[2].label == "SQL"

assert at.tabs[3].label == "Description"

assert at.tabs[3].children[0].value == "Sample Tile"

assert at.tabs[4].label == "Download Data"
