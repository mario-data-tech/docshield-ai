from __future__ import annotations

from pathlib import Path
import typer
from .scanner import Scanner
from .classifier import Classifier
from .report import ReportWriter

app = typer.Typer(add_completion=False, help="DocShield.ai - Sensitive Data Discovery & DSPM lightweight engine")

@app.command()
def scan(
    path: str = typer.Argument(..., help="File or folder to scan"),
    output: str = typer.Option("json", "--output", "-o", help="json|html|csv"),
    report_path: str = typer.Option("report", "--report-path", help="Output path without extension for json/html or full csv path"),
    enable_nlp: bool = typer.Option(True, "--enable-nlp/--no-nlp"),
):
    scanner = Scanner(enable_nlp=enable_nlp)
    results = scanner.scan_path(path)
    report = Classifier().score(results)
    if output == "json":
        out = Path(f"{report_path}.json")
        out.write_text(ReportWriter.to_json(report), encoding="utf-8")
    elif output == "html":
        out = Path(f"{report_path}.html")
        out.write_text(ReportWriter.to_html(report), encoding="utf-8")
    else:
        out = ReportWriter.to_csv(report, report_path if report_path.endswith(".csv") else f"{report_path}.csv")
    typer.echo(f"Saved report to {out}")

def main():
    app()

if __name__ == "__main__":
    main()
