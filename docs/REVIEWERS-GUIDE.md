# A guide for reviewers

*Not part of the standard's rules. A plain-language guide to reading what the standard produces.*

This guide is for people who review work rather than build it. You might work in procurement, legal,
security or management. You do not need a technical background. You do not need to read code.

## The idea in one minute

When work is made with help from AI, you often can't see how it was made. This standard gives you
another way to judge it. Before the work starts, people agree in writing on what good looks like. Then
someone who did not make the work reads it against that agreement. Everything is written down and kept
with the work. So you can look at it later, and so can anyone after you.

You are not asked to trust the tools, or the people who used them. You are asked to look at what was
agreed, who checked it, and what they found.

## The words you will meet

The standard uses a small set of ordinary words in a special way. Here they are, in the order you will
need them.

The bar means the written statement of what good looks like for this work. It is agreed before the work
starts, and it does not change once the work begins. A bar has parts. A dimension is a single part of the
bar, judged on its own. For example, "every figure names its source" could be one dimension.

The maker means the person, team or AI tool that made the work. The buyer means the party the work is
for. A specialist is a person who knows the field well enough to say what good looks like. The buyer and the
specialist both approve the bar before the work starts.

An evaluator means the party who reads the work against the bar, and did not make it. An evaluator did not
write the bar either. An evaluator can be a person, an AI model, or a script. A check is a single reading of one dimension by one evaluator. Each check ends in
one of three outcomes. Conforms means the work meets that part of the bar. Does not conform means it
falls short. Unobserved means the evaluator could not tell, and says why.

The record means the set of documents that travel with the work: the bar, who checked the work, what they
found, and who accepted it. The record also names the people involved, and the limits of the process.
Custody means holding the bar and the record, and answering for them. That is why the standard calls it a
custody record.

The disposition means the final decision on the work: given, not yet given, or declined. The approver is
a named person who makes that decision. If some checks were unobserved, the approver must say so in the
decision.

A level is a measure of how much proof the record claims. There are three. CL1 is the basic level. CL2 and CL3 are
stricter. A record can also be a baseline, which means the bar was written after the work. A baseline
record is honest, but it makes no claim about the bar coming first.

The specification means the document that states the rules every record must follow. It is the file named
SPEC.md. You do not need to read it to use this guide.

## What a record tells you

A record answers six questions. You can ask them in this order.

1. **What was made?** The record names the work, and holds a fingerprint of each file. A fingerprint is a
   short code worked out from the file itself. If the file changes, the fingerprint no longer matches.
2. **What was it measured against?** The record holds the bar, the time it was fixed, and the time the
   work started. It shows who approved it, and when.
3. **Who made it?** The record names the maker, and says whether it was a person, an AI model or a
   script. If it was an AI model, it names the model.
4. **Who checked it, and were they independent?** The record lists every evaluator, and what kind each one
   is. It says if an evaluator is a fresh session of the same AI model that made the work.
5. **What did they find?** The record lists every check, with its outcome and its evidence.
6. **Who accepted it, and on what terms?** The record holds the disposition, the approver's name, and the
   time. It lists any unobserved parts the approver accepted.

A good record also lists its own weak spots. These are called separation gaps. A separation gap is a
place where the people who should be kept apart were not. For example, one person may have written the
bar and also made the work. A record that lists its gaps is being honest with you. A record with no gaps
at all deserves a second look.

## Ask for the plain view

Records are written in a computer format, so they can be hard to read as they are. The standard comes
with a small program that prints any record in plain words. It follows the six questions above, in the
same order, and ends with the checker's answer. It only reports what the record says. Ask whoever sends
you a record to send its plain view too. They run `python3 tools/explain.py` on the record.

## How the free checker helps

The standard comes with a free program, the checker. It reads a record and says whether the record holds
up against the rules. You can ask anyone with a computer to run it for you. It gives one of three answers.

- **OK** means the record follows every rule it was checked against. It also says which level the record
  reached.
- **FAILED** means the record breaks at least one rule. It names the rule.
- **NOT-CHECKABLE** means the record points to something the checker could not see. This is often
  evidence kept outside the record. It names what is missing.

The checker also says where the record should go next. "To approver" means a person still needs to look
at something. "Acknowledged" means some parts were unobserved, and the approver has already named them
and decided anyway. Read what the approver said about them.

An OK from the checker means the record is complete and honest about itself. It does not mean the work
is good. Only the checks, read against the bar, can tell you that.

## Questions to ask before you sign off

You can sign off on work when these answers satisfy you.

1. Was the bar written and approved before the work started? Look at the dates. The plain view says
   whether the bar was fixed before, at the same moment as, or after the work started.
2. Does the bar say what you care about? If something important is missing from it, no check can cover
   it.
3. Was each part of the bar read by someone who did not make the work?
4. Did any check fall short, or go unobserved? If so, what did the approver say about it?
5. Did the process show it could catch problems? Good records include planted tests. These are copies of
   the work with a known flaw added on purpose. The checks should have caught them.
6. Are the separation gaps ones you can live with?
7. Did the checker say OK?

You do not need every answer to be perfect. You need to know what the answers are, and be willing to put
your name to them.

## Warning signs

Slow down if you see any of these.

- The bar was fixed after the work was made, but the record does not say baseline.
- Every check conforms, but there are no planted tests.
- The only evaluators are sessions of the maker's own AI model, and the record claims more than CL1.
- Unobserved checks, and an approver who does not mention them.
- A record that lists no gaps at all.
- Claims about the work that no check supports.

## What a record cannot tell you

A record shows how the work was judged. It cannot make a weak bar strong. If the bar asks for the wrong
things, the work can meet it and still not serve you. That is why the bar comes first, and why you
should read it.

A record also cannot see what nobody looked at. Unobserved means just that. The standard makes those
parts visible, so that a person decides about them on purpose.

## Where to find more

- [GLOSSARY.md](GLOSSARY.md) explains every word the specification uses, in plain language.
- [README.md](../README.md) says what the standard is, who it is for, and its current state.
- [SPEC.md](../SPEC.md) holds the rules themselves.
