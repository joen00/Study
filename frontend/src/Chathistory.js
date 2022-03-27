import React from "react";

function Chathistory(props) {
  return (
    <div>
      <div>
        {props.chathistorydatas.map((a, i) => {
          return (
            <div>
              <p style={{ color: "black", fontSize: "1rem" }}>
                {props.chathistorydatas[i].content}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Chathistory;
