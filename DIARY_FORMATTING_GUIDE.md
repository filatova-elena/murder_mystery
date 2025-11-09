# Diary Entry Formatting Guide
## Murder Mystery Book

---

## TYPE 1: FULL DIARY ENTRIES

**Definition:** Entire entry is a diary entry (first-person, from diary perspective)

### JSON Structure:
```json
{
  "date": "YYYY-MM-DD or Month DD, YYYY",
  "location": "[Diary Name]",
  "title": "[Entry Title or Topic]",
  "content": "<i>[Full diary entry text here]</i>"
}
```

### Key Points:
- **location** field = The name of the diary (e.g., "Eleanor's Diary", "Cordelia's Diary", "Sebastian's Notebook")
- **content** = Wrapped entirely in `<i></i>` tags (italics)
- These are introspective, personal reflections
- First-person perspective

### Example:

```json
{
  "date": "1939-07-05",
  "location": "Eleanor's Diary",
  "title": "The Gift",
  "content": "<i>Mother gave me a small box today when I turned fifteen. She said I was old enough to understand. Inside were photographs—a woman with dark hair and sad eyes, beautiful in a way that made my chest ache.\n\n'This is your birth mother,' Mother explained. 'She loved you very much. She wasn't able to raise you, but she wanted you to know what she looked like. To know she hadn't forgotten.'\n\nFather looked uncomfortable. He left the room.\n\nI stared at the photograph for hours. The woman looked lonely.\n\nI also saw a letter addressed to me, in a handwriting I didn't recognize. I opened it. Inside was a recipe.\n\nRose bread.\n\nThe note read: 'From a friend of your mother's. She wanted you to have this. It was her favorite!' I will make this recipe, it's my only connection to her.</i>"
}
```

### Entries of This Type in Narrative:

1. **July 5, 1939** - Eleanor's Diary - "Mother gave me a small box..."
2. **December 10, 1946** - Eleanor's Diary - "Today I stood in the bakery..."
3. **October 15th, 1923** - Cordelia's Diary - "My heart is like a wounded bird..."
4. **December 7, 1923** - Cordelia's Diary - "Mother knows..."
5. **March 15, 1925** - Cordelia's Diary - "Alice / She came to the garden..."
6. **June 5, 1925** - Cordelia's Diary - "I could not believe what I saw today..."
7. **June 5, 1925 (continued)** - Cordelia's Diary - "There was something in the way..."
8. **September 4, 1925** - Cordelia's Diary - "This morning, Sebastian gave me the elixir..."
9. **October 5, 1925** - Cordelia's Diary - "I've been feeling strange..."
10. **October 8, 1925** - Cordelia's Diary - "Sebastian came to see me..."
11. **October 12, 1925** - Cordelia's Diary - "Sebastian is dead..."
12. **October 13, 1925** - Cordelia's Diary - "I learned today that Alice is dead..."
13. **October 14, 1925** - Cordelia's Diary - "I can barely leave my bed..."

---

## TYPE 2: EMBEDDED DIARY ENTRIES

**Definition:** Diary entry embedded within narrative prose; diary excerpt is part of a larger scene/narrative

### JSON Structure:
```json
{
  "date": "YYYY-MM-DD or Month DD, YYYY",
  "location": "[Location in narrative - NOT diary name]",
  "title": "<u>[Entry Title or Topic]</u>",
  "content": "[Narrative prose]\n\n<strong><i>[Diary entry excerpt]</i></strong>\n\n[More narrative prose if applicable]"
}
```

### Key Points:
- **location** field = Physical location (e.g., "Sebastian's Laboratory", "Montrose Mansion")
- **title** = Underlined with `<u></u>` tags
- **content** = Mix of narrative and diary
  - Narrative portions = normal text
  - Diary portions = wrapped in `<strong><i></i></strong>` tags (bold italics)
- Provides context around the diary excerpt

### Example:

```json
{
  "date": "1925-08-24",
  "location": "Montrose Mansion",
  "title": "<u>A Moment of Jealousy</u>",
  "content": "Sebastian sat in his laboratory, reviewing accounts from the dressmaker. Elias Monroe had been spending considerable time with Cordelia, and Sebastian's mind turned restless.\n\n<strong><i>Elias Monroe has been spending considerable time with Cordelia on the dress alterations. Fittings, measurements, consultations—it all seems excessive for a wedding dress, even one as elaborate as ours will be.\n\nI know he is a craftsman, meticulous about his work. His reputation is built on perfection. But something in his demeanor troubles me. The way he looks at her when he thinks no one is watching. The way he finds excuses to extend their appointments.\n\nCordelia insists the dress is not yet perfect, that he is merely being thorough. She sees no cause for concern.\n\nBut I have faith in my elixir. I feel us becoming more bound with each passing day. The ritual draws us closer, intertwines our very essences. By the wedding day, she will be mine completely—in ways that no dressmaker's needle can accomplish.</i></strong>\n\nHe set down his pen, trying to shake the feeling of unease."
}
```

### Entries of This Type in Narrative:

**Sebastian's Notebook Entries:**
1. **March 15, 1920** - "First principles..."
2. **July 22, 1923** - "Component mathematics..."
3. **January 7, 1925** - "Cordelia / I saw her today..."
4. **March 14, 1925** - "YES! She said YES!..."
5. **August 24, 1925** - "Elias Monroe has been spending considerable time..."
6. **October 6, 1925** - "Understanding..."

**Dr. Thaddeus Crane's Notebooks/Research Notes:**
1. **October 7, 1925** - Antidote research notes - "Sebastian has ingested foxglove..."
2. **October 9, 1925** - Antidote research notes - "[Handwriting deteriorating]..."
3. **October 11, 1925** - Antidote research notes - "[Barely legible]..."
4. **September 2, 1925** - Dr. Crane's Hidden Diary - "I cannot sleep..."
5. **October 9, 1925** - Dr. Crane's Hidden Diary - "Sebastian is ill..."
6. **October 11, 1925** - Dr. Crane's Hidden Diary - "Sebastian is dead..."
7. **October 17, 1925** - Dr. Crane's Hidden Diary - "Cordelia died this morning..."
8. **October 10, 1925** - Dr. Crane's Hidden Diary - "I cannot continue this deception..."
9. **October 11, 1925** - Dr. Crane's Hidden Diary - "Sebastian is dead. His heart simply stopped..."

**Elias Monroe's Poetry:**
1. **August 20, 1925** - "For Cordelia (Unsent)" - "She turns to roses..."
2. **October 8, 1925** - "Watching Her Fade (Unsent)" - "Watching Her..."

---

## FORMATTING RULES SUMMARY

| Aspect | Full Diary | Embedded Diary |
|--------|-----------|-----------------|
| **Location Field** | Diary name (e.g., "Eleanor's Diary") | Physical location (e.g., "Montrose Mansion") |
| **Title** | Normal text | `<u>Underlined</u>` |
| **Content Wrapper** | `<i>entire content</i>` | Mix of normal + `<strong><i>diary portion</i></strong>` |
| **Perspective** | First-person throughout | Narrative + first-person diary excerpt |
| **Use Case** | Pure introspection | Scene-setting with diary insight |

---

## HTML Tags Quick Reference

```html
<!-- Italics (used for full diary entries) -->
<i>This text is italicized</i>

<!-- Underline (used for embedded diary titles) -->
<u>This text is underlined</u>

<!-- Bold Italics (used for embedded diary excerpts) -->
<strong><i>This text is bold and italicized</i></strong>

<!-- Image tags (if needed for character portraits) -->
<img src="../assets/character_name.png" width="300" height="300" alt="Character Name">
```

---

## Best Practices

1. **Full Diary Entries:**
   - Use for deep introspection
   - When the entire entry is personal reflection
   - Use naturalistic line breaks with `\n\n` for paragraphs

2. **Embedded Diary Entries:**
   - Use to provide context and narrative flow
   - When diary excerpt needs explanation
   - When showing how characters react to diary content
   - Helps maintain story pacing while revealing diary insights

3. **Date Formatting:**
   - Use ISO format in JSON date field: `YYYY-MM-DD` or natural date: `Month DD, YYYY`
   - Always include the format that appears in the narrative

4. **Consistency:**
   - Keep all diary entries from same character using same tone
   - Maintain character voice throughout their entries
   - Use consistent date formatting per chapter

5. **Content Quality:**
   - Preserve original punctuation and voice
   - Use `\n\n` for paragraph breaks in JSON
   - Avoid truncating entries unnecessarily
   - Keep emotional authenticity

---

## Example: Full Chapter Structure

Here's how these two types work together in a chapter:

```json
{
  "entries": [
    {
      "date": "1925-03-15",
      "location": "Sebastian's Notebook",
      "title": "<u>First Principles</u>",
      "content": "Sebastian sat at his workbench, surrounded by botanical specimens...\n\n<strong><i>What is love but chemistry? The ancients knew this—Venus governing desire, the quickening of pulse, the movement of blood toward heat. They poeticized what we may now quantify.</i></strong>\n\nHe closed the notebook, his mind racing with possibilities..."
    },
    {
      "date": "1925-07-05",
      "location": "Sebastian's Notebook",
      "title": "Breakthrough",
      "content": "<i>Months I have been at this. And I understand nothing!\n\nWait—no. I understand EVERYTHING. The mathematics are perfect:\n\nDamiana: 3 parts (desire, heat, awakening)\nValerian Root: 2 parts (calm, trust, grounding)\nRose Otto: 1 drop only (Venus—transcendence)\n\nBut it's MISSING something. The crucial element.</i>"
    }
  ]
}
```

---

## Questions?

When in doubt:
- **Is the entire entry first-person diary?** → Use TYPE 1 (Full Diary)
- **Is the entry part of a larger narrative scene?** → Use TYPE 2 (Embedded Diary)
- **Unsure about formatting?** → Reference the examples above

