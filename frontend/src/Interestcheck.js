import React, { useState, useRef, useEffect } from "react";

function Interestcheck(props) {
  return (
    <div>
      <div>
        {props.interestdatas.map((a, i) => {
          return (
            <div>
              <p style={{ color: "black", fontSize: "1rem" }}>
                방 : {props.interestdatas[i].room_pk}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Interestcheck;
