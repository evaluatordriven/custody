# Signing: deferred by decision, not by omission — 2026-11-10

**Status:** CL3 is unreachable today, on purpose. No signing tool ships with this repository. That is a
recorded decision with a named trigger, not an unfinished feature and not an oversight.

A reviewer who finds every published record at CL1 should read this file before concluding the author did
not notice. The gap between CL1 and CL3 is one named requirement — `CL3-3` — and it is unmet deliberately.

## What CL3-3 asks, and why we have not built it

`SPEC.md` §5.4 requires a **Sigstore bundle** over the record as a DSSE envelope, **logged in Rekor**, and a
verifier that reads `OK` only when it checks the signature, the certificate **and** the log entry.

Reduced to its purpose, the clause buys three things:

1. **A stranger can verify without asking the author.** No key hand-delivered out of band.
2. **An outside anchor for "when".** Without it, "the bar came first" is self-attested, and a record can be
   signed today and presented as signed last month.
3. **Append-only.** The attestation cannot be quietly replaced later by whoever holds commit access.

Properties 2 and 3 come from the **witness** — an append-only log that timestamps the bytes and issues a
proof anyone can check. Sigstore happens to bundle a signature and a witness into one artifact. The witness
is the requirement; Sigstore is one implementation of it, and the one the SPEC names.

## The alternatives weighed, and why each stops short

| Option | Signature | Identity | Outside "when" | Append-only | Verdict |
|---|---|---|---|---|---|
| `ssh-keygen -Y sign` | yes | via published keys | **no** — signer's own clock | **no** | half an attestation |
| PGP with a registered key | yes | yes (email-verified keyservers, WKD) | **no** unless a TSA is added | **no** | better identity, same hole |
| PGP + RFC 3161 timestamp | yes | yes | yes (public TSA) | partial | meets the spirit; does not publish the digest |
| Sigstore keyless | yes | yes (OIDC certificate) | yes (Rekor) | yes | meets the clause and the spirit |

The one case where the PGP + timestamp path is *better*: it does not publish the record's digest to a
permanent public ledger, so an attestation can exist for a record whose existence should not be world
readable. If that requirement ever appears, the design changes to that path and the SPEC with it — as a
deliberate amendment, with the reason recorded here first.

## Why not a weaker signature at CL2

Offered and rejected. CL2 is a claim about **evaluator independence** (`CL2-1` runs, `CL2-2` read-only,
`CL2-3` maker separation). No CL2 requirement concerns signatures, and `external[]` admits only `CL1-15`,
`CL2-4` and `CL3-3` as requirement names — so an ssh signature has no home in the record at CL2.

Beyond the schema, a lower-tier signature would be **a false floor**: a record that looks more attested
than an unsigned one while lacking the outside anchor that is the entire point. This project's standing rule
is that a prompted model promises and a configured instance enforces; a signature that cannot testify to
when is a promise wearing an attestation's clothes.

**What is legitimate instead:** signing release artifacts (tarballs, tags) with `ssh-keygen -Y sign`, or any
signature kept **outside** the custody record for a purpose other than CL3 — artifact integrity, release
provenance. That is honest, it is cheap, and nobody can mistake it for a CL3 claim, because it never enters
`external[]` and never raises `levelClaimed`.

## The trigger

Build the signing path when **any** of these is true, and not before:

1. A reviewer, adopter or buyer asks for a verified signature — that is demand, and it is the reason the
   standard exists.
2. A record must prove the bar preceded the work to someone who does not trust the author. That is CL3's
   actual use, and it arrives with the first outside job.
3. An outside party agrees to be the `readBy` for the bundle. `CL3-3` is unmeetable without one, and
   synthesising a reader would be the worst possible answer.

Until then the honest state is: signed nothing, claiming CL1, saying so.

## What we will not do

- Change `CL3-3` to match a cheaper tool. A standard that moves to its tooling stops being a standard.
- Ship an unlogged bundle and let a verifier read `OK`.
- Add a "signed" flag at CL1 or CL2 so a record can look attested without being so.
- Imply that a signature, once it exists, means the reading was honest. It does not. It means the bytes are
  the bytes and someone outside the author said when.
