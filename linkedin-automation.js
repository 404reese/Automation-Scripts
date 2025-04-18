async function sendLinkedInConnections() {
    // Configuration
    const MAX_CONNECTIONS = 2;
    const SCROLL_TIMEOUT = 1000;
    const CLICK_TIMEOUT = 300;
    
    // Counters
    let connects = 0;
    let fails = 0;
    
    // Function to scroll down the page
    function scroll() {
        window.scrollTo(0, document.body.scrollHeight);
        console.log("Scrolling down...");
    }
    
    // Function to find Connect buttons
    function selectConnectButtons() {
        return [...document.querySelectorAll("button span")]
            .filter(span => span.textContent.trim() === "Connect")
            .map(span => span.closest("button"));
    }
    
    // Function to click a single button with delay
    async function singleClick(element) {
        return new Promise(resolve => {
            setTimeout(() => {
                try {
                    element.click();
                    resolve(true);
                } catch (error) {
                    console.error("Failed to click:", error);
                    resolve(false);
                }
            }, CLICK_TIMEOUT);
        });
    }
    
    // Function to handle the send invitation modal
    async function handleSendInvitationModal() {
        return new Promise(resolve => {
            setTimeout(() => {
                try {
                    // Look for the "Send" button in the modal
                    const sendButtons = [...document.querySelectorAll("button span")]
                        .filter(span => span.textContent.trim() === "Send")
                        .map(span => span.closest("button"));
                    
                    if (sendButtons.length > 0) {
                        sendButtons[0].click();
                        resolve(true);
                    } else {
                        // If no Send button, look for "Connect" button in the modal
                        const connectButtons = [...document.querySelectorAll("button span")]
                            .filter(span => span.textContent.trim() === "Connect")
                            .map(span => span.closest("button"));
                        
                        if (connectButtons.length > 0) {
                            connectButtons[0].click();
                            resolve(true);
                        } else {
                            resolve(false);
                        }
                    }
                } catch (error) {
                    console.error("Failed to handle invitation modal:", error);
                    resolve(false);
                }
            }, CLICK_TIMEOUT);
        });
    }
    
    // Main loop
    while (connects < MAX_CONNECTIONS) {
        // Scroll to load more profiles
        scroll();
        
        // Wait for content to load after scrolling
        await new Promise(resolve => setTimeout(resolve, SCROLL_TIMEOUT));
        
        // Find connect buttons
        const buttons = selectConnectButtons();
        console.log(`Found ${buttons.length} connect buttons`);
        
        if (buttons.length === 0) {
            console.log("No more connect buttons found. Scrolling to find more...");
            // Scroll a few more times before giving up
            for (let i = 0; i < 3; i++) {
                scroll();
                await new Promise(resolve => setTimeout(resolve, SCROLL_TIMEOUT));
                const newButtons = selectConnectButtons();
                if (newButtons.length > 0) {
                    buttons.push(...newButtons);
                    break;
                }
            }
            
            if (buttons.length === 0) {
                console.log("Still no connect buttons found. Exiting.");
                break;
            }
        }
        
        // Process buttons
        for (const button of buttons) {
            // Stop if we've reached the maximum
            if (connects >= MAX_CONNECTIONS) {
                console.log(`Reached maximum connection limit (${MAX_CONNECTIONS}). Stopping.`);
                break;
            }
            
            // Click the connect button
            const clickSuccess = await singleClick(button);
            
            if (clickSuccess) {
                // Handle any modal that appears for sending the invitation
                const modalHandled = await handleSendInvitationModal();
                
                if (modalHandled) {
                    connects++;
                    console.log(`Connection request sent: ${connects}/${MAX_CONNECTIONS}`);
                } else {
                    fails++;
                    console.log(`Failed to complete connection: ${fails}`);
                }
            } else {
                fails++;
                console.log(`Failed to click connect button: ${fails}`);
            }
            
            // Small delay between requests to avoid detection
            await new Promise(resolve => setTimeout(resolve, CLICK_TIMEOUT * 2));
        }
    }
    
    console.log(`Finished sending connection requests!`);
    console.log(`Successful connections sent: ${connects}`);
    console.log(`Failed attempts: ${fails}`);
}

// Execute the function
sendLinkedInConnections();