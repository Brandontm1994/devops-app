import React from "react";

export function EventStream({ events }: { events: any[] }) {
  return (
    <div style={{ padding: 10, border: "1px solid #ddd" }}>
      <h3>Live Events</h3>
      <div style={{ height: 150, overflowY: "scroll" }}>
        {events.map((evt, i) => (
          <div key={i} style={{ fontSize: 12 }}>
            {evt.action} → {JSON.stringify(evt.locator)}
          </div>
        ))}
      </div>
    </div>
  );
}
