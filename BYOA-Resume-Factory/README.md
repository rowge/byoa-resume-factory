# BYOA Resume Factory

**Bring your own agent.** Unzip it, point your agent at this folder, and talk.
More stories → better resumes. How many is enough scales with years
worked, not a universal 15.

Talk for an hour at least. Honesty beats polish. After that, you paste job
URLs (or ask it to search). That’s the product.

This is not a writer that invents metrics. It is a filing system, standing
orders for your agent, and a PDF builder.

---

## First hour

1. Unzip. Open your agent in the folder that **contains `AGENTS.md`**
   (Grok Build, Claude Code, Cursor, Codex — anything that can read and
   edit files here). Windows “Extract All” sometimes creates an extra nested
   folder — go in until you see `AGENTS.md`.
2. Say something like: *Read this folder and set me up* — or just paste an
   old resume. You do not need a magic command.
3. Talk. Eras of your career, then real incidents. Messy is fine. Voice dump
   into `stories/INBOX.md` is fine.
4. When it asks the two extra questions at the end (form drafts, money talk),
   answer yes or no. Skip them and both stay **on**.

ChatGPT-in-a-browser can help you draft, but the kit is built for an agent
that can see these files.

---

## After that

- **A job URL** → fit % for *you*, then it asks before building a package
  (unless it’s an obvious smash).
- **“Find jobs”** / a track name → search using your tracks, cities, and
  deal-breakers. It will not rebuild fifteen resumes unasked.
- **“Rejected from Acme”** / **“what’s on the board?”** → it updates or reads
  `STATUS.md`. The board is only true if you tell it what happened.

---

## Layout

| Path | What |
|------|------|
| `AGENTS.md` | Standing orders. The law. |
| `CLAUDE.md` | Same orders, filename Claude Code looks for. |
| `questionnaire.md` | Interview script (the agent can walk it as a chat). |
| `CONTEXT.md` | You, tracks, search, filters, the two opt-outs. |
| `STATUS.md` | Application board. |
| `APPLICATION-FORM-ANSWERS.md` | Awkward form questions, written once. |
| `stories/` | Inbox + numbered STAR stories. Source of truth. |
| `jobs/_template/` | Copy this for each job. |
| `jobs/example-acme-sre/` | **Fake** example. Delete when you’re done looking. |
| `tools/` | YAML → ATS-safe resume + cover letter PDFs. |

---

## PDFs

Python 3.10+. Your agent should pick the command for your OS.

**Windows** (Command Prompt or PowerShell), from `tools\`:

```text
py -3 -m pip install -r requirements.txt
build.bat ..\jobs\<slug>
```

If `py` is not found, use `python` instead of `py -3`.

**macOS / Linux**, from `tools/`:

```bash
python3 -m pip install -r requirements.txt
./build.sh ../jobs/<slug>
```

---

## License

Personal use. See `LICENSE.txt`.
