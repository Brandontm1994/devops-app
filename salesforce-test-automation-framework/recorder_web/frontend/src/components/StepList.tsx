export function StepList({ steps }: { steps: any[] }) {
  return (
    <div style={{ marginTop: 20 }}>
      <h3>Recorded Steps</h3>
      <ul>
        {steps.map((s, i) => (
          <li key={i}>
            <strong>{s.action}</strong> → {JSON.stringify(s.locator)}
          </li>
        ))}
      </ul>
    </div>
  );
}