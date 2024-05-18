/* eslint-disable react/prop-types */
import { useCallback, useEffect, useRef } from "react";
import { withStreamlitConnection, Streamlit } from "streamlit-component-lib";

const Eidos = ({ args }) => {
  const {
    key,
    eidos,
    spectype,
    height = 500,
    events = [],
    renderer = "https://render.eidos.oceanum.io",
  } = args;
  const container = useRef(null);
  const iframeRef = useRef(null);

  useEffect(() => {
    Streamlit.setFrameHeight();
  });

  useEffect(() => {
    if (iframeRef.current) {
      window.addEventListener("message", handleMessage);
    }
  }, []);

  useEffect(() => {
    updateSpec(eidos, spectype);
  }, [eidos, spectype]);

  const handleMessage = useCallback(
    (message) => {
      const { data } = message;
      if (data.action === "status" && data.data.status === "ready") {
        updateSpec(eidos, spectype);
      } else if (events.includes(data.action)) {
        console.log("sending event");
        Streamlit.setComponentValue({
          lastevent: data,
        });
      }
    },
    [events]
  );

  const updateSpec = useCallback(
    (spec, spectype) => {
      const messageTarget = iframeRef.current?.contentWindow;
      if (messageTarget) {
        messageTarget.postMessage(
          { id: key, type: spectype, payload: spec },
          "*"
        );
      }
    },
    [key, iframeRef]
  );

  return (
    <div
      className="eidos-component"
      style={{ height, width: "100%", position: "relative" }}
      ref={container}
    >
      <iframe
        title="Eidos"
        src={`${renderer}?id=${key}`}
        style={{ width: "100%", height: "100%", border: "none" }}
        ref={iframeRef}
      ></iframe>
    </div>
  );
};

export default withStreamlitConnection(Eidos);
