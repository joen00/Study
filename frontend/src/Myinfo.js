import React from "react";

function Myinfo(props) {
  return (
    <div>
      <div>
        <p style={{ fontSize: "20px", fontWeight: "bold" }}>
          나의 ID : {props.username}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          이메일 : {props.email}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          나의 목표 : {props.user_goal}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          나의 키워드 : {props.keywords}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          score : {props.score}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          가입된 방 : {props.group_joined}
        </p>
      </div>
    </div>
  );
}

export default Myinfo;
