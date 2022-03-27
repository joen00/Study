import React from "react";
import { Badge } from "react-bootstrap";
function Mainroomscore(props) {
  return (
    <div>
      <div>
        <h6 className="hi">현재 점수 : &nbsp;&nbsp;</h6>
        <h3>
          <Badge bg="warning" text="dark">
            {props.score}
          </Badge>
        </h3>
      </div>
    </div>
  );
}

export default Mainroomscore;
