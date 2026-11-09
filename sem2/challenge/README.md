# Chain Reaction

A basic Flask cybersecurity challenge with four stages.

## Run

1. Install Flask: `python -m pip install flask`
2. Run from this directory: `python app.py`
3. Open `http://127.0.0.1:5000` in a browser.

Set `FLASK_SECRET_KEY` to a long random value before deploying. The built-in fallback key is for local testing only.

The challenge uses fictional training data. Stage 4's PCAP generator requires Scapy (`python -m pip install scapy`) if you need to regenerate the capture.
