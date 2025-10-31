# Quick Reference Card

## 🎯 One-Page Guide to The Crimson Murder

### Start Here
- **Main URL**: `/index.html` (character selection)
- **Local Testing**: `python -m http.server 8000` then `http://localhost:8000`

---

## 👥 Characters (12 total)

```
Art Collector      Baker              Clockmaker         Dressmaker
Explorer           Fiduciary          Heiress            Influencer
Mortician          Professor          Psychic            Doctor
```

**Each character page**: `/character/{name}.html`
- Confirms role selection
- Stores character in localStorage

---

## 👁️ Visions (3 total - Alice implemented)

| Vision | Location | Full | Partial | Blocked |
|--------|----------|------|---------|---------|
| **Alice** | `/vision/alice.html` | ✅ 11 visions | ✅ 11 visions | ✅ Generic msg |
| **Cordelia** | `/vision/cordelia.html` | ⏳ Template | ⏳ Template | ✅ Generic msg |
| **Sebastian** | `/vision/sebastian.html` | ⏳ Template | ⏳ Template | ✅ Generic msg |

### Who Sees What?
- **Psychic** → FULL visions
- **Baker** → PARTIAL (fragmented) visions
- **Everyone Else** → BLOCKED (generic message)

### Vision Cycling
- Each scan increments counter (1 → 2 → 3... → 11 → 1)
- Independent for each spirit
- Counter stored: `vision_{name}_number`

---

## 🔧 Key Functions

```javascript
// Character Management
getCharacter()                              // Returns: 'psychic'
setCharacter('baker')                       // Sets character

// Vision Control
getVisionAccessLevel('psychic', 'alice')    // Returns: 'FULL'
getNextVisionNumber('alice', 11)            // Returns: 1, then 2, 3...
resetVisionCounter('alice')                 // Clears counter

// Validation
checkCharacterSelected('../index.html')     // Auto-redirect if no character
```

---

## 📱 Mobile Experience

### Player Flow
1. **Scan Character QR** → Character page loads → Stores identity
2. **Click "Begin Investigation"** → Back to main page
3. **Scan Vision QR** → Shows vision content → Counter increments
4. **Scan Clue QR** → Shows base + expert info

### Tested Devices
- ✅ iPhone 12+ with Safari
- ✅ Android with Chrome
- ✅ Tablet browsers
- ✅ Mobile landscape orientation

---

## 🎨 Styling

### Colors
```css
Dark Background:     #0a0a0a
Secondary Dark:      #1a1a2e
Gold Accent:         #d4a574
Purple Accent:       #4a148c
Text Light:          #e0e0e0
```

### Responsive Sizes
- **Desktop**: Full layout
- **Tablets** (≤600px): Smaller text/padding
- **Mobile** (≤400px): 2-column grid, minimal padding

---

## 📂 File Organization

```
Core:
  index.html              Main landing page
  assets/style.css        All styling (responsive)
  assets/script.js        All functions

Characters (12 files):
  character/*.html        Each stores character name

Visions (3 files):
  vision/alice.html       ✅ Complete (11 visions)
  vision/cordelia.html    ⏳ Template ready
  vision/sebastian.html   ⏳ Template ready

Clues (expand as needed):
  clue/template.html      Example with all characters

Documentation:
  README.md               Full guide
  SETUP.md                Quick start & testing
  PROJECT_SUMMARY.md      Complete feature list
  QUICK_REFERENCE.md      This file
```

---

## 💾 localStorage Keys

```javascript
localStorage.getItem('characterName')       // Current character
localStorage.getItem('vision_alice_number')     // Alice counter
localStorage.getItem('vision_cordelia_number')  // Cordelia counter
localStorage.getItem('vision_sebastian_number') // Sebastian counter
```

**Reset Everything:**
```javascript
localStorage.clear()
```

---

## 🚀 Deployment Checklist

- [ ] Test all character pages load
- [ ] Test all vision pages (with different characters)
- [ ] Test vision cycling (11 times)
- [ ] Test on mobile device
- [ ] Generate QR codes
- [ ] Print and laminate QR codes
- [ ] Test QR codes with phone camera
- [ ] Have backup URLs written down
- [ ] Deploy to hosting (GitHub Pages/Netlify/etc)
- [ ] Test links on deployed site
- [ ] Brief players on process

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Character doesn't persist | Check localStorage enabled (F12 → Storage) |
| Vision doesn't increment | Reload page, check counter value |
| CSS doesn't load | Ensure running through server (not file://) |
| Mobile looks broken | Test in DevTools device emulation |
| QR code doesn't scan | Try manual URL entry, test QR code |

---

## ✏️ Quick Customizations

### Change Title
Edit `index.html`:
```html
<h1>The Crimson Murder</h1>  ← Change this
```

### Add New Character
1. Create `character/name.html` (copy baker.html)
2. Update `setCharacter('name')`
3. Add link in `index.html`

### Add Vision Content
1. Open `vision/cordelia.html`
2. Replace `fullVisions` array (11 items)
3. Replace `partialVisions` array (11 items)

### Add Clue
1. Create `clue/name.html` (copy template.html)
2. Update `expertInfo` object (all 12 characters)
3. Link from vision page

---

## 📞 Help Resources

- **Getting Started**: See SETUP.md
- **Full Features**: See README.md
- **What's Done**: See PROJECT_SUMMARY.md
- **Browser Issues**: Check browser console (F12)
- **localStorage Debug**: `localStorage` in console
- **Mobile Test**: DevTools → Device Toolbar (F12)

---

## 🎭 Game Theory

### Info Distribution
```
Psychic:    Gets FULL truth through visions
Baker:      Gets emotional impressions  
Others:     Must gather from clues & collaboration
```

### Victory Condition
Players piece together truth by:
1. Collecting visions (different per character)
2. Finding clues (base + expert info)
3. Sharing information
4. Deducing who committed the crime

---

## ⏱️ Timeline

**Setup**: 5-10 minutes
- [ ] Start local server
- [ ] Test on one device
- [ ] Generate QR codes

**During Event**: Ongoing
- [ ] Players scan character QR (5 min)
- [ ] Players investigate for 30-60 min
- [ ] Deduction phase (15-30 min)

---

**Questions?** Check the documentation files or review the source code. Everything is commented and well-organized!

🔍 **Happy investigating!** ✨
