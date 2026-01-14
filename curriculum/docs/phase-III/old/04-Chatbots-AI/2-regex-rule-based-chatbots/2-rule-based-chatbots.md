# Rule Based Chatbots

## Concepts of a Rule-Based ChatBot

A **rule-based ChatBot** is a conversational agent that relies on predefined rules, conditions, or patterns to determine how to respond to user inputs. Unlike machine learning chatbots, it does not learn from data or adapt dynamically—instead, it uses *if-else logic*, *decision trees*, or *regular expressions (regex)* to match user input to specific responses. In this lecture we will utilize Python Classes to create a Rule Based Chatbot that helps agents `learn` how to pay their bill and `paying` their bills.

### What common methods belong to a ChatBot?

A typical rule-based chatbot contains:

- **Entering**  
  A method that greets the user and introduces the chatbot’s purpose. It can also be utilized to capture the users name in hopes of generating a more user friendly interaction with the ChatBot.

- **Exiting**  
  A method that allows users to leave the conversation gracefully (e.g., recognizing exit commands or negative sentiments).

- **Handling a Conversation**  
  A method that controls the conversation flow—parsing input, matching patterns, and delivering appropriate responses.

---

## Creating a Welcome Method

The welcome method introduces the bot to the user and sets expectations for what it can do.

```python
class BillPayChatBot:
    def __init__(self):
        self.conversation()

    def conversation(self):
        reply = input(f"""
Hello! I'm BillBot. I can help you pay your bills.
You can type things like 'I want to pay my bill' or 'How can I pay my bill'.
Type 'exit' at any time to leave the conversation.""")
        print(reply)
```

When you create an instance of `BillPayChatBot`, it will greet the user and provide instructions.

---

## Identifying Negative Responses

The bot should recognize when a user wants to leave the chat or refusing help from the bot itself. We can do this by adding a couple of instance variables detailing both predefined `Exit` and `Negative` responses.

```python
    def __init__(self):
        self.exit_commands = ['exit', 'quit', 'bye']
        self.negative_responses = ['no', 'not now', 'never']
```

We can determine if these `Negative` commands are present within our users initial response by creating a method `check_negative` that will take in the users input, iterate through the `negative_responses` and identify if any of them are present within the user input. We can call this method within our initial conversation method:

```python
    def conversation(self):
        reply = input(f"""
Hello! I'm BillBot. I can help you pay your bills.
You can type things like 'I want to pay my bill' or 'How can I pay my bill'.
Type 'exit' at any time to leave the conversation.""")
        if self.check_negative(reply):
          return

    def check_negative(self, user_input):
      if any(neg in user_input.lower() for neg in self.negative_responses):
            print("Alright, no problem! If you need help later, just let me know.")
            return True
      return False
```

## Creating a Handling Conversation Method

The core of the chatbot is the ability to process user inputs, identify intent, and respond accordingly allowing users to feel like they can effectively communicate and find their desired information. We can accomplish this by creating a method which will handle the conversation between our user and our ChatBot and call the method within the `conversation` method.

```python
    def conversation(self):
        reply = input(f"""
Hello! I'm BillBot. I can help you pay your bills.
You can type things like 'I want to pay my bill' or 'How can I pay my bill'.
Type 'exit' at any time to leave the conversation.""")
        if self.check_negative(reply):
          return
        self.conversation(reply)

    def handle_conversation(self, user_input):
        while True:
            print(user_input) 
            break
```

---

## Creating the Exit Command

Now that we are able to pass the user input into our `handle_conversation` method, we can ensure the users have a method for being capable to exit the interaction with the ChatBot. This method should iterate through the different `exit` commands and check if they are present within the user input.

```python
    def handle_conversation(self, user_input):
        while not self.check_exit(user_input):
            print(user_input) 
            break

    def check_exit(self, user_input):
        if any(cmd in user_input.lower() for cmd in self.exit_commands):
            print("Thank you for using BillBot. Goodbye!")
            return True
        return False
```

This method scans user input for exit commands. If found, it gracefully ends the interaction.

---

## Identifying Intent

Since this is a rule-based chatbot, we know exactly which intents we want to handle allowing us to utilize tools like regex to identify and designate intent to our users input. In this case:
✅ **Pay bill**
✅ **Ask about balance**
✅ **General help**

We can use regex or simple keyword matching:

```python
    def handle_conversation(self, user_input):
            while not self.check_exit(user_input):
                match = self.identify_intent(user_input)
                if not match:
                  user_input = input("I'm sorry, I couldn't understand you. Please rephrase your statement.\n")

    def identify_intent(self, user_input):
        intents = {
          "pay_bill":[r'\bpay\b.*\bbill\b',r'\bbill\b.*\bpay\b'],
          "check_balance":[r'\bbalance\b'],
          "help":[r'\bhelp\b']
        }
        user_input = user_input.lower()
        for intent, expression in intents.items():
            for expression in expressions:
                if re.search(expression, user_input)  and intent == "pay_bill":
                    return 'pay_bill'
                elif re.search(expression, user_input) and intent == "check_balance":
                    return 'check_balance'
                elif re.search(expression, user_input) and intent == "help":
                    return 'help'
        return "_"
```

This method scans for keywords using regex patterns and maps them to specific intents.

---

## Matching to a Response

Depending on the identified intent, the bot provides a predefined response.

```python
    def handle_conversation(self, user_input):
            while not self.check_exit(user_input):
                match = self.identify_intent(user_input)
                self.match_response(match)
                user_input = input("How else can I help you?")
                  

    def match_response(self, intent):
        if intent == 'pay_bill':
            print("Great! I can help you pay your bill. Please provide your account number.")
        elif intent == 'check_balance':
            print("Sure, I can help with that. Please provide your account number to check your balance.")
        elif intent == 'help':
            print("I'm here to assist you. You can say things like 'pay my bill' or 'check my balance'.")
        else:
            print("I'm sorry, I couldn't understand you. Please rephrase your statement.\n")
```

We can take this method and replace each one of these print statements with independent functions or utilities that will help the user achieve their intent.

---

## Conclusion

In this lesson, we designed a **rule-based chatbot** that assists customers in paying their bills. We explored how to:

✅ Greet and guide users at the start of a conversation.
✅ Recognize exit commands and negative responses to end conversations politely.
✅ Identify user intent using regex patterns.
✅ Return clear, predefined responses based on intent.

Rule-based bots like this are ideal for narrow, well-defined tasks (such as bill payment) because they provide **predictable**, **controlled**, and **reliable** interactions. While they may not handle unexpected queries as flexibly as AI-driven chatbots, they remain a valuable tool for customer service scenarios where accuracy and compliance are essential.
