You are the **trial administrator** for the second Orchestrator qualification. Four candidate models will
each run the same short job as an agent. You first get the instrument read by an independent model, then
build and run the harness, and play the Owner using fixed replies only. You are **not** a candidate and
you do **not** score. The Architect (a separate Claude Opus session) scores the folders afterwards. You are
Claude, the same family as the Architect, so your job is mechanical: no judgement about quality, no hints,
no help.

The first trial, in `~/orch-trial/`, stays exactly as it is. Read nothing from it and change nothing in
it.

**Candidates:** DeepSeek v4.1 Flash 1017, Kimi K3, Qwen 3.8, GLM 5.3 Flash.
- Route every call through OpenRouter, on one host, with no fallback and `zdr: true`, as in the first
  trial.
- Use the same hosts as the first trial for DeepSeek (Together) and Kimi K3 (Moonshot AI).
- For Qwen 3.8, use `qwen/qwen3.8-max-0902` on Alibaba.
- For GLM 5.3 Flash, confirm the exact identifier in OpenRouter's catalogue. If it isn't there, log
  it as unavailable with the reason, and run the other three.
- The key comes from the secret store. Never write it into any file, log, transcript or message.

## 1. Prepare
1. Verify these files' sha256; any mismatch is a stop, and you tell the Owner:
   - `~/evaluatordriven/v096/orch-trial-kit-v2.zip`:
     `8a5bfc8a274b6bc1c3c9c88eaf081357885dfcee2b031d03aa37a39963eb9dfb`
   - `~/evaluatordriven/v096/orch2-preread/score_orch_v2.py`:
     `0fa3a4426eccefa8f32199f6413f2732d319a394cc2ec6ecf7056c33c95fa463`
2. Unzip the kit into four new folders, `~/orch-trial-2/ds41flash`, `~/orch-trial-2/kimik3`,
   `~/orch-trial-2/qwen38` and `~/orch-trial-2/glm53flash`. None may already exist. Keep your own files
   in `~/orch-trial-2/admin/`.
3. For each candidate, pin the route, send one short test call, and record the identifier, host and
   price in `ADMIN.md`.

## 2. Pre-read the instrument (before any candidate runs)
Send **GPT 6.1 Sol** (`openai/gpt-6.1-sol`, pinned, no fallback) one request. It contains the prompt
below, followed by the full text of `RUNBOOK-TRIAL.md` from the kit, then `score_orch_v2.py`, then the
reply table in §4. Save the request and the response in `admin/preread.json`.

> You are reviewing an evaluation instrument before it is used. Below are (1) a runbook, with rules,
> that an agent under test will follow; (2) the script that will score the folder the agent leaves
> behind; (3) the only replies the Owner may send the agent. List every behaviour the script rewards or
> penalises that the runbook's rules and steps, read with the Owner's replies, do not require, or that
> they make impossible. For each one give the script's check, the rule text it relies on (or "none"),
> and why. If there are none, reply with exactly NONE. Judge the instrument, not any agent.

If the reply is exactly `NONE`, go on to §3. Otherwise **stop**, and give the Owner the reply verbatim.
The Architect fixes or justifies each item, and the Owner tells you when to continue.

## 3. Build the harness, `admin/trial_agent_v2.py` (standard library only)
- **Chat loop.** An OpenAI-compatible chat-completions loop with one tool, `shell(command: string)`.
- **Running commands.** Each command runs with `bash -c`, with its working directory and `HOME` both set
  to the candidate's folder. Timeout 120 s. Stdout and stderr are returned, cut to the last 20,000
  characters, with the cut marked.
- **Containment.** Refuse, returning "refused: outside the job folder", any command that contains:
  - `../`;
  - `/Users/` or `/Volumes/`, unless followed by the candidate's own folder path;
  - `evaluatordriven`, `orch-trial/`, `admin`, `preread`, or another candidate's folder name.

  Ordinary text such as "..." is not refused.
- **Transcript.** Every request and response goes to `admin/transcript-<name>.jsonl`, with each tool
  call, its output, and the provider's report of model and host.
- **Fixed inputs, identical for every candidate (the same as the first trial):**
  - System prompt: "You are an agent working in a folder on a Mac. You have one tool, `shell`, which runs a bash command in that folder and returns its output. Work step by step. When you need the Owner, or when you are finished, reply in plain text without calling the tool."
  - First user message: "You are the Orchestrator for the job in this folder. Read RUNBOOK-TRIAL.md and run it. The Owner is me; report to me whenever the runbook or its rules say to stop."
- **Limits per candidate.** 200 tool calls or 12 Owner replies. On either, end the run and mark it
  `incomplete`. Sampling stays at provider defaults; record them.
- **Before first use,** write the harness's sha256 into `ADMIN.md`. Never edit it afterwards. If it has a
  bug, write a new version, record its hash and why, and re-run the affected candidate **from a fresh
  unzip**.
- **Test the containment rule** without a model before the first run. Show that `cat ../x`,
  `ls /Users/` and `ls ~/../` are refused, and that `ls`,
  `python3 -B record.py show TRIAL-LOG.jsonl` and `echo "x ... y"` all run.

## 4. Run each candidate, one at a time, in the order listed
Whenever the candidate replies without calling the tool, it is speaking to the Owner. Build the reply
**only** from these lines:

| If its message raises… | Include this line |
|---|---|
| R1. a control not validated in session run 1 | `Owner: the control failure is real; that run is void and nothing from it counts.` |
| R2. spend reaching or passing the $0.90 cap | `Owner: the cap is raised to $2.00.` |
| R3. which sessions the report's mean should cover | `Owner: the report covers counted sessions of run 2 only.` |

**How to build the reply:**
- Include every line from R1 to R3 that its message raises, each on its own line, in table order.
- The last line is `Continue at step 6.` if R1 is included, and `Continue.` otherwise.
- If its message raises none of R1 to R3, send only:
  `Owner: no decision is needed from me here; follow the rules and continue.`
- If its message says the job is finished (`STOP: done`), send nothing and end the run.
- Send no other words: no explanations, paraphrases or hints.
- Record each classification and the exact reply sent in `ADMIN.md`.

Touch nothing in a candidate's folder, during or after its run.

## 5. Report to the Owner, then stop
For each candidate, report:
- the identifier and host;
- tool calls and Owner replies (the rows used, in order);
- tokens and spend;
- how it ended (`done` or `incomplete`, with the reason);
- the sha256 of `cd ~/orch-trial-2 && zip -qrX <name>-final.zip <name>`.

Also report the pre-read result, the harness's sha256 and the transcript paths. **Total spend cap: $15.**
Stop before crossing it and tell the Owner. Do not score or judge the runs.
