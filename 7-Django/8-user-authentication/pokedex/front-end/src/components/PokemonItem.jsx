import { useState, useEffect } from "react";
import axios from "axios";

export const PokemonItem = ({ pokemon }) => {
  const [nounProjectIcon, setNounProjectIcon] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [newType, setNewType] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [captured, setCaptured] = useState(pokemon.captured);
  const [levelUp, setLevelUp] = useState(false);

  const getIcon = async () => {
    let response = await axios
      .get(`http://127.0.0.1:8000/api/v1/noun/${pokemon.type}/`)
      .catch((err) => {
        console.log(err);
        alert("Problems getting Icon");
      });
    setNounProjectIcon(response.data);
  };

  const updatePokemon = async (e) => {
    e.preventDefault();
    let data = {
      type: newType,
      captured: captured,
      level_up: levelUp,
      description: newDescription,
    };
    console.log(data)
    let response = await axios
      .put(`http://127.0.0.1:8000/api/v1/pokemon/${pokemon.id}/`, data)
      .catch((err) => {
        alert("couldn't update pokemon");
        console.error(err);
      });
    if (response.status === 204) {
      window.location.reload();
    }
  };

  const deleteAPokemon = async() => {
    let response = await axios
      .delete(`http://127.0.0.1:8000/api/v1/pokemon/${pokemon.id}/`)
      .catch((err)=>{
        alert("could not delete a pokemon")
        console.error(err)
      })
    if (response.status === 204){
      window.location.reload()
    }
  }

  useEffect(() => {
    getIcon();
  }, []);

  return (
    <li
      style={{
        margin: "3vmin",
        display: "flex",
        flexDirection: "column",
      }}
    >
      Name: {pokemon.name}
      <button onClick={deleteAPokemon}>Delete</button>
      {showForm ? (
        <form onSubmit={(e) => updatePokemon(e)}>
          <br />
          <input
            type="text"
            placeholder={pokemon.type}
            onChange={(e) => setNewType(e.target.value)}
          />
          <input
            type="text"
            placeholder={pokemon.description}
            onChange={(e) => setNewDescription(e.target.value)}
          />
          <div>
            <label>
              <input
                type="checkbox"
                id="caught"
                name="caught"
                checked={captured}
                onChange={(e) => setCaptured(e.target.checked)}
              />
              Caught
            </label>
            <label>
              <input
                type="checkbox"
                id="level"
                name="level"
                checked={levelUp}
                onChange={(e) => setLevelUp(e.target.checked)}
              />
              Level Up
            </label>
          </div>
          <button onClick={() => setShowForm(!showForm)}>CANCEL</button>
          <input type="submit" placeholder="Submit" />
        </form>
      ) : (
        <>
          <br /> Level: {pokemon.level}
          <ul>
            {nounProjectIcon ? (
              <img
                style={{ height: "5vmin", width: "5vmin" }}
                src={nounProjectIcon}
              />
            ) : null}
            Moves
            {pokemon.moves.map((move, idx) => (
              <li key={`${pokemon.id}${idx}`}>{move}</li>
            ))}
          </ul>
          Description: {pokemon.description}
          <br />
          {pokemon.captured ? <>Captured</> : <>Not Captured</>}
          <button onClick={() => setShowForm(!showForm)}>EDIT</button>
        </>
      )}
    </li>
  );
};
