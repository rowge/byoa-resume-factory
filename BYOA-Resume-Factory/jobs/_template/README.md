# Job package

1. Paste the posting into `JOB.md`.
2. Agent fills `package.yaml` from CONTEXT + story bank only.
3. From `tools/` — Windows: `build.bat ..\jobs\<this-folder>`
   (or `py -3 build_pdfs.py ..\jobs\<this-folder>`).
   macOS/Linux: `./build.sh ../jobs/<this-folder>`.

PDFs land here. Edit YAML and rebuild; do not hand-edit the PDFs.
