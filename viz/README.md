# Ocean wave visualization

Optional browser-based WebGL ocean simulation. This is not used by the Raspberry Pi motor control software — it is a standalone visualization you can open locally for reference or demos.

## Run locally

Serve the folder with any static file server, then open `index.html`:

```bash
cd viz
python3 -m http.server 8080
```

Open http://localhost:8080 in a browser.
