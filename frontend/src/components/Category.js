import React from 'react';


const mainDivStyles = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "4px",
  margin: "2px"
}

const mainFormStyles = {
  display: "flex",
  alignItems: "center",
  padding: "4px",
  margin: "2px"
}

const notificationStyles = {
  display: "flex", 
  alignItems: "center", 
  marginBottom: "4px",
  border: "1px solid lightblue",
  borderRadius: "8px",
  width: "60%"
}

export default () => {

  const [category, setCategory] = React.useState("");
  const [msg, setMsg] = React.useState(null);

  const handleTextChange = (event) => {

    const newValue = event.target.value;

    setCategory(newValue);
  };

  const handleSubmitClick = (event) => {

    event.preventDefault();

    if (category === "") {
      alert("Category cannot be empty");
      return;
    }

    fetch("/api/categories", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({type: category})
    })
    .then(result => {
      result.json().then(res => {
        setMsg(res.category.type)
        console.log(res)
      })
    })
    .catch(error => {
      // too lazy to design border color change for notification, just alert error
      error.json().then(err => {
        if ("message" in err) {
          alert(err.mesage);
          return
        }
        console.log(err)
      })
    });
  };


  return(
    <div style={mainDivStyles}>
      <form style={mainFormStyles}>
        <div style={{ display: "flex", alignItems: "center", marginBottom: "4px"}}>
          <label htmlFor={"Category"}> Category:</label>
          <input type={"text"} onChange={handleTextChange} name={"Category"} style={{ marginLeft: "4px"}} required/>
        </div>
        <button className="show-answer" onClick={handleSubmitClick}> Submit</button>
      </form>
      {
        (msg !== null) && 
        <div style={notificationStyles}>
          <p> {msg} category has been created successfully </p>
          <button style={{ marginLeft: "auto"}} onClick={() => setMsg(null)}> close </button>
        </div>
      }
    </div>
  );
};