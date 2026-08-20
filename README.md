# DocShield.ai

DocShield.ai es un motor ligero de descubrimiento de datos sensibles y cumplimiento, orientado a escaneo local de archivos y carpetas.

## Instalación

```bash
git clone [https://github.com/mario-data-tech/docshield-ai.git](https://github.com/mario-data-tech/docshield-ai.git)
cd docshield-ai
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e ".[nlp]"
python -m spacy download en_core_web_sm
docshield scan ./data --output json --report-path ./reports/docshield
docshield scan ./data --output html --report-path ./reports/docshield
docshield scan ./data --output csv --report-path ./reports/docshield.csv
pytest
docker build -f docker/Dockerfile -t docshield-ai .
docker run --rm -v "$PWD":/data docshield-ai scan /data --output json --report-path /data/report
