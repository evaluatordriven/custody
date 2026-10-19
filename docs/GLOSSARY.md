# Glossary

*Not part of the standard's rules. Plain explanations of every word the specification uses. Where a word
is one of the specification's defined terms, the definition that counts is the one in SPEC.md, section 2;
the explanation here only puts it in plain words.*

Words are grouped by what they are about. Field names, as they appear inside a record, are shown like
`this`.

## The standard's defined terms

*Each of these is defined in SPEC.md, section 2.*

### artifact
The work being judged: a document, a dataset, a piece of software, a report. A record identifies it by a
fingerprint of each of its files.

### bar
The written statement of what good looks like for the work. It is broken into parts, and it is fixed
before the work starts.

### dimension
A single part of the bar, judged on its own. "Every figure names its source" could be one.

### maker
Whoever made the work: a person, a team, or an AI tool.

### evaluator
The party who reads the work against the bar. An evaluator did not make the work and did not write the
bar. It can be a person, an AI model, or a script. Each session of an AI model counts as a separate
party.

### buyer
The party the work is for. The buyer's question is whether the work does the job it was meant to do.

### specialist
A person who knows the field well enough to say what good looks like. On evaluatordriven.com this is
called a subject matter expert.

### check
A single reading of one dimension, by one evaluator, in one run.

### instrument
The written rules an evaluator reads by (the rubric), and the tool that applies them (the runner).

### record
The set of documents that travel with the work: the bar, who checked the work, what they found, and who
accepted it. Technically, it is an in-toto Statement whose predicate is `custody/v1` (both explained
below).

### published
Made available at a stable address to the people who rely on the record. Published does not have to mean
public.

### disposition
The final decision on the work, made by a named person, the approver. It is one of three: `given`
(accepted), `not_yet_given` (not yet accepted), or `declined`.

## Outcomes and decisions

### conforms, does not conform, unobserved
The three outcomes of a check. Conforms means the work meets that dimension. Does not conform means it
falls short. Unobserved (on the website: not observed) means the evaluator could not tell, and must say
which way it tried and why it failed. An unobserved check is never turned into a pass or a fail.

### approver
The named person who makes the disposition. The approver is never one of the evaluators.

### acknowledged
What the approver does with unobserved parts: names them in the disposition, so the decision to go ahead
without them is on the record.

### violation
A dimension where at least one check did not conform. Every record lists its violations, even when there
are none.

### disagreement
Two or more checks of the same dimension that came out differently. The record names them. Outcomes are
never averaged into one.

### dissent
Where the buyer and the specialist disagree about the bar. The disagreement is written down and kept
in the record, and never averaged away.

## Levels

### level
How much proof a record claims. The record states its claim in `levelClaimed`.

### CL1
The basic level. The bar came first, it was approved, someone other than the maker checked the work,
the checks show they could catch a planted problem, and a named person decided. The evaluator can be a
fresh session of the maker's own AI model, if the record says so. The maker may also approve the bar,
as buyer or specialist, if the record names that overlap as a separation gap. This lets a one-person
shop reach CL1 honestly.

### CL2
A stricter level. Every evaluator reads each dimension at least twice, and the record shows how often the
readings agreed. If AI models check the work, at least one comes from a different model family than the
maker's. And for each dimension, evaluators from the maker's model family are no more than half of those
who read it; people and scripts count in that total. At CL2 the maker may not approve the bar.

### CL3
The strictest level. Each evaluator proved it could catch a planted problem before it read the real work.
The bar is published. The record is signed and entered in a transparency log, a log that shows any later
change, and someone other than the maker has checked that entry.

### baseline
A record whose bar was written after the work was made. It is honest about that, and it makes no claim
that the bar came first. It lists what was read before the bar was fixed.

## Inside a record

### subject
The list of the work's files, each with its fingerprint.

### digest, sha256, fingerprint
A digest is a short code worked out from a file's exact contents. sha256 is the method used. If a single
character of the file changes, the digest changes too. That is how a record proves which version of the
work it describes. This guide also calls it a fingerprint.

### frozen, `frozenAt`
When the bar was fixed. After this moment the bar does not change.

### `producedAt`
When the work was finished. For a CL1 claim, the bar must be frozen before this.

### approval
A signed-off agreement to the bar, by the buyer or the specialist, with who, when, and the fingerprint of
the bar they approved. When the specialist is a published standard rather than a person, the approval
names that standard and its version (`adopted`).

### criterion
What a dimension asks for, in words.

### scale, anchors, threshold, floor
How a dimension is scored, when it is scored with numbers. The scale gives the range. Anchors describe
what each score looks like. The threshold is the score needed to conform. The floor is the lowest score
allowed at all.

### ground truth
The references the bar judges against, such as an approved source document or a website as it stood on
a given day. Each is named with its version and fingerprint.

### method
The written rules the maker followed, identified by their fingerprint.

### kind
What sort of evaluator it is: `person`, `model` or `script`.

### model family, identifier, endpoint
For an AI evaluator: its family (the model line, as its builder names it, such as `gpt` or `qwen`), its
exact version, and the host name of the service that answered.

### read-only, `readOnly`
The AI evaluator could read the work but not change it.

### same model as maker, `sameModelAsMaker`
A flag that says an evaluator is a fresh session of the very AI model that made the work. It must be set
exactly when that is true: leaving it off for the maker's own model, or setting it for a different model,
fails the record. Such a session is allowed at CL1.

### run, batch
A run is one pass of an evaluator over the work. A batch is a group of checks done together.

### spread
For CL2: how many runs each evaluator did on a dimension, and how many agreed.

### failure condition, `failureCondition`
What would have made a check fail. Writing it down shows the check could have gone the other way.

### evidence
What a check points to as its reason: a quote, a test result, a log.

### control, planted case
A test with a known answer, mixed in with the real work. Usually it is a copy of the work with a flaw
added on purpose. If an evaluator gets a control wrong, that evaluator's checks in the same batch cannot
be trusted, so they must be recorded as not observed. A control can name the one dimension it tests;
then only the checks of that dimension are affected. Controls in a record are run alongside
the real checks. Demonstrations, at CL3, are planted cases done before the real reading.

### separation gap
A place where the people who should be kept apart were not. For example, one person wrote the bar and
made the work. A good record lists its gaps.

### external evidence, `external`
Proof kept outside the record, such as a log of which AI model answered. A named person who is not the
maker must have read it.

### retention
Where the full record is kept, and whether it is public.

## Checking a record

### checker, verifier
A program that reads a record and reports whether it follows the rules. `checker/check.py` is the free
one that comes with the standard. To check fully, it needs the record, the work's files and the bar file,
so it can confirm each one matches its fingerprint. If it ever disagrees with SPEC.md, SPEC.md wins.

### OK, FAILED, NOT-CHECKABLE
The checker's verdict. OK: every rule checked holds. FAILED: at least one rule is broken, and it names
which. NOT-CHECKABLE: something the record points to could not be seen, often external evidence.

### level achieved
The level the record actually reached, as the checker works it out. It is never more than the claim.

### routing
Where the record should go next. "To approver" means a person still needs to decide about something.
"Acknowledged" means some parts were unobserved and the approver has already named them in a given
disposition. "None" means nothing is waiting.

### requirement ID
The label of one rule in the specification, such as CL1-6. Each rule is also marked structural (about
the record's shape), semantic (about what it says), or external (it needs evidence from outside).

### key words
When the specification writes must, should or may in capital letters, they carry the formal meanings set
by BCP 14, the standard reference for such words.

## The technical wrapping

### in-toto, Statement, predicate
in-toto is an existing open format for statements about software and how it was made. A Statement names
what it is about (the subject) and what it says (the predicate). This standard's predicate is called
`custody/v1`.

### JSON, schema
JSON is the plain-text format records are written in. The schema is the formal description of a record's
shape, which other programs can check against.

### fixture
A sample record used to test the checker. Each one is built to pass, or to fail for one known reason.

### custody log
A running list of events, written as the work happens, where each entry is sealed to the one before. If
anyone edits, removes or reorders an entry, the seal breaks. Records can be built from it, so nothing is
pieced together afterward.

## Words from evaluatordriven.com

### custody
Holding the bar and the record, and answering for them.

### decider, practitioner
The two readers the website is written for. A decider decides whether to accept work. A practitioner does
the work, or leads the people who do.

### judge
On the website, an AI model used as an evaluator.

### gate, threshold
The point where work passes or does not. In the specification this is a dimension's threshold.

### handoff, delegation
Giving the work to someone else, and giving them the way it was made. A record lets the next person see
how quality was decided, even after the original people have left.

### signature
The named person who accepts the result. In the specification, this is the approver's disposition.

### specification
The document that states the rules: SPEC.md.
