document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const audioPlayer = document.getElementById('audioPlayer');
    const playButton = document.getElementById('playBtn');
    const pauseButton = document.getElementById('pauseBtn');
    const repeatButton = document.getElementById('repeatBtn');
    const startVerseSelect = document.getElementById('startVerse');
    const endVerseSelect = document.getElementById('endVerse');
    const repeatCountInput = document.getElementById('repeatCount');
    const progressBar = document.getElementById('progressBar');
    const verseElements = document.querySelectorAll('.verse-item');
    
    // State variables
    let currentVerse = 1;
    let isPlaying = false;
    let isRepeating = false;
    let repeatCount = 1;
    let currentRepeatCounter = 0;
    
    // Handle errors
    function handleAudioError(error) {
        console.error('Audio error:', error);
        alert('عذرا، حدث خطأ أثناء تشغيل الملف الصوتي. يرجى المحاولة مرة أخرى.');
    }
    
    // Get audio URL for a verse
    function getAudioUrl(verseNumber) {
        return `/api/audio/${verseNumber}`;
    }
    
    // Load and play verse audio
    function loadAndPlayVerse(verseNumber) {
        // Remove active class from all verses
        verseElements.forEach(verse => verse.classList.remove('active'));
        
        // Add active class to current verse
        const currentVerseElement = document.getElementById(`verse-${verseNumber}`);
        if (currentVerseElement) {
            currentVerseElement.classList.add('active');
            
            // Scroll to verse if needed
            currentVerseElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        // Update current verse
        currentVerse = verseNumber;
        
        try {
            // Set audio source using direct URL approach for better mobile compatibility
            audioPlayer.src = getAudioUrl(verseNumber);
            
            // Set event listeners for this specific playback
            audioPlayer.oncanplay = function() {
                // Play the audio when it's ready
                const playPromise = audioPlayer.play();
                if (playPromise !== undefined) {
                    playPromise.catch(error => {
                        // Auto-play was prevented
                        console.error('Autoplay prevented:', error);
                        // Don't show error on auto-play prevention
                        if (error.name !== 'NotAllowedError') {
                            handleAudioError(error);
                        }
                        isPlaying = false;
                        updateUIState();
                    }).then(() => {
                        isPlaying = true;
                        updateUIState();
                    });
                }
            };
            
            // Error handling
            audioPlayer.onerror = function(e) {
                console.error('Audio error:', e);
                handleAudioError(e);
                isPlaying = false;
                updateUIState();
            };
            
            // Set ended event for next verse functionality
            audioPlayer.onended = function() {
                playNextVerse();
            };
            
            // Load the audio
            audioPlayer.load();
            isPlaying = true;
            updateUIState();
        } catch (error) {
            console.error('Error setting up audio:', error);
            handleAudioError(error);
        }
    }
    
    // Update UI based on current state
    function updateUIState() {
        if (isPlaying) {
            playButton.disabled = true;
            pauseButton.disabled = false;
        } else {
            playButton.disabled = false;
            pauseButton.disabled = true;
        }
        
        // Update repeat button
        repeatButton.classList.toggle('btn-info', !isRepeating);
        repeatButton.classList.toggle('btn-success', isRepeating);
        repeatButton.innerHTML = isRepeating ? 
            '<i class="fas fa-redo-alt me-2"></i> إيقاف التكرار' : 
            '<i class="fas fa-redo-alt me-2"></i> تكرار';
    }
    
    // Get start and end verse numbers
    function getStartVerse() {
        return parseInt(startVerseSelect.value);
    }
    
    function getEndVerse() {
        return parseInt(endVerseSelect.value);
    }
    
    // Play next verse
    function playNextVerse() {
        const startVerse = getStartVerse();
        const endVerse = getEndVerse();
        
        // Check if we need to repeat the current verse
        if (isRepeating && currentRepeatCounter < repeatCount - 1) {
            currentRepeatCounter++;
            loadAndPlayVerse(currentVerse);
            return;
        }
        
        // Reset repeat counter
        currentRepeatCounter = 0;
        
        // Move to next verse or wrap around
        if (currentVerse < endVerse) {
            loadAndPlayVerse(currentVerse + 1);
        } else {
            // Finished playing all verses in range
            // Go back to start verse
            loadAndPlayVerse(startVerse);
        }
    }
    
    // Update progress bar
    audioPlayer.addEventListener('timeupdate', function() {
        if (audioPlayer.duration) {
            const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
            progressBar.style.width = progress + '%';
        }
    });
    
    // Event Listeners
    
    // Play button
    playButton.addEventListener('click', function() {
        if (isPlaying) {
            audioPlayer.pause();
            isPlaying = false;
        } else if (audioPlayer.src) {
            audioPlayer.play().catch(e => {
                console.error('Play error:', e);
                if (e.name !== 'NotAllowedError') {
                    handleAudioError(e);
                }
            });
            isPlaying = true;
        } else {
            const startVerse = getStartVerse();
            loadAndPlayVerse(startVerse);
        }
        updateUIState();
    });
    
    // Pause button
    pauseButton.addEventListener('click', function() {
        audioPlayer.pause();
        isPlaying = false;
        updateUIState();
    });
    
    // Repeat button
    repeatButton.addEventListener('click', function() {
        isRepeating = !isRepeating;
        updateUIState();
    });
    
    // Verse click to play specific verse
    verseElements.forEach(verse => {
        verse.addEventListener('click', function() {
            const verseNumber = parseInt(this.dataset.verseNumber);
            startVerseSelect.value = verseNumber;
            loadAndPlayVerse(verseNumber);
        });
    });
    
    // Handle repeat count changes
    repeatCountInput.addEventListener('change', function() {
        repeatCount = Math.max(1, parseInt(this.value) || 1);
        this.value = repeatCount;
    });
    
    // Handle start verse changes
    startVerseSelect.addEventListener('change', function() {
        const startVerse = parseInt(this.value);
        if (startVerse > getEndVerse()) {
            endVerseSelect.value = startVerse;
        }
    });
    
    // Handle end verse changes
    endVerseSelect.addEventListener('change', function() {
        const endVerse = parseInt(this.value);
        if (endVerse < getStartVerse()) {
            startVerseSelect.value = endVerse;
        }
    });
    
    // Initialize UI state
    updateUIState();
    
    // Handle clicking download buttons without propagating to verse click
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
    
    // Handle visibility change (mobile tab switching)
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && isPlaying) {
            // Automatically pause when switching away on mobile
            audioPlayer.pause();
            isPlaying = false;
            updateUIState();
        }
    });
    
    // Special handler for mobile devices
    if ('ontouchstart' in window) {
        // Add click handler to body to enable audio on first interaction
        document.body.addEventListener('touchstart', function initAudio() {
            // Create and play a short silent audio to unlock audio playback
            const tempAudio = new Audio();
            tempAudio.play().then(() => {
                console.log('Audio unlocked on mobile');
            }).catch(e => {
                console.log('Could not unlock audio yet:', e);
            });
            
            // Remove this listener after first touch
            document.body.removeEventListener('touchstart', initAudio);
        }, { once: true });
    }
    
    // Preload audio files when app starts (for offline use)
    function preloadAudioFiles() {
        // Create a hidden preload container
        const preloadContainer = document.createElement('div');
        preloadContainer.style.display = 'none';
        document.body.appendChild(preloadContainer);
        
        // Try to preload first 5 verses for quick start
        for (let i = 1; i <= 5; i++) {
            fetch(getAudioUrl(i)).then(() => {
                console.log(`Preloaded audio for verse ${i}`);
            }).catch(e => {
                console.log(`Could not preload audio for verse ${i}:`, e);
            });
        }
    }
    
    // Start preloading after a short delay
    setTimeout(preloadAudioFiles, 2000);
});
