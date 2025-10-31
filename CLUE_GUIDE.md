# Clue Design & Interpretation Guide

---

## Part 1: Clue Design - Avoid Revealing Too Much

### The Core Principle

Each clue should reveal **ONE puzzle piece**, not multiple. Players must find multiple clues to solve the mystery. This creates mystery progression and prevents players from solving everything from one document.

### What is a "Puzzle Piece"?

A puzzle piece is a discrete fact, observation, or connection needed to solve part of the mystery.

**Examples of puzzle pieces:**
- Raw evidence (ingredient list, order dates)
- Character analysis of that evidence
- A specific connection showing WHO did something
- A specific connection showing WHY someone did it
- A specific connection showing HOW something happened
- Confirmation of an outcome

---

### BAD: Too Much in One Clue

```json
{
  "document": {
    "id": "pharmacy_orders",
    "content": "[Large ingredient ledger with dates and quantities]",
    "character_interpretations": {
      "professor": "The foxglove purchases prove Thaddeus was planning to poison Cordelia. Here's the evidence of premeditation..."
    }
  }
}
```

**Problem:** The clue contains:
- ✓ Puzzle piece 1: Raw evidence (ingredient list)
- ✓ Puzzle piece 2: Character analysis (foxglove is unusual)
- ❌ Puzzle piece 3: WHO did it (Thaddeus ordered it)
- ❌ Puzzle piece 4: WHAT he did (poisoning)
- ❌ Puzzle piece 5: WHEN (planning premeditation)

**Result:** Players solve the mystery from ONE clue. No mystery!

---

### GOOD: Spread Across Multiple Clues

**Clue 1: Pharmacy Orders Document**
```json
{
  "content": "[Ingredient ledger showing foxglove purchases on Aug 12 and Sept 1]",
  "reveals": "Shows foxglove was purchased in multiple quantities",
  "interpretations": {
    "professor": "The foxglove purchases are unusual. According to my ancestor's records, Sebastian never discussed foxglove in his approved formula. Yet here he is purchasing it. The pattern is noteworthy."
  }
}
```

Reveals: Raw evidence + observation that it's unusual. **Players must find more clues.**

---

**Clue 2: Loose Handwritten Note** (separate document)
```json
{
  "content": "Sebastian - need more concentrated foxglove extract for my cardiac cases. Can you prepare another batch? - Thaddeus",
  "reveals": "A routine pharmaceutical request",
  "interpretations": {
    "fiduciary": "A straightforward pharmaceutical request. Foxglove was a standard cardiac medicine in the 1920s—widely used and perfectly legal."
  }
}
```

Reveals: WHO requested it + context that it's normal. **Still no smoking gun.** Players must combine evidence.

---

**Clue 3: Hartley's Consultation Notes** (separate)
```json
{
  "content": "[Consultation records about the formula]",
  "reveals": "The approved formula was safe and contained no foxglove",
  "interpretations": {
    "fiduciary": "Hartley's documentation creates a baseline—this was what the formula WAS SUPPOSED to be"
  }
}
```

Reveals: The original formula didn't have foxglove. **Now players can start connecting.**

---

**Clue 4: Autopsy Report** (later discovery)
```json
{
  "reveals": "Toxicology shows foxglove compounds in the victims' systems",
  "interpretations": {
    "doctor": "The toxicology reveals cardiac glycosides—foxglove compounds. This wasn't in the approved formula."
  }
}
```

Reveals: Foxglove WAS in their bodies. **Now players can deduce substitution.**

---

**Result:** Players must find and combine 4+ clues to realize:
1. Foxglove was purchased
2. It was requested by Thaddeus
3. It wasn't in the approved formula
4. It WAS in the victims' bodies
5. Therefore: **Someone substituted it**

---

### How to Identify Bundling Problems

Ask yourself:

**Does this single clue answer more than ONE of these questions?**

1. WHAT happened? (the action/crime)
2. WHO did it? (the perpetrator)
3. WHY did they do it? (motive)
4. HOW did they do it? (means/method)
5. WHEN did it happen? (timeline)
6. WHERE does it point? (location/evidence source)

If yes, **SEPARATE IT into multiple clues.**

---

### Examples of Proper Separation

#### ❌ BAD: Single clue revealing multiple pieces
> "Dr. Thaddeus's desperate attempt to poison Cordelia is shown by his purchase of foxglove on September 1st, just before she began drinking the elixir on September 4th."

Reveals: WHO + WHAT + WHEN + HOW

#### ✅ GOOD: Separated into multiple clues

**Clue A:** Pharmacy orders showing foxglove purchase (WHAT was purchased)
**Clue B:** Handwritten request showing it was Thaddeus (WHO requested it)
**Clue C:** Pocket watch with Sept 4 engraved (WHEN - timing observation)
**Clue D:** Hartley's notes showing original formula had no foxglove (HOW substitution happened)
**Clue E:** Autopsy showing foxglove in bodies (WHAT ended up in victims)

---

### Red Flags: Bundling Problems

- ❌ A clue + interpretation that directly solves WHO committed the crime
- ❌ A clue that shows both the evidence AND what someone did with it
- ❌ Multiple character observations each revealing different mystery pieces
- ❌ An interpretation that connects unrelated clues together
- ❌ A single clue proving motive + means + opportunity

---

## Part 2: Character Interpretations - Avoid Story Knowledge

