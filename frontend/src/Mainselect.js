import React from "react";
import { Badge } from "react-bootstrap";

function Mainselect(props) {
  return (
    <div>
      <div>
        <h2 style={{ color: "black" }}>{props.id}</h2>
        <p style={{ color: "black", fontSize: "1rem" }}>
          방의 설명 : {props.explain}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          grace_period : {props.grace_period}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          최대 인원 : {props.max_user_count}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          현재 인원 : {props.user_count}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          최종 목표 : {props.main_goal}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          생성된 날짜 : {props.date_renew}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          갱신하는 날짜 : {props.period_renew}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          들어올때 금액 : {props.enterence_fee}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          총 금액 : {props.total_money}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          만나는 요일 : {props.meeting_days}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          만나는 시간 : {props.meeting_times}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          패널티 : {props.penalty}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          방의 pk값 : {props.classroombasic_pk}
        </p>
        <p style={{ color: "black", fontSize: "1rem" }}>
          방의 키워드 : {props.keywords}
        </p>
        <h6 className="hi"> 방의 평점 : &nbsp;&nbsp;</h6>
        <h3>
          <Badge bg="warning" text="dark">
            {props.score}
          </Badge>
        </h3>
      </div>
    </div>
  );
}

export default Mainselect;
