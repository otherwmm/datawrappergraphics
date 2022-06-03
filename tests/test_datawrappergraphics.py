import pandas as pd
import datawrappergraphics

def test_simple_map():
    
    TEST_CHART_ID = "UPTcO"
    
    raw = pd.DataFrame({"title": ["Point 1"], "latitude": [50.2373819], "longitude": [-90.708556], "anchor": ["middle-right"], "tooltip": ["A test tooltip."], "icon": ["attention"]})
    
    assert (datawrappergraphics.Map(chart_id=TEST_CHART_ID)
        .data(raw)
        .head(f"Testing datawrappergraphics library")
        .deck("")
        .publish()
    )