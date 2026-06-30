# Ocean wave visualization

Optional browser-based WebGL ocean simulation. This is **not** used by the Raspberry Pi motor control software — it is a standalone visualization for reference or demos.

## Attribution

The `viz/` folder contains a WebGL ocean wave simulation bundled with this project. A reference video is linked from `index.html` ([YouTube](https://youtu.be/IrUehq6vJss)). The visualization code predates the current Driftwood motor software and is included as a separate browser demo.

Driftwood motor control software is licensed under MIT (see [LICENSE](../LICENSE) in the repository root).

## Run locally

Serve the folder with any static file server, then open `index.html`:

```bash
cd viz
python3 -m http.server 8080
```

Open http://localhost:8080 in a browser with WebGL support.
