import React from "react";
import { useRecorder } from "./hooks/useRecorder";
import { ControlPanel } from "./components/ControlPanel";
import { EventStream } from "./components/EventStream";
import { StepList } from "./components/StepList";
import { LocatorPreview } from "./components/LocatorPreview";

export default function App() {
  const recorder = useRecorder();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, padding: 20 }}>
      <h2>Salesforce UI Recorder</h2>

      <ControlPanel
        isRecording={recorder.isRecording}
        onStart={recorder.startRecording}
        onStop={recorder.stopRecording}
        onExport={recorder.exportYaml}
      />

      <LocatorPreview current={recorder.currentEvent} />

      <EventStream events={recorder.events} />

      <StepList steps={recorder.steps} />
    </div>
  );
}