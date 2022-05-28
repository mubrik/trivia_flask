import React from 'react';


const mainDivStyles = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "4px",
  margin: "2px"
}

// const mainFormStyles = {
//   display: "flex",
//   alignItems: "center",
//   padding: "4px",
//   margin: "2px"
// }

const notificationStyles = {
  display: "flex", 
  alignItems: "center", 
  marginBottom: "4px",
  border: "1px solid red",
  borderRadius: "8px",
  width: "60%"
}

export default () => {

  const [user, setUser] = React.useState(null);
  const [msg, setMsg] = React.useState(false);

  const handleUsernameSubmit = async (event) =>  {
    event.preventDefault();

    const form = document.getElementById("username-form");
    const formData = new FormData(form);
    const _username = formData.get("username")

    const result = await fetch(`/api/users/${_username}`);

    console.log(result);
    if (result.ok) {
      const _user = await result.json();
      console.log(_user);
      setUser(_user.user);
    } else {
      setMsg(true);
    }
  };




  return(
    <div style={mainDivStyles}>
      {
        user ? 
        <div style={mainDivStyles}>
          <h2> Last 10 sessions </h2>
          { 
            (user.scores.length === 0) ?
              <h2> No session played yet </h2>:
            (user.scores.length > 10) ?
              user.scores
              .slice(user.scores.length - 10, user.scores.length)
              .map((_score, index) => {
                return <p key={index}> Session {index+1}: {_score}</p>
              })
              :
            user.scores.map((_score, index) => {
              return <p key={index}> Session {index+1}: {_score}</p>
            })
          }
        </div> :
        <form onSubmit={handleUsernameSubmit} id="username-form" style={{marginTop: "6px", alignItems:"center"}}>
          {/* <input type='text' name='username'/>
          <input
            className='submit-guess button'
            type='submit'
            value='Input Username'
          /> */}
          <div style={{ display: "flex", alignItems: "center", marginBottom: "4px"}}>
            <label htmlFor={"username"}> Username:</label>
            <input type='text' name='username' style={{ marginLeft: "4px"}} required/>
          </div>
          <input
            className='show-answer'
            type='submit'
            value='Submit'
          />
        </form>
      }
      {
        (msg) && 
        <div style={notificationStyles}>
          <p> Error, User does not exist </p>
          <button style={{ marginLeft: "auto"}} onClick={() => setMsg(false)}> close </button>
        </div>
      }
    </div>
  );
};