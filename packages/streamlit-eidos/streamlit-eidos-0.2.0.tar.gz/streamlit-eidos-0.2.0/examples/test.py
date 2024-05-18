import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import shapely as sh

from streamlit_eidos import st_eidos
from oceanum.eidos import Eidos, Node, EidosDatasource, FeatureLayerSpec

os.environ["EIDOS_RENDERER"] = "http://localhost:3001"

st.write("## Example EIDOS")

layerSpec = FeatureLayerSpec(
    hoverInfo={"template": "{{name}}"},
    style={
        "getPointRadius": 10,
        "getFillColor": "red",
        "opacity": 1.0,
        "pointRadiusUnits": "pixels",
    },
)

if "points" not in st.session_state:
    st.session_state["points"] = gpd.GeoDataFrame({"name": []}, geometry=[])

data = [EidosDatasource(id="points", data=st.session_state["points"])]

e = Eidos(
    id="eidos_test",
    name="EIDOS Test",
    title="Test",
    data=data,
    rootNode=Node(
        id="my-map",
        name="Root",
        nodeType="world",
        nodeSpec={
            "layers": [
                {
                    "id": "points",
                    "layerType": "feature",
                    "dataId": "points",
                    "visible": True,
                    "layerSpec": layerSpec,
                }
            ]
        },
    ),
)


value = st_eidos(e, height=800, events=["click"])
print(value)
if (
    value
    and "lastevent" in value
    and not value["lastevent"] == st.session_state.get("lastevent", {})
):
    st.session_state["lastevent"] = value["lastevent"]
    points_data = gpd.GeoDataFrame(
        {"name": ["Null island"]},
        geometry=[sh.geometry.Point(value["lastevent"]["coordinate"])],
    )
    st.session_state["points"] = pd.concat(
        [st.session_state["points"], points_data],
        ignore_index=True,
    )
    print("Adding point")
    st.rerun()

click = st.button("Clear points")
if click:
    st.session_state.pop("points", None)
    print("Clearing points")
    st.rerun()
