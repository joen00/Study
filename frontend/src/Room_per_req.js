import React, { useState, useRef, useEffect } from "react";

function Room_per_req(props) {
  let token = localStorage.getItem("wtw-token") || "";
  return (
    <div>
      <div>
        <h2 style={{ color: "black" }}>{props.id}</h2>
        <p style={{ color: "black", fontSize: "1rem" }}>
          유저 번호 : {props.user_pk}&nbsp;&nbsp;&nbsp; 방의 번호 :
          {props.classroombasic_pk}
          <button
            type="button"
            className="btn"
            id="btn2"
            onClick={() => {
              fetch(
                "http://127.0.0.1:8000/main/room/permission/" +
                  props.classroombasic_pk,
                {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: "jwt " + token,
                  },
                  body: JSON.stringify({
                    guest: props.user_pk,
                    allow: 1,
                  }),
                }
              )
                .then((response) => response.json())
                .then((res) => {
                  console.log(res.data);
                });
            }}
          >
            입장
          </button>
          <button
            type="button"
            className="btn"
            id="btn1"
            onClick={() => {
              fetch(
                "http://127.0.0.1:8000/main/room/permission/" +
                  props.classroombasic_pk,
                {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: "jwt " + token,
                  },
                  body: JSON.stringify({
                    guest: props.user_pk,
                    allow: 2,
                  }),
                }
              )
                .then((response) => response.json())
                .then((res) => {
                  console.log(res.data);
                });
            }}
          >
            거부
          </button>
        </p>
      </div>
    </div>
  );
}

export default Room_per_req;
