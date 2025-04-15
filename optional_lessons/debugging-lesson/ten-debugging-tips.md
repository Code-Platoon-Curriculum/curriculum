# Debugging Advice

1. Embrace the scientific process: observe without touching, hypthesize, make a single modification, observe the results, repeat.

   - Don’t touch anything!!! Examine the data you have before making changes, otherwise you'll lose your data & it'll be harder to reproduce the bug. And only change one thing at a time so you can accurately observe the effects of your change. 

2. Get data. If you dont have data (error messages, print statements, program behavior) – its impossible to analyze and identify the issue. Get data!!

3. Use your brain - don’t throw code against the wall like spaghetti to see what sticks.

   - If you’re getting frustrated take a break. Often just letting your eyes rest on something else for a while will reveal your solution when you return.

   - Sometimes its hard to use your brain staring at a screen. Write, draw, talk out the problem. Get up and walk.

4. Read the error messages. Google the error message.

5. Walk through your assumptions and check them. Get data - don’t assume. 

6. Reduce the problem space - use print statements, the debugger, whatever, to get insight into the flow of data through your program. Know which sections of your code are “good” – you can prove it is behaving as expected. Work to, line by line, to eliminate potential “bad” code – lines of code where the bug could be hiding. Reduce the problem space.

   - Sometimes simply commenting stuff out until your program runs as expected, then un-commenting line by line, is a great approach. Be sure to commit before you do this. 

   - If you know the problem is on one line code – can you turn that one line of code into two lines of even simpler code? Simplify until you find your bug. 

7. Be pragmatic - can I simplify things? Do I need this bit of code at all? If I am stuck, can I work on something else?

8. Ask for a second set of eyes on your code, or practice some [rubber-duck debugging](https://rubberduckdebugging.com/).

9. Start to classify your errors:
    - Silent failures (no error messages)

    - Unintended behavior or misunderstood (the program runs, just not the way I expected). 
        - The program behaves differently
        - I misunderstood what I was doing (i.e., I thought `reduce()` in JS works one way but it actually works another way).

    - Simple bugs caused by programmer error (aka “I should set up that linting plugin”)



   - Learn to anticipate that sometimes it’s more than one bug at the same time. 

10. Once you fix the bug, do a postmortem – what can I do in the future to avoid reproducing that bug? What parts of my debugging process were successful, and what could I have done differently to better identify & fix the bug?
