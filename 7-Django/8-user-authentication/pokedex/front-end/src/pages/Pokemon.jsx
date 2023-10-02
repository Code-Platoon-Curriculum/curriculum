import Row from "react-bootstrap/esm/Row";
import { useEffect, useState } from "react";
import axios from "axios";
import { PokemonItem } from "../components/PokemonItem";

export const Pokemon = () => {
  const [pokemon, setPokemon] = useState([]);
  const [name, setName] = useState("");
  const [level, setLevel] = useState(0);
  const [captured, setCaptured] = useState(false);
  const [type, setType] = useState("");
  const [description, setDescription] = useState("");

  const getAllPokemon = async () => {
    // request would be sent within this function
    let response = await axios
      .get("http://127.0.0.1:8000/api/v1/pokemon/")
      .catch((err) => {
        console.log(err);
        alert("something went wrong");
      });
    console.log(response.data);
    setPokemon(response.data);
  };

  useEffect(() => {
    getAllPokemon();
  }, []);

  const createAPokemon = async(e) => {
    e.preventDefault()
    let data = {
      "name":name,
      "level":level,
      "description":description,
      "captured":captured,
      "type":type
    }
    console.log(data)
    let response = await axios
      .post("http://127.0.0.1:8000/api/v1/pokemon/", data)
      .catch((err)=>{
        alert("could not create Pokemon")
        console.error(err)
      })
    if (response.status === 201){
      window.location.reload()
    }
  }

  return (
    <Row style={{ padding: "0 10vmin" }}>
      <form onSubmit={(e)=>createAPokemon(e)}>
        <h2>Create a Pokemon</h2>
        <input
          type="text"
          placeholder="Pokemon Name"
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Pokemon Type"
          onChange={(e) => setType(e.target.value)}
        />
        <input
          type="number"
          placeholder="Pokemon Level"
          onChange={(e) => setLevel(e.target.value)}
        />
        <textarea
          placeholder="description"
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
        <label>
          Captured
          <input
            type="checkbox"
            onChange={(e) => setCaptured(e.target.checked)}
          />
        </label>
        <input type="submit" value="create" />
      </form>
      <h1 style={{ textAlign: "center" }}>Pokemon</h1>
      <ul>
        {pokemon.map((poke) => (
          <PokemonItem key={poke.id} pokemon={poke} />
        ))}
      </ul>
    </Row>
  );
};
