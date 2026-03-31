# Assignments

Assignments should be completed from top to bottom as they will raise in difficulty the lower in the stack.

## Part I

- **Children Story Generator**: Build a Django Server that will communicate with Google Gemini to accomplish the following:
    - A user will send in a 'lesson' through a request, for example: "Sharing", "Don't Lie", "Enjoying the little things", etc.
    - Gemini should generate a 500 word story, detailed for children, that a parent can comfortably read to their children at bedtime.

## Part II

- **Children Story Generator**: Build a Full-Stack app that will communicate with Google Gemini to accomplish the following:
    - A user will fill out a form with a 'lesson' through and submit it through a request, for example: "Sharing", "Don't Lie", "Enjoying the little things", etc.
    - The server will accept the request and forward it to Gemini
    - Gemini should generate:
        - 500 word story, detailed for children, that a parent can comfortably read to their children at bedtime.
        - An image for the story cover
    - Gemini's response should be in a JSON format that could be forwarded to the Front-End
    - Upon the server receiving a response from Gemini, said response should be forwarded to the Front-End
    - The Front-End should display the story to the user along with an image.