#!/usr/bin/env bash
# =============================================================================
#  c2_52_setup.sh  --  C2-52 regeneration: non-interactive setup + verification
#  BioAegis / BioScyde (St. Paul's College, Hong Kong) -- iGEM 2026 Modeling
#
#  WHAT IT DOES (nothing irreversible, nothing network-facing):
#    1. writes frozen_core_52.txt   (all 52 MD-rigid Pocket 1 residues)
#    2. writes frozen_core_21.txt   (the Cycle 1 subset, for diffing only)
#    3. verifies the design-input PDB numbering against the MD numbering
#       by printing the residue identity at every one of the 52 positions
#    4. builds fixed_positions_52.jsonl (via ProteinMPNN's own helper script
#       when it is available, otherwise writes the JSON directly)
#    5. prints a verification block for you to paste back
#
#  USAGE (from inside the C2-52 working directory):
#    bash c2_52_setup.sh /full/path/to/design_input.pdb [CHAIN] [PDB_KEY]
#  e.g.
#    bash c2_52_setup.sh ~/scyE_cycle2/strategyC/scyE_clean.pdb A scyE_clean
#
#  CHAIN   defaults to A        (Cycle 1 used --chain_list "A")
#  PDB_KEY defaults to the PDB filename without .pdb
#          (Cycle 1's fixed_positions.jsonl key was "scyE_clean")
# =============================================================================
set -u

PDB="${1:-}"
CHAIN="${2:-A}"
if [ -z "$PDB" ]; then
  echo "ERROR: give the path to the design-input PDB."
  echo "  bash c2_52_setup.sh ~/scyE_cycle2/strategyC/scyE_clean.pdb A scyE_clean"
  exit 1
fi
if [ ! -f "$PDB" ]; then
  echo "ERROR: no such file: $PDB"
  exit 1
fi
PDB_BASE="$(basename "$PDB" .pdb)"
PDB_KEY="${3:-$PDB_BASE}"

echo "================================================================"
echo " C2-52 setup"
echo " PDB      : $PDB"
echo " chain    : $CHAIN"
echo " jsonl key: $PDB_KEY"
echo " date     : $(date)"
echo " host     : $(hostname)"
echo "================================================================"
echo

# ---------------------------------------------------------------- 1. the lists
# All 52 Pocket 1 residues that the frozen-core script returned as MD-rigid.
cat > frozen_core_52.txt <<'EOF'
34,36,51,65,66,67,68,69,70,71,73,102,108,109,110,111,113,128,130,177,179,181,182,183,197,198,200,231,232,233,242,243,245,247,249,251,266,267,268,269,271,299,314,319,320,323,324,325,328,359,375,376
EOF
# strip the trailing newline so the byte count is comparable with the Cycle 1 file
printf '%s' "$(cat frozen_core_52.txt)" > frozen_core_52.txt

# The 21 residues actually handed to ProteinMPNN in Cycle 1 (frozen_core.txt, 80 bytes).
printf '%s' "34,36,51,109,111,113,128,181,182,197,198,200,249,251,266,267,299,314,319,375,376" > frozen_core_21.txt

echo "--- 1. frozen core files written ---"
printf 'frozen_core_52.txt : %s bytes   (expect 196)\n' "$(wc -c < frozen_core_52.txt | tr -d ' ')"
printf 'frozen_core_21.txt : %s bytes   (expect 80, matches the Cycle 1 file size on record)\n' "$(wc -c < frozen_core_21.txt | tr -d ' ')"
printf 'count in 52 file   : %s residues (expect 52)\n' "$(tr ',' '\n' < frozen_core_52.txt | grep -c .)"
printf 'count in 21 file   : %s residues (expect 21)\n' "$(tr ',' '\n' < frozen_core_21.txt | grep -c .)"
echo

# ----------------------------------------------- 2. numbering verification step
# THIS IS THE STEP THAT CATCHES A RENUMBERED PDB. The 52 numbers are in the
# MD/pocket numbering of the 403-residue construct: signal peptide 1-22,
# mature body 23-397, His6 tag 398-403. If the design-input PDB was renumbered
# (e.g. mature-only, or starting at 1 after the leader was stripped), these
# numbers point at the WRONG residues and the whole run is silently wrong.
python3 - "$PDB" "$CHAIN" <<'PYEOF'
import sys, collections

pdb, chain = sys.argv[1], sys.argv[2]

three2one = {
 'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G',
 'HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S',
 'THR':'T','TRP':'W','TYR':'Y','VAL':'V','MSE':'M','HID':'H','HIE':'H','HIP':'H',
 'CYX':'C','CYM':'C','HSD':'H','HSE':'H','HSP':'H',
}

res = {}       # resseq -> resname
order = []
for line in open(pdb):
    if not line.startswith(('ATOM  ', 'HETATM')):
        continue
    if line[21] != chain:
        continue
    icode = line[26].strip()
    try:
        num = int(line[22:26])
    except ValueError:
        continue
    name = line[17:20].strip()
    key = num
    if key not in res:
        res[key] = (name, icode)
        order.append(key)

if not res:
    print("!! NO residues found for chain '%s' in %s" % (chain, pdb))
    print("!! Chains present:", sorted({l[21] for l in open(pdb)
          if l.startswith(('ATOM  ','HETATM'))}))
    sys.exit(2)

nums = sorted(res)
print("--- 2. numbering verification ---")
print("chain %s: %d residues, numbering %d..%d" % (chain, len(res), nums[0], nums[-1]))
print()

# --- gate 2a: the construct should be the 403-residue one the MD used
if len(res) == 403 and nums[0] == 1 and nums[-1] == 403:
    print("GATE 2a  PASS   403 residues numbered 1-403: matches the MD construct.")
else:
    print("GATE 2a  CHECK  expected 403 residues numbered 1-403 (the MD construct:")
    print("                signal peptide 1-22, His6 398-403). Got %d residues, %d..%d."
          % (len(res), nums[0], nums[-1]))
    print("                DO NOT GENERATE until this is understood. If this PDB is")
    print("                mature-only or renumbered, the 52 numbers must be mapped")
    print("                onto it first (offset or alignment), not used as-is.")
print()

# --- gate 2b: the His6 tag must read HHHHHH at 398-403
tag = ''.join(three2one.get(res[i][0], 'X') for i in range(398, 404) if i in res)
if tag == 'HHHHHH':
    print("GATE 2b  PASS   residues 398-403 read '%s' -> the His6 tag is where the MD"
          % tag)
    print("                numbering says it is. This is the strongest single check.")
else:
    print("GATE 2b  FAIL   residues 398-403 read '%s', expected 'HHHHHH'." % (tag or '(absent)'))
    print("                The PDB numbering does NOT line up with the MD numbering.")
    print("                STOP HERE and send this output back.")
print()

# --- gate 2c: the Cys62 / Cys74 pair the MD topology linked
c62 = three2one.get(res.get(62, ('?',''))[0], '?')
c74 = three2one.get(res.get(74, ('?',''))[0], '?')
if c62 == 'C' and c74 == 'C':
    print("GATE 2c  PASS   62 and 74 are both CYS -- the disulfide pair pdb2gmx linked")
    print("                (CYS62 SG - CYS74 SG) is at the expected numbers.")
else:
    print("GATE 2c  FAIL   residue 62 = '%s', residue 74 = '%s'; expected C and C." % (c62, c74))
    print("                Numbering is shifted. STOP HERE.")
print()

# --- gate 2d: identity at every one of the 52 frozen positions
fc = [int(x) for x in open('frozen_core_52.txt').read().strip().split(',')]
fc21 = set(int(x) for x in open('frozen_core_21.txt').read().strip().split(','))
missing = [r for r in fc if r not in res]
print("--- 2d. residue identity at all 52 frozen positions ---")
print("(C1 = also frozen in Cycle 1's 21-residue subset; NEW = newly frozen in C2-52;")
print(" FLEX = fails the 0.15 nm cutoff on the System B production trajectory)")
print()
flex_on_production = {65, 66, 67, 68, 69, 70, 71, 233, 242}
print("  num  res  1L  status")
for r in fc:
    if r not in res:
        print("  %3d  ---  -   MISSING FROM PDB" % r)
        continue
    name, icode = res[r]
    one = three2one.get(name, 'X')
    tags = []
    tags.append("C1" if r in fc21 else "NEW")
    if r in flex_on_production:
        tags.append("FLEX")
    if icode:
        tags.append("insertion-code '%s'" % icode)
    print("  %3d  %-3s  %s   %s" % (r, name, one, ' '.join(tags)))
print()
if missing:
    print("GATE 2d  FAIL   %d of the 52 positions are absent from chain %s: %s"
          % (len(missing), chain, missing))
    print("                STOP HERE and send this output back.")
else:
    print("GATE 2d  PASS   all 52 positions exist in chain %s." % chain)
print()

# --- 2e: the His314 sanity check, named explicitly in the team's records
h314 = three2one.get(res.get(314, ('?',''))[0], '?')
if h314 == 'H':
    print("GATE 2e  PASS   residue 314 is HIS -- the His314 our records name repeatedly")
    print("                (ESM-IF1 mutated it to Met; Strategy D displaced it 23.4 A).")
else:
    print("GATE 2e  FAIL   residue 314 = '%s', expected H (HIS). Numbering is shifted." % h314)
print()

# one-line digest for pasting back
seq52 = ''.join(three2one.get(res[r][0], 'X') if r in res else '-' for r in fc)
print("52-position identity string (paste this back):")
print("  " + seq52)
print()
PYEOF
PYRC=$?
if [ "$PYRC" -ne 0 ]; then
  echo "!! verification step failed (exit $PYRC). Do NOT continue to generation."
  exit "$PYRC"
fi

# ------------------------------------------------- 3. build fixed_positions JSONL
echo "--- 3. fixed-positions JSONL ---"
POSLIST="$(tr ',' ' ' < frozen_core_52.txt)"

if [ -n "${PMPNN_DIR:-}" ] && [ -f "$PMPNN_DIR/helper_scripts/make_fixed_positions_dict.py" ] \
   && [ -f "./parsed_pdbs.jsonl" ]; then
  echo "Using ProteinMPNN's own helper (the Cycle 1 route)."
  python3 "$PMPNN_DIR/helper_scripts/make_fixed_positions_dict.py" \
    --input_path  "./parsed_pdbs.jsonl" \
    --output_path "./fixed_positions_52.jsonl" \
    --chain_list "$CHAIN" \
    --position_list "$POSLIST"
  echo "Wrote fixed_positions_52.jsonl via make_fixed_positions_dict.py"
else
  echo "ProteinMPNN helper or parsed_pdbs.jsonl not available here;"
  echo "writing the JSONL directly in the same format Cycle 1 produced."
  python3 - "$PDB_KEY" "$CHAIN" <<'PYEOF2'
import sys, json
key, chain = sys.argv[1], sys.argv[2]
fc = [int(x) for x in open('frozen_core_52.txt').read().strip().split(',')]
with open('fixed_positions_52.jsonl', 'w') as f:
    f.write(json.dumps({key: {chain: fc}}) + "\n")
print("Wrote fixed_positions_52.jsonl")
PYEOF2
fi
echo
echo "contents of fixed_positions_52.jsonl:"
cat fixed_positions_52.jsonl
echo
echo "NOTE: the key above must match the key ProteinMPNN uses for this PDB in"
echo "      parsed_pdbs.jsonl. Cycle 1's key was \"scyE_clean\". Check with:"
echo "      python3 -c \"import json;print(list(json.loads(open('parsed_pdbs.jsonl').readline()).keys()))\""
echo

# --------------------------------------------------------------- 4. diff summary
echo "--- 4. what changed versus Cycle 1 ---"
python3 - <<'PYEOF3'
a = [int(x) for x in open('frozen_core_52.txt').read().strip().split(',')]
b = [int(x) for x in open('frozen_core_21.txt').read().strip().split(',')]
new = sorted(set(a) - set(b))
print("Cycle 1 frozen : %d residues" % len(b))
print("C2-52 frozen   : %d residues" % len(a))
print("newly frozen   : %d residues" % len(new))
print("  " + ", ".join(str(x) for x in new))
assert set(b) <= set(a), "the 21 are NOT a subset of the 52 -- something is wrong"
print("subset check   : OK, all 21 Cycle 1 residues are inside the 52")
PYEOF3
echo
echo "================================================================"
echo " SETUP DONE. Files in $(pwd):"
ls -la frozen_core_52.txt frozen_core_21.txt fixed_positions_52.jsonl 2>/dev/null
echo
echo " Send back: the whole output above (gates 2a-2e, the identity table,"
echo " the 52-position identity string, and the JSONL contents)."
echo " Do NOT run generation until the gates read PASS."
echo "================================================================"
