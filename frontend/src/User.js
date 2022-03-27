import React from "react";

function User(props) {
  return (
    <div>
      <div>
        {props.userinfodatas.map((a, i) => {
          return (
            <div>
              <p style={{ color: "black", fontSize: "1rem" }}>
                이름 : {props.userinfodatas[i].name} &nbsp;&nbsp; id :
                {props.userinfodatas[i].user_pk}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default User;
