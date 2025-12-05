export function ControlPanel({
  isRecording,
  onStart,
  onStop,
  onExport
}: {
  isRecording: boolean;
  onStart: () => void;
  onStop: () => void;
  onExport: () => void;
}) {
  return (
    <div style={{ display: "flex", gap: 10 }}>
      <button onClick={onStart} disabled={isRecording} style={{ padding: "6px 12px" }}>
        Start Recording
      </button>

      <button onClick={onStop} disabled={!isRecording} style={{ padding: "6px 12px" }}>
        Stop Recording
      </button>

      <button onClick={onExport} style={{ padding: "6px 12px" }}>
        Export YAML
      </button>
    </div>
  );
}