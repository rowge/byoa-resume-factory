# PDF builder

Reads `package.yaml` in a job folder. Writes:

- `<Name>_<Role>_Resume.pdf`
- `<Name>_<Role>_Cover_Letter.pdf`

ATS-safe: one column, no tables-for-layout, no graphics.

Needs Python 3.10+.

**Windows** (from this folder):

```text
py -3 -m pip install -r requirements.txt
build.bat ..\jobs\example-acme-sre
```

If `py` is missing, use `python`.

**macOS / Linux** (from this folder):

```bash
python3 -m pip install -r requirements.txt
./build.sh ../jobs/example-acme-sre
```
