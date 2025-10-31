# Quick Start Guide - The Lost Souls of Kennebec Avenue

## Getting Started

### 1. Running Locally

#### Option A: Python (Recommended for Mac/Linux)
```bash
cd /Users/elenafilatova/code/murder_mystery
python -m http.server 8000
```
Then visit: `http://localhost:8000`

#### Option B: Node.js
```bash
npm install -g serve
cd /Users/elenafilatova/code/murder_mystery
serve
```

#### Option C: VS Code Live Server
- Install "Live Server" extension in VS Code
- Right-click on `index.html` → "Open with Live Server"

---

## Testing the Game Flow

### Test Path 1: Psychic Character (Full Vision Access)
1. Visit `http://localhost:8000/character/psychic.html`
2. Click "Begin Investigation"
3. Open `http://localhost:8000/vision/alice.html` multiple times
4. **Expected**: You should see detailed visions, incrementing from 1-11
5. After vision 11, it loops back to 1

### Test Path 2: Baker Character (Partial Vision Access)
1. Clear browser storage: Open DevTools → Storage → Delete all
2. Visit `http://localhost:8000/character/baker.html`
3. Click "Begin Investigation"
4. Open `http://localhost:8000/vision/alice.html` multiple times
5. **Expected**: You should see fragmented visions (different text), incrementing 1-11

### Test Path 3: Doctor Character (Blocked Vision)
1. Clear browser storage
2. Visit `http://localhost:8000/character/doctor.html`
3. Click "Begin Investigation"
4. Open `http://localhost:8000/vision/alice.html`
5. **Expected**: Generic message: "You sense a cold presence..."

### Test Path 4: Multiple Visions
1. Set character to Psychic
2. Visit each vision multiple times:
   - `http://localhost:8000/vision/alice.html` (increments 1-11)
   - `http://localhost:8000/vision/cordelia.html` (increments 1-11)
   - `http://localhost:8000/vision/sebastian.html` (increments 1-11)
3. **Expected**: Each vision has independent counters

---

## Browser Developer Tools

### Checking localStorage
```javascript
// In browser console (F12)
localStorage.getItem('characterName')  // Should show character
localStorage.getItem('vision_alice_number')  // Should show current vision
```

### Resetting Progress
```javascript
// Clear everything
localStorage.clear()

// Clear specific items
localStorage.removeItem('characterName')
localStorage.removeItem('vision_alice_number')
localStorage.removeItem('vision_cordelia_number')
localStorage.removeItem('vision_sebastian_number')
```

---

## QR Code Setup

### Generating QR Codes

You can use any QR code generator. Create codes pointing to:

**Character Selection QR Codes:**
- Psychic: `https://your-domain.com/character/psychic.html`
- Baker: `https://your-domain.com/character/baker.html`
- (etc. for each character)

**Vision QR Codes (place around venue):**
- Alice: `https://your-domain.com/vision/alice.html`
- Cordelia: `https://your-domain.com/vision/cordelia.html`
- Sebastian: `https://your-domain.com/vision/sebastian.html`

### Recommended QR Generators
- https://qr-code-generator.com/
- https://www.qr-code-generator.de/ (German site but intuitive)
- https://www.the-qrcode-generator.com/

### Physical Setup Tips
- Print QR codes on cardstock
- Laminate for durability
- Make them large enough to scan easily
- Test scanning with multiple phones/cameras

---

## Mobile Testing

### iPhone Safari
- QR Scanner built-in (Camera app)
- Tests from Notes app or Messages (tap link)
- Works great for this use case

### Android Chrome
- Built-in QR scanner in Google Lens
- Point camera at QR code
- Tap lens icon and scan

### Test Devices
Test on at least one mobile device to ensure:
- Font sizes are readable
- Buttons are easily tapable (min 44x44px - already satisfied)
- Colors display correctly
- Layout is responsive

---

## Customization Tips

### Change the Mystery Title
Edit in `index.html`:
```html
<h1>The Crimson Murder</h1>
```

### Modify Color Scheme
Edit in `assets/style.css`:
```css
:root {
  --accent-gold: #d4a574;  /* Change this */
  --accent-purple: #4a148c;  /* Or this */
  /* etc. */
}
```

### Add New Characters
1. Create `character/newcharacter.html`
2. Copy from `character/baker.html`
3. Change title, description, and `setCharacter('newcharacter')`
4. Add link in `index.html` character grid
5. Update `script.js` access levels if needed

### Add New Visions
1. Create `vision/newvision.html`
2. Copy from `vision/alice.html`
3. Update vision text arrays
4. Add to `script.js` access level definitions

---

## Troubleshooting

### Issue: Character not persisting after page reload
**Solution**: Check browser privacy settings. If in private/incognito mode, localStorage may be restricted.

### Issue: Vision counter not incrementing
**Solution**: Make sure you're using the same browser/device. Each device has separate localStorage.

### Issue: CSS styling not showing
**Solution**: Check file paths. Ensure you're running through a server (not `file://`).

### Issue: QR code links not working
**Solution**: Use full URLs with domain, not relative paths. Test links manually first.

### Issue: Mobile responsiveness issues
**Solution**: 
- Test in multiple browsers
- Check DevTools device emulation (F12 → Device Toolbar)
- Verify meta viewport tag is present

---

## Hosting & Deployment

### GitHub Pages (Free)
1. Create GitHub repository
2. Upload files
3. Enable Pages in Settings
4. Share QR codes pointing to your Pages URL

### Netlify (Free)
1. Drag & drop folder to Netlify
2. Get free domain
3. Configure custom domain if desired

### Traditional Hosting
- Any web host that serves static files works
- No database needed
- No backend processing needed

---

## Performance Notes

- Website loads instantly (no external dependencies)
- Works offline once cached
- Minimal data usage
- Optimized for phone cameras/screens

---

## Support & Debugging

### Enable Console Logging
Add this to any page to debug:
```javascript
console.log('Character:', getCharacter());
console.log('Access Level:', getVisionAccessLevel(getCharacter(), 'alice'));
console.log('Current Vision:', getCurrentVisionNumber('alice'));
```

### Common Issues Checklist
- [ ] Running through HTTP server (not file://)
- [ ] Browser allows localStorage
- [ ] JavaScript is enabled
- [ ] CSS file paths are correct
- [ ] All HTML files created
- [ ] No console errors (F12)

---

## Game Master Tips

### Before the Event
- Test all QR codes work
- Test on multiple devices
- Have backup phones ready
- Print physical QR codes with backup digital copies
- Organize character assignments

### During the Event
- Have the developer console open on a laptop to reset players if needed
- Keep printed copies of URLs for players having camera issues
- Have backup character sheets with direct links

### After the Event
- Collect feedback
- Note any bugs or improvements
- Consider expanding with more visions/clues

---

**Ready to host your murder mystery!** 🔍✨
