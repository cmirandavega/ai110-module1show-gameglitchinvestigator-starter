# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  1. The hints are backwards, its saying to guess higher when you should be guessing lower and lower when you should be guessing higher
  2. The difficulty should be changing the range and its not showing in the app. When I select the Easy difficulty it should be numbers up to 20, but it will still allow me to guess above that, as I am testing currently on easy difficulty it shows secret is 50 which is above the limit
  3. the attempt limits seem to be off by 1, the code said Easy has a attempt limit of 6 but shows 5 in the browser
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). For example when I was manually finding some bugs I found the higher and lower being off, then I asked claude to find bugs without giving it to much specificity to see if it would catch it and it did.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result). AI just deleted the entire app.py code LOL, I asked Claude when creating the test cases, it tried to mask a failed test output and I said no no no, went back to the logic, found what was wrong and retested using the same assert and expected values from before and it passed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I ran the code logic through the pytest, however I also replayed the game myself. I tried to see if the UI fixed itself and also if I could catch the same things as before when I played it the first time. 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code. I came up with the winning verification, so guessing the correct answer and getting the correct output message.
- Did AI help you design or understand any tests? How? I asked Claude to take me through step by step in the thought process of it all, from coming up with the test, what are we validating, and is this test really a test (Not no 1 = 1 test).

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  One reason was that streamlit tends lit would rerun the app after every action was made, essentially it would keep rerunning changing its parameters.
  Another reason was the hardcoded random secret number, if you were to run an easy mode for example, the secret number would still be above what the secret number should be.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Imagine Streamlit like a whiteboard that gets erased and redrawn every time someone touches it
- What change did you make that finally gave the game a stable secret number?
  The key fix was adding this block before the existing if "secret" not in st.session_state. It tracks the current difficulty in session state and compares it on every rerun.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or        projects? 
- This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I found that telling Claude to go through step by step into its thought process. Not only does it make it easier to understand what is happening, but it makes validation of code easier. One thing I would do differently is use the planning mode more often, making it also easier to verify the plan of implimentation, for example in my personal classes I have claude build out step by step documentation of each programming task. This project really influences me to not be scared of using AI generated code, because if I didnt know what I was doing this code wouldnt have worked. It kind of reliefs me of imposter syndrome almost? In a way like anyone can just ask claude to code them something and itll work flawlessly. No that not the case. This was a great experience.
