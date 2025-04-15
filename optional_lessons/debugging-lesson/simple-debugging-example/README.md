# Simple Debugging Example

This is a simple debugging example in Python. It uses the CSV Reader programming assignment. All code & content necessary is here. See the [problem readme](problem-readme.md) for context on the assignment.

## Diagnosis & Fixing the bug

We will use the scientific approach - observe, research & make a hypothesis, make a single change, and observe the results. Then rinse and repeat. We will also use several of the ten debugging tips previously mentioned.

You can also think of this debugging workflow as [Observe, Orient, Decide, Act](https://fs.blog/ooda-loop/).

Here is a modification of one correct solution, except it has some errors. This is based on multiple real-world errors seen in working with students:

```python
import csv
animal_type = input("cats or dogs?\n")

try:
    data = open(f'./datas/{animal_type}.csv')
    reader = csv.DictReader(data)

    for row in reader:
        print(f"{row['name']} is a {row['age']} year old {row['breed']}.")
        
        data.close()

except:
    print(f"Sorry, we don't have any {animal_type} here.")
```

The biggest problem with this code is, if we run it, we get a **silent failure**. We see our exception print statement, "Sorry, we don't have any dogs here.", **but**, this gives us **almost no useful information** we can use to debug our error.

The exception is actually swallowing the error info we need. Our first step to fix this is to get useful data from the exception:


```python
import csv, traceback
animal_type = input("cats or dogs?\n")

try:
    data = open(f'./datas/{animal_type}.csv')
    reader = csv.DictReader(data)

    for row in reader:
        print(f"{row['name']} is a {row['age']} year old {row['breed']}.")
        
    data.close()

except Exception:
    traceback.print_exc()
```

When we run this code, we should now get a more useful error message. With some work we can determine that our path to read the csv file from - in this line of code:

```python
    data = open(f'./datas/{animal_type}.csv')
```

... that the path here is wrong. It should be `/data` instead of `/datas`. The correct line of code is this:

```python
    data = open(f'./data/{animal_type}.csv')
```

We should now get a new error message. This last issue is trickier. With some investigation, we determine that this is the line of code causing the error:

```python
print(f"{row['name']} is a {row['age']} year old {row['breed']}.")
```

Let's simplify it:
```python
print(row)
```

Now our program works! Let's add in a bit more of the desired behavior to that line of code:

```python
print(f"{row['name']}") 
```

This also works. Using this process of **simplification**, we realize eventually that the issue is the **leading whitespace** in the our csv file headers -- `name, age, breed`. With some online research we can determine that we can use the `skipinitialspace` argument of Python's csv DictReader class to handle our dirty data.

We need to change this:
```python
    reader = csv.DictReader(data)
```

... to this:

```python
    reader = csv.DictReader(data, skipinitialspace=True)
```

Let's run that and make sure it works. Then, let's add in the full behavior we want for print statement we've been simplifying:

```python
print(f"{row['name']} is a {row['age']} year old {row['breed']}.")
```

Our entire program should now work. You can refer to [the complete correct solution here](solution.py)

## Postmortem

The big takeaway here is -- get good error messages! Exceptions, unless they are returning data which a user will see, should return meaningful error information. The actual error message itself is best.

What's also important is to recognize that **multiple issues** are common. It is normal to discover that there are several errors in your code, each hidden behind the last. One way to avoid this is to work in small chunks & always run your code after doing a bit of work to always keep your code in a "good state".

Another takeaway is -- hardcoded strings (our `data/` path) are easy to get wrong by making typos! Double-check and when possible use the DRY principle with hardcoded data like this. This particular error, for this specific problem, is a harder one to come up with a "process improvement" step for.

Finally -- read the docs. The `skipinitialspace` option of Python's csv `DictReader` is super useful. And, remember that with `.csv` files issues like this are common in the data and to anticipate these sorts of problems & always examine data files when we can, before writing code.

Hopefully this was helpful! Happy coding.
