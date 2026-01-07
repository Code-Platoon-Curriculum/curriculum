# useParams and useNavigate

## Introduction

Modern React applications often need to display **detail views** based on user interaction. Clicking on a list item, card, or row should navigate the user to a page that displays more information about that specific resource.

In this lesson, we will extend the PokemonCard application by adding a **Pokemon Details page**. This page will be driven by a dynamic URL parameter and reached through programmatic navigation.

By the end of this lecture, students will understand how:

- URLs can represent application state
- Dynamic route parameters work
- Components can navigate imperatively without links
- Routing, data fetching, and UI composition work together

---

## What is `useParams`?

`useParams` is a hook provided by `react-router-dom` that allows a component to **read dynamic values from the URL**.

When a route includes a dynamic segment, such as:

```bash
/pokemon/:id
```

`useParams` allows the component rendered at that route to access the `id` value directly.

> the `:` declares `id` as a parameter within this route

---

## What Problem Does `useParams` Solve?

Applications frequently need to render content based on **which resource the user is viewing**.

Examples include:

- Viewing a specific Pokémon
- Viewing a user profile
- Viewing a product detail page

Rather than storing this information in state, the **URL becomes the source of truth**. `useParams` provides a clean way to extract that information.

---

## Adding a Pokemon Details Route

### Creating the Details Page

Inside `src/pages`, create a new file called `PokemonDetailsPage.jsx`.

This page will:

- Read the Pokémon ID from the URL
- Fetch data from the PokeAPI
- Display a clean, focused Pokémon view

#### Capturing the Parameter

Lets first work through the process of grabbing the parameter straight from the url pattern and displaying it on the screen:

```jsx
//router.jsx within `children
{
  path: "pokemon/:id",
  element: <PokemonDetailsPage />,
}

// PokemonDetailsPage.jsx
import { useParams } from "react-router-dom";
import axios from "axios";

const PokemonDetailsPage = () => {
  const { id } = useParams();

  return (
    <div>
      <h2>{id}</h2>
    </div>
  );
};

export default PokemonDetailsPage;

// within the PokemonCard.jsx add
<Link to={`/pokemon/${data.id}`}>Details</Link>
```

Now when you click on a cards *Details link you should see the Pokemons Id being displayed on the screen.

---

#### Fetching Pokemon Data

We will utilize

```jsx
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const PokemonDetailsPage = () => {
  const { id } = useParams();
  const [pokemon, setPokemon] = useState(null);

  const fetchPokemon = async () => {
    try {
      const response = await axios.get(
        `https://pokeapi.co/api/v2/pokemon/${id}`
      );
      setPokemon(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(()=>{
    fetchPokemon()
  }, [id])

  return (
    <>
      {
        pokemon ?
        <div>
          <h1>{pokemon.name}</h1>
          <img src={pokemon.sprites.front_default} />
          <p>Height: {pokemon.height}</p>
          <p>Weight: {pokemon.weight}</p>
        </div>
        :
        <p>Loading...</p>
      }
    </>
  );
};

export default PokemonDetailsPage;
```

This component **does not receive props**. Everything it needs comes from the URL. Let's break it down a bit further. Here we conduct the following:

- Grab the ID parameter from the URL pattern
- Fetch a Pokemons data from the PokeAPI
- Anytime the ID parameter changes update the state of `pokemon`
- Once a Pokemon is present, render the Pokemon details

---

## What is `useNavigate`?

`useNavigate` is a hook that allows components to **change routes programmatically**.

Instead of relying on links, components can trigger navigation as a result of:

* Button clicks
* Form submissions
* Business logic

---

## Why Use `useNavigate` Instead of `Link`?

While `<Link>` is ideal for static navigation, `useNavigate` is preferred when:

* Navigation depends on data
* Navigation is triggered by logic
* Navigation is attached to non-anchor UI (buttons, cards)

In our case, clicking a Pokémon card button should navigate to a page **based on that Pokémon’s ID**.

---

## Updating the PokemonCard Component

We will now add a **“See Details”** button to each Pokémon card.

This button will:

* Read the Pokémon ID from props
* Navigate to `/pokemon/:id`

```jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function PokemonCard({ data }) {
  const [shiny, setShiny] = useState(false);
  const navigate = useNavigate();

  return (
    <div>
      <h2>{data.name}</h2>
      <img
        src={
          shiny
            ? data.sprites.front_shiny
            : data.sprites.front_default
        }
      />
      <button onClick={() => setShiny(!shiny)}>
        {shiny ? "un-shine" : "shine"}
      </button>

      <button onClick={() => navigate(`/pokemon/${data.id}`)}>
        See Details
      </button>
    </div>
  );
}

export default PokemonCard;
```

This keeps the card reusable while allowing it to participate in navigation.

---

## The Mental Model

At this point, the application follows a clean routing architecture:

* **Lists live on pages**
* **Details live at URL-specific routes**
* **URLs represent what the user is viewing**
* **Components do not own navigation state**

The URL `/pokemon/25` now fully represents:

> “The user is viewing Pikachu”

---

## Summary

In this lesson, you learned how to:

* Use `useParams` to read dynamic values from the URL
* Use `useNavigate` to programmatically change routes
* Build a real detail page backed by a public API
* Connect list views to detail views using routing
* Treat URLs as a source of application state

This pattern is foundational for building scalable React applications and mirrors how professional SPAs structure navigation and data flow.
