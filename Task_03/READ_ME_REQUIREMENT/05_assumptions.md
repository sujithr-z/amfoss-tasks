&#x20;\*\*Assumptions I Made (the real ones, no cap)\*\*



\*\*1. The gate should work both ways\*\*

Docs never actually said "V1 blocks V2" but like... V2 was already blocking non-V2? So we just assumed symmetry is a thing. If a door locks from one side it should probably lock from the other too. Made a test for it so we're not just trusting vibes.



\*\*2. Pipeline order wasnt our idea\*\*

Didnt just make up the migrate → check → register → save flow. Its literally in the architecture diagrams. The code was just built different (wrong). We restored what was already supposed to be there, not invented some new pipeline because we felt creative.



\*\*3. JSON format because the scripts wanted it\*\*

Couldve used something cooler but `verify.sh` and the tests were already married to pretty-printed JSON. No point being quirky about file formats when the tooling has expectations. We just gave the people what they wanted.



\*\*4. Left configs alone\*\*

Ports, client limits, legacy flags — all untouched. If it wasnt broken we didnt touch it. The assignment was "fix whats broken" not "redesign the whole thing because youre bored." Minimal changes only. Less is more fr.

