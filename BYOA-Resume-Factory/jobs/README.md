# Job packages

One folder per application. Copy `_template/`; do not edit it in place.

Folder name: letters, numbers, hyphens only (no `:` or spaces).

macOS/Linux: `cp -a jobs/_template jobs/acme-sre-nyc`  
Windows: `xcopy /E /I jobs\_template jobs\acme-sre-nyc`

Paste the JD into `JOB.md`. The agent fills `package.yaml`.

`example-acme-sre/` is **fictional** — run the PDF builder on it, then delete
it. Do not copy its numbers onto your resume.
