# Intermediate JS and Jest

## Intro

We will learn about more modern JS language features to help us write our code more expressively, and also introduce how to write and run *tests*. The more complex our programs become the more value tests can offer. Ideally, tests make our lives easier as developers. Different languages have different tools for writing tests but in general the approach is similar across languages. We'll learn about *Jest*, a popular library for writing tests in JS.

Specifically we will write some **unit tests**, tests that test a specific *unit* of our code, such as a specific function. Unit tests are often the foundation of a testing strategy.

## Intermediate JavaScript

Many of the JS features we will explore today are what is referred to as 'syntactic sugar'. The ideas presented in part 1 are the core of the language. Syntactic sugar on the other hand just provides a way for a programmer to more neatly and concisely express an idea that was already possible without it, but was perhaps unnecessarily verbose or otherwise inconvenient.

### 'Arrow' functions

Functions are not only syntactic structures in JS but also 'first class' values, meaning they can be assigned to a variable and passed around. This is very useful and modern JS makes this simple to do with what are called 'arrow functions'.

```js
const makeFullName = (firstName, lastName) => `${firstName} ${lastName}`;

makeFullName("Benjamin", "Cohen"); // "Benjamin Cohen"
```

This seems about identical but note that:

1. it is a normal variable, so had to be defined before referencing/calling it (no hoisting on arrow functions).
2. The function itself is anonymous - it has no name. To name it, you need to store it in a variable.
3. the return statement was implicit, perfect for one-liners. (arrow functions can also have full bodies but this is the default behavior)

This is incredibly useful when using a 'higher order function', ie a function that takes another function as a parameter. The classic example is `map`, an Array method that allows you to create a new array based on the original with the help of a 'mapper' function. Like so:

```js
const nums = [1, 2, 3];

const doubles = nums.map((x) => x * 2);

console.log(doubles); // [2, 4, 6]
```

Consider how much more convenient and concise that is than the below example:

```js
const nums = [1, 2, 3];

const doubles = nums.map(doubler);

console.log(doubles); // [2, 4, 6]

function doubler(x) {
  return x * 2;
}
```

It's not night and day but it's a useful feature for writing short functions that doesn't litter your codebase with one off named functions.

### Destructuring

Destructuring is a modern syntax tool that allows the programmer to 'pick off' useful values from an array or object. Consider these two approaches to creating variables from a complex data type:

```js
const myArray = ["x", "y", "z"];
const x = myArray[0];
const y = myArray[1];
const z = myArray[2];

const myObject = { a: 45, b: "hello", c: true };
const a = myObject.a;
const b = myObject.b;
const c = myObject.c;
```

As compared to:

```js
const [x, y, z] = ["x", "y", "z"];

const { a, b, c } = { a: 45, b: "hello", c: true };
```

Anywhere you would normally use a single variable to capture some value (a variable declaration, a function parameter, etc) you can use destructuring. Let's reconsider the `Object.entries` example from part 1:

```js
const database = {
  457: {
    name: "Tom",
    age: 34,
  },
  57782: {
    name: "Sally",
    age: 42,
  },
};

for (let [key, value] of Object.entries(database)) {
  console.log(key); // '457'
  console.log(value); // { name: 'Tom', age: 34 }
}
```

### The 'spread' operator (`...`)

The JavaScript spread operator (...) allows us to quickly copy all or part of an existing array or object into another array or object.

```js
const arrOne = [1, 2, 3];
const arrTwo = [4, 5, 6];
const arrCombined = [...arrOne, ...arrTwo];

const objOne = { x: 1, y: 2, z: 3 }
const objTwo = { a: 4, b: 5,c: 6 }
const objCombined = {...objOne, ...objTwo};

console.log(arrCombined)
console.log(objCombined)
```

You can also use the spread operator to expand an array into individual arguments for a function.

```js
const numbers = [10, 20, 5];
const maxNumber1 = Math.max(numbers);
const maxNumber2 = Math.max(...numbers);
console.log(maxNumber1, maxNumber2); // NAAN, 20
```



## Conclusion

We've reviewed important modern JS language features - arrow functions, destructuring, and imports/exports in particular. And we've learned how to write unit tests in Jest to test the functions we write and get good *test coverage*, and organize and run our tests. Writing tests takes more work - at first. But as your programs grow complex, writing unit tests and practicing *Test-Driven Development* will help you design your programs, organize your workflow, and make it *easier* to change your code - because you can trust your tests to be a "harness" to catch you if you make a mistake! 🚀
Jest is a third party JavaScript library, meaning it's not baked into the language by default. This means we will need to use `npm` to download it.

In order to do this, let's first create a folder we want to work with, and then set it up to be an `npm` project.

```sh
npm init
```

The above command will initiate a list of questions, and when done will add a file to your project's folder - `package.json`. This file is a config file, it defines things that your JS project might care about, and is necessary to start downloading packages.

> `npm init -y` will answer all questions by default and just make the `package.json` for you which you can then edit manually

Now we want to download Jest. We do this with:

```js
npm install --save jest
```

> The `--save` will update `package.json` with a new field called `dependencies`. This keeps track of what dependencies your project requires, which is useful for other people who share your code who can then just type `npm install` to download all the necessary dependencies. If running into issues in the WSL environment, you might need to edit this `--save` flag to become `--save-dev`.

Now try typing `jest` into your command line to see `jest` run (even though we don't have any tests yet). Not recognized, right?! That's because `jest` only exists for our project, not for the entire computer. To get around this, we can run it by modifying part of the `package.json`. `package.json` has a field called `scripts`, replace it with:

```js
...
  "scripts": {
    "test": "jest"
  },
...
```

Your entire `package.json` should look similar to the below to follow along:

```js
{
  "name": "jest-intro",
  "version": "1.0.0",
  "scripts": {
    "test": "jest"
  },
  "dependencies": {
    "jest": "^29.6.4"
  },
}
```

Now we can run `npm test` and it will run `jest`. If you see some output saying you have no tests, we are ready to move on!
