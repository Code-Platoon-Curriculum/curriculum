# How to Succeed at Whiteboarding Problems

## Introduction

Technical Interviews and the 'Interview Process' are unavoidable facts of life for software engineers. It is important to understand the interview process as a whole and approach it proactively in order to succeed.

You will learn about the interview process as a whole, the different kinds of technical interviews and when they happen, and, the specific strategy to practice and utilize to succeed in technical interviews, aka 'whiteboarding problems'.

## Lecture

### Background - The Interview Process

The interview process - approx. 3-5 interviews, approx. 1hr each.  Here is a rough outline of the process. It doesn't always occur in this order and sometimes there are multiple behavioral/technical rounds.

1. Resume screen (i.e. submitting the job application and getting past HR)
2. Coding Challenge on leetcode or something similar
3. Technical Interview One. It could be ...
    a. A technical conversation (talk about a project you've done, a technology you like, etc)
    b. A whiteboarding problem

4. Technical interview Two. It could be ...
    a. A technical conversation (talk about a project you've done, a technology you like, etc)
    b. A whiteboarding problem
    c. A take-home coding assignment (a weekend project)
        i. They say "it should take 4hrs". It always takes twice as long. Aim to write production-quality code w/best practices, and treat it like a professional task - deliver on time, communicate delays, etc.
5. Behavioral Interview
6. Final, final interview (if you're here you're in the running). Sometimes just a nontechnical conversation
    - Have good questions to ask about the company and career growth.

### The Whiteboarding Problem / Technical Interview

#### History

Historically, a whiteboarding problem was in-person. It meant writing code on a whiteboard to solve a technical challenge / or task, and, maybe doing some design (drawing database tables/schema, etc).

It comes from Computer Science courses. Traditionally the problems have been algorithm/data-structures focused.

#### Today

It has evolved over time ...

- Usually over zoom
- Usually writing code (but maybe not running it)
- Not always algorithm/data science problems, BUT, focused on thought process.

#### Purpose / function

**The interviewer wants to see how you think.** The interview is:

- 60% process, 40% solving the problem.
- A huge part of this is the **process**.


IF YOU DO WELL ... they will push you more in the interview.
**You can still get hired if you don't finish the whiteboarding problem.**

## Succeeding At Whiteboarding Problems

"The interviewer is not your enemy -- they are your ally"
-- *A Sierra Platoon student.*

Treat the interview like an audition. Preparation and practice are essential.

ALWAYS 1-3 DAYS BEFORE THE INTERVIEW, CONFIRM:

- Language / task
  - Usually you can pick the language.
- Ask for name/role of who is interviewing me

### Tackling the Problem

Here is the strategy to follow:

1. Process the Problem
2. Prototype your solution
3. Implement your solution  
4. Adjust and Communicate as you go
5. Double-check before telling the interviewer you've solved it.

#### Time Management

Time management is important - you want to be writing code about 20min in,
aim to have a solution working 10min before interview is over.

- Checking in / asking the interviewer about time is never a bad idea.
- Saying out loud if you are stuck is never a bad idea.
  - This demonstrates awareness of the importance of time/project management in software. 

#### Process the Problem

Analyze the problem, discuss it with the interviewer, look for edge cases, and get yourself warmed up.

**WRITE ALL THIS DOWN ON THE SCREEN AS YOU TALK THROUGH IT.**

1. Repeat the question

- Shows we are listening
- Buys us time
- MAKING SURE WE UNDERSTAND THE QUESTION
  - That the interviewer KNOWS we understand the question
  - Clarify if there is a misunderstanding
  - Sometimes the interviewer made a mistake / the question has a problem

2. Understand inputs and outputs

**What are the inputs?**

- Type and shape (int/string/dict etc)
- Think out loud about EDGE CASES - zero, special characters, etc.
- Input size - upper and lower bounds?
  - Asking this shows that you understand that input size affects performance

A good approach is always to prototype for a small input size, and worry about a big input size later.

- EDGE CASES - what are input edge cases?

**What is the output?**

- What kind of output / what format?
  - Missing a detail in the output specification is a common gotcha.

#### Prototype your solution

Talk through the simplest possible version of the problem. Explain your approach.

- Pseudocode with a tiny input size like for example a list of four `['4', '3', '2',  '1']
- Extremely small / simple data, no edge cases yet.

Your goal here is to 'fail fast' - with pseudocode "think through" the solution you want to use with a *tiny* amount of real world input. *Maybe* you write a little bit of actual code.

- Explain your plan before you start coding.
- Ask the interviewer, "what do you think? does that make sense?"
- Approach the process collaboratively.

#### Implement your solution

Now we write code!

1. Get your solution working for the simplest cases.
2. Run your code as you go.
3. Handle edge cases.

- Work in small (tiny, tiny) chunks.
  - Get each chunk working before you move on.
- Don't be afraid to ask questions / ask for help / check in.
- KEEP TALKING.

#### Adjust and communicate as you go

Check in regularly with your interviewer to ask if they have any feedback. Explain out loud your thought process while coding. **Never go silent**.

You may run into problems - that's OK! Ideally you want to 'fail fast'. It's OK if during implementation you realize your solution is not the right apprach.

Remember:

- First make it work
- Then make it right
- Then make it fast (efficient)

Be prepared for the interviewer to "add on " tasks / make the problem harder as you go.This means you are doing well!

#### Double-check your solution

Make a checklist of edge cases, and what the solution has to output. Run down your checklist before saying you're "done". It is easy to get lost in the weeds in details and lose sight that, say, your code must return the *size* of the list you sorted, not the sorted list itself!

Do this out loud and give your interviewer opportunity to give you feedback.

## Conclusion

Technical Interviews / Whiteboarding Problems are about showing how you think as much as they are about demonstrating your technical skills and knowledge. Like an NBA player practicing their free-throws, focus your practice on the fundamentals so you still sink that easy shot on Game Day. With preparation and practice, technical interviews can be an opportunity to show your skills and shine!

## Resources

- [Launch School's 'PEDAC' process for Technical Interviews](https://medium.com/launch-school/solving-coding-problems-with-pedac-29141331f93f)
