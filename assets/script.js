// The Lost Souls of Kennebec Avenue Investigation System
// Shared utility functions

/**
 * Get the current character from localStorage
 * @returns {string|null} The character name or null if not set
 */
function getCharacter() {
  return localStorage.getItem('characterName');
}

/**
 * Set the character in localStorage
 * @param {string} characterName - The name of the character
 */
function setCharacter(characterName) {
  localStorage.setItem('characterName', characterName);
}

/**
 * Clear the character from localStorage
 */
function clearCharacter() {
  localStorage.removeItem('characterName');
}

/**
 * Get the access level for a character viewing a vision
 * @param {string} characterName - The character name
 * @param {string} visionName - The vision name (e.g., 'alice', 'cordelia', 'sebastian')
 * @returns {string} 'FULL', 'PARTIAL', 'GOD_HELMET', or 'LIMITED'
 */
function getVisionAccessLevel(characterName, visionName) {
  // Define access levels for each vision
  const accessLevels = {
    alice: {
      FULL: ['psychic', 'explorer'],
      PARTIAL: ['baker'],
      GOD_HELMET: ['clockmaker']
    },
    cordelia: {
      FULL: ['psychic', 'dressmaker'],
      PARTIAL: ['baker'],
      GOD_HELMET: ['clockmaker']
    },
    sebastian: {
      FULL: ['psychic', 'doctor'],
      PARTIAL: ['baker'],
      GOD_HELMET: ['clockmaker']
    }
  };

  const visionAccess = accessLevels[visionName] || {};
  
  if (visionAccess.FULL && visionAccess.FULL.includes(characterName)) {
    return 'FULL';
  }
  if (visionAccess.PARTIAL && visionAccess.PARTIAL.includes(characterName)) {
    return 'PARTIAL';
  }
  if (visionAccess.GOD_HELMET && visionAccess.GOD_HELMET.includes(characterName)) {
    return 'GOD_HELMET';
  }
  return 'LIMITED';
}

/**
 * Get the access level for a character viewing a clue type
 * @param {string} characterName - The character name
 * @param {string} clueType - The clue type (e.g., 'rumors', 'botanical', 'medical', 'documents', 'artifacts')
 * @returns {string} 'FULL', 'PARTIAL', or 'LIMITED'
 */
function getClueAccessLevel(characterName, clueType) {
  // Define access levels for each clue type
  const accessLevels = {
    rumors: {
      FULL: ['heiress', 'influencer'],
      PARTIAL: ['psychic', 'baker', 'clockmaker', 'dressmaker', 'explorer', 'fiduciary', 'mortician', 'professor', 'doctor', 'artcollector']
    },
    botanical: {
      FULL: ['professor'],
      PARTIAL: ['fiduciary', 'explorer', 'baker']
    },
    medical: {
      FULL: ['doctor'],
      PARTIAL: ['mortician', 'professor']
    },
    documents: {
      FULL: ['fiduciary'],
      PARTIAL: ['mortician']
    },
    artifacts: {
      FULL: ['artcollector'],
      PARTIAL: ['explorer', 'heiress']
    }
  };

  const clueAccess = accessLevels[clueType] || {};
  
  if (clueAccess.FULL && clueAccess.FULL.includes(characterName)) {
    return 'FULL';
  }
  if (clueAccess.PARTIAL && clueAccess.PARTIAL.includes(characterName)) {
    return 'PARTIAL';
  }
  return 'LIMITED';
}

/**
 * Get current vision number for a specific vision, incrementing it
 * @param {string} visionName - The vision name (e.g., 'alice')
 * @param {number} maxVisions - Maximum number of visions to cycle through
 * @returns {number} The current vision number (1-indexed)
 */
function getNextVisionNumber(visionName, maxVisions = 11) {
  const key = `vision_${visionName}_number`;
  let current = parseInt(localStorage.getItem(key)) || 0;
  
  // Increment and loop back if necessary
  current = (current % maxVisions) + 1;
  
  localStorage.setItem(key, current);
  return current;
}

/**
 * Get current vision number without incrementing
 * @param {string} visionName - The vision name
 * @returns {number} The current vision number (1-indexed)
 */
function getCurrentVisionNumber(visionName) {
  const key = `vision_${visionName}_number`;
  const current = parseInt(localStorage.getItem(key)) || 1;
  return current;
}

/**
 * Reset vision counter for a specific vision
 * @param {string} visionName - The vision name
 */
function resetVisionCounter(visionName) {
  const key = `vision_${visionName}_number`;
  localStorage.removeItem(key);
}

/**
 * Check if character is selected, redirect if not
 * @param {string} redirectUrl - URL to redirect to if no character is selected
 * @returns {boolean} True if character is selected, false if redirected
 */
function checkCharacterSelected(redirectUrl = '/index.html') {
  const character = getCharacter();
  if (!character) {
    window.location.href = redirectUrl;
    return false;
  }
  return true;
}

/**
 * Format a character name for display (capitalize)
 * @param {string} name - The character name
 * @returns {string} Formatted name
 */
function formatCharacterName(name) {
  return name.charAt(0).toUpperCase() + name.slice(1);
}

/**
 * Format an entry date from ISO format (YYYY-MM-DD) to readable format
 * @param {string} dateString - The date in ISO format (YYYY-MM-DD or YYYY-MM)
 * @returns {string} Formatted date (e.g., "March 15, 1920" or "May 1925")
 */
function formatEntryDate(dateString) {
  if (!dateString) return '';
  
  const dateParts = dateString.split('-');
  
  // Handle YYYY-MM format (just month and year)
  if (dateParts.length === 2) {
    const year = parseInt(dateParts[0]);
    const month = parseInt(dateParts[1]);
    const date = new Date(year, month - 1);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
  }
  
  // Handle YYYY-MM-DD format (full date)
  if (dateParts.length === 3) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  }
  
  return dateString;
}
