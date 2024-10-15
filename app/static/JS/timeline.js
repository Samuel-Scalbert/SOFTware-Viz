document.addEventListener('DOMContentLoaded', (event) => {
    let currentBlockIndex = 0; // Track the currently visible block
    const blocks = document.querySelectorAll('.time_block'); // Select all time blocks

    // Function to update block visibility, blur, and position effects
    function updateBlockVisibility() {
        blocks.forEach((block, index) => {
            if (index === currentBlockIndex) {
                // Current block - fully visible and centered
                block.style.opacity = '1';
                block.style.filter = 'none';
                block.style.zIndex = '2'; // Ensure this block is on top
                block.style.transform = 'translate(-50%, -100%)'; // Center it properly in the middle
            } else if (index === currentBlockIndex - 1) {
                // Block just before (above) the current block - blurred and slightly above
                block.style.opacity = '0.5'; // Slightly visible
                block.style.filter = 'blur(5px)'; // Apply blur
                block.style.zIndex = '1'; // Send it behind the current block
                block.style.transform = 'translate(-50%, calc(-150%))'; // Adjusted positioning above the current block
            } else if (index === currentBlockIndex + 1) {
                // Block just after (below) the current block - blurred and slightly below
                block.style.opacity = '0.5'; // Slightly visible
                block.style.filter = 'blur(5px)'; // Apply blur
                block.style.zIndex = '1'; // Send it behind the current block
                block.style.transform = 'translate(-50%, calc(-40%))'; // Adjusted positioning below the current block
            } else {
                // All other blocks - hidden
                block.style.opacity = '0';
                block.style.filter = 'none'; // No blur on hidden blocks
                block.style.zIndex = '0'; // Hide these blocks behind others
                block.style.transform = 'translate(-50%, -50%)'; // Keep them centered off-screen
            }
        });
    }

    // Initial setup
    updateBlockVisibility();

    // Scroll event listener
    window.addEventListener('wheel', (event) => {
        // Determine scroll direction
        if (event.deltaY > 0) {
            // Scrolling down
            if (currentBlockIndex < blocks.length - 1) {
                currentBlockIndex++;
            }
        } else {
            // Scrolling up
            if (currentBlockIndex > 0) {
                currentBlockIndex--;
            }
        }
        updateBlockVisibility(); // Update visibility of blocks
    });
});
