export function LocatorPreview({ current }: { current: any }) {
  if (!current) return null;
  return (
    <div style={{ padding: 10, background: "#f8f8f8", border: "1px solid #ddd" }}>
      <h4>Current Action Preview</h4>
      <pre style={{ fontSize: 12, margin: 0 }}>
        {JSON.stringify(current, null, 2)}
      </pre>
    </div>
  );
}