import datetime
import os

class HTMLReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate(self, results):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/report_{timestamp}.html"

        html = [
            "<html><head><title>Salesforce Test Report</title></head><body>",
            "<h1>Salesforce Test Automation Report</h1>",
            "<table border='1' cellpadding='6' cellspacing='0'>",
            "<tr><th>Step</th><th>Action</th><th>Status</th><th>Details</th></tr>"
        ]

        for idx, r in enumerate(results):
            html.append(
                f"<tr>"
                f"<td>{idx + 1}</td>"
                f"<td>{r['action']}</td>"
                f"<td>{r['status']}</td>"
                f"<td>{r.get('details', '')}</td>"
                f"</tr>"
            )

        html.append("</table></body></html>")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(html))

        return filename

