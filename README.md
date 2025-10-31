# The Lost Souls of Kennebec Avenue Investigation - QR Code System

A gothic-themed, mobile-first web application for hosting a The Lost Souls of Kennebec Avenue party game with QR code scanning mechanics.

## Project Overview

Players navigate through an interactive mystery investigation where they:
1. **Select a character** by scanning their character QR code
2. **Investigate clues** unique to their character's expertise
3. **Receive visions** from the spirit world, with content varying by character role
4. **Piece together** the truth about "The Crimson Murder"

## Features

### Character System
- **12 Playable Characters** with unique perspectives:
  - Art Collector, Baker, Clockmaker, Dressmaker
  - Explorer, Fiduciary, Heiress, Influencer
  - Mortician, Professor, Psychic, Doctor

- Character identity stored in `localStorage` for persistence
- Each character has a dedicated identity page that explains their role

### Vision System
- **Three Spirit Characters**: Alice, Cordelia, Sebastian
- **Dynamic Access Levels**:
  - **FULL ACCESS**: Psychic (see complete visions)
  - **PARTIAL ACCESS**: Baker (see fragmented/emotional versions)
  - **BLOCKED**: Other characters (generic message only)

- **11 Cycling Visions** per spirit
- Each QR scan increments the vision counter
- Counter loops back to Vision 1 after Vision 11
- Vision progress tracked in `localStorage`

### Design
- **Gothic 1920s Art Deco Theme**:
  - Dark color scheme (blacks, deep purples)
  - Gold accents for elegance
  - Cream text on dark backgrounds
  - Responsive, mobile-first design

- **Mobile-Optimized**: Perfect for phone-based QR scanning

## File Structure

```
murder_mystery/
├── index.html                 # Landing page with character selection
├── README.md                  # This file
├── character/
│   ├── artcollector.html
│   ├── baker.html
│   ├── clockmaker.html
│   ├── dressmaker.html
│   ├── explorer.html
│   ├── fiduciary.html
│   ├── heiress.html
│   ├── influencer.html
│   ├── mortician.html
│   ├── professor.html
│   ├── psychic.html
│   └── doctor.html
├── vision/
│   ├── alice.html             # Complete with 11 cycling visions
│   ├── cordelia.html          # Placeholder - ready for content
│   └── sebastian.html         # Placeholder - ready for content
├── clue/                      # Directory for clue pages (to be added)
└── assets/
    ├── style.css              # All styling
    └── script.js              # Shared utility functions
```

## How to Use

### For Players

1. **Character Selection**: Navigate to the index page and click on your assigned character
   - This stores your character identity in localStorage
   - Shows confirmation of your role

2. **Begin Investigation**: Click "Begin Investigation" to return to the main page
   - You can now scan clue QR codes throughout the venue

3. **Scan Vision QR Codes**: When you encounter a vision QR code:
   - Navigate to the vision page (e.g., `/vision/alice.html`)
   - The first scan shows Vision 1
   - Each subsequent scan shows the next vision in sequence
   - After Vision 11, the counter resets to Vision 1

4. **View Your Information**: Your character role determines what you see:
   - **Psychic**: Full, detailed visions
   - **Baker**: Fragmented, emotion-based visions
   - **Others**: Generic message about the spirit

### For Organizers

#### To Change A Player's Character
Players can visit any character page to change their role:
```
example.com/character/psychic.html  # Switch to Psychic
example.com/character/baker.html    # Switch to Baker
```

#### To Reset A Player's Progress
Clear their browser's localStorage:
```javascript
localStorage.clear()
```

Or specific visions:
```javascript
localStorage.removeItem('vision_alice_number');
localStorage.removeItem('vision_cordelia_number');
localStorage.removeItem('vision_sebastian_number');
```

## Core JavaScript Functions

Located in `assets/script.js`:

- `getCharacter()` - Retrieve current character
- `setCharacter(name)` - Store character identity
- `getVisionAccessLevel(character, vision)` - Determine access level
- `getNextVisionNumber(vision, max)` - Get next vision and increment counter
- `getCurrentVisionNumber(vision)` - Get current vision without incrementing
- `resetVisionCounter(vision)` - Clear vision progress
- `checkCharacterSelected(url)` - Redirect if no character selected
- `formatCharacterName(name)` - Capitalize character name

## Styling

The application uses CSS custom properties (variables) for easy theming:

```css
--primary-dark: #0a0a0a
--secondary-dark: #1a1a2e
--accent-gold: #d4a574
--accent-purple: #4a148c
--accent-cream: #f5f1e8
--text-light: #e0e0e0
```

### Responsive Breakpoints
- **Default**: Full size
- **600px and below**: Reduced padding, adjusted font sizes
- **400px and below**: 2-column character grid, minimal padding

## Adding Content

### Creating a New Vision
1. Create a new file in `/vision/` (e.g., `margaret.html`)
2. Copy structure from `alice.html`
3. Update the `fullVisions` and `partialVisions` arrays
4. Update access levels in `script.js` if needed

### Creating Clue Pages
1. Create files in `/clue/` directory
2. Use same pattern as vision pages:
   - Check character selection
   - Show base information
   - Display expert information based on character expertise

### Modifying Access Levels
Edit the `getVisionAccessLevel()` function in `script.js`:

```javascript
const accessLevels = {
  alice: {
    FULL: ['psychic', 'grandmother'],
    PARTIAL: ['baker', 'professor']
  },
  // Add more as needed
};
```

## Browser Compatibility

- Modern browsers with localStorage support
- Mobile browsers (iOS Safari, Chrome Mobile, etc.)
- Works offline once loaded

## Technical Notes

- **No Framework Dependencies**: Pure HTML/CSS/JavaScript
- **localStorage**: Used for character identity and vision counters
- **Responsive**: Mobile-first design approach
- **Self-Contained**: All assets served locally

## Future Enhancements

Potential features to add:
- Clue pages with character-specific information
- Scoring/progress tracking
- Timer for investigation period
- QR code generation scripts
- Admin dashboard for organizers
- Multi-player shared state (for organizers to track all players)
- Additional characters and visions
- Sound effects and atmospheric audio

## Deployment

### Local Testing
```bash
# Simple Python server
python -m http.server 8000

# Or Node.js
npx serve
```

### Production
- Deploy to any static hosting (GitHub Pages, Netlify, Vercel, etc.)
- No backend required
- No database needed

## Game Design Notes

The mystery is designed so that:
- Each character gains information appropriate to their role
- Psychic gets the full truth through visions
- Baker gets emotional impressions through partial visions
- Other characters must gather information through clues and observation
- Collaboration between characters reveals the complete story

---

**Created**: October 2025
**Theme**: 1920s Gothic Mystery
**Technology**: HTML5, CSS3, JavaScript (Vanilla)
