import React from "react";

function Subgoal(props) {
  return (
    <div>
      <div>
        {props.subgoaldatas.map((a, i) => {
          return (
            <div>
              <p style={{ color: "black", fontSize: "1rem" }}>
                id :{props.subgoaldatas[i].id}&nbsp;&nbsp; 서브 제목 :
                {props.subgoaldatas[i].title} &nbsp;&nbsp; 설명 :
                {props.subgoaldatas[i].explain}&nbsp;&nbsp; 기간 마감 :
                {props.subgoaldatas[i].date_end}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Subgoal;
