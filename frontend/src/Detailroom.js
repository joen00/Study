import React, { useState, useRef, useEffect } from "react";
import { useHistory, useParams } from "react-router-dom";
import { Offcanvas, Card, Overlay, Popover } from "react-bootstrap";
import axios from "axios";
import "./Detailroom.css";
import Mainselect from "./Mainselect.js";

// axios.get("/main/room/info/" + id).then((reponse) => {
//   setDatas(reponse.data);
// });

function Detailroom(props) {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const [show1, setShow1] = useState(false);
  const [target, setTarget] = useState(null);
  const ref = useRef(null);

  const handleClick = (event) => {
    setShow1(!show1);
    setTarget(event.target);
  };
  let token = localStorage.getItem("wtw-token") || "";
  let { id } = useParams();
  const [Mai, setMai] = useState([]);
  const [datas, setDatas] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/main/room/info/" + id, {
      headers: {
        Authorization: "jwt " + token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setMai([data]);
        setDatas(data);
      });
  }, []);

  return (
    <div className="container">
      <Offcanvas show={show} onHide={handleClose}>
        <Offcanvas.Header closeButton>
          <h2>DetailInfo</h2>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <div ref={ref}>
            <button
              type="button"
              className="btn"
              id="detailbtn"
              onClick={handleClick}
            >
              방장 ID
            </button>
            <Overlay
              show={show1}
              target={target}
              placement="bottom"
              container={ref}
              containerPadding={20}
            >
              <Popover id="popover-contained">
                <Popover.Header as="h3">방장의 평점</Popover.Header>
                <Popover.Body>
                  <strong>연락하기</strong>
                </Popover.Body>
              </Popover>
            </Overlay>
          </div>
          <hr />
          <div className="maindetail">{/* <p>{datas["id"]}</p> */}</div>
          <hr />
          <button type="button" className="btn" id="detailbtn">
            방 입장하기
          </button>
        </Offcanvas.Body>
      </Offcanvas>
      <div className="detailinforoom">
        <Card className="text-center">
          <Card.Header className="detailgoal">방 제목</Card.Header>
          <Card.Body>
            <Card.Text>
              <div style={{ width: "100%", margin: "0" }}>
                {datas && (
                  <Mainselect
                    id={datas.id}
                    explain={datas.explain}
                    grace_period={datas.grace_period}
                    max_user_count={datas.max_user_count}
                    user_count={datas.user_count}
                    date_renew={datas.date_renew}
                    period_renew={datas.period_renew}
                    enterence_fee={datas.enterence_fee}
                    total_money={datas.total_money}
                    meeting_days={datas.meeting_days}
                    meeting_times={datas.meeting_times}
                    penalty={datas.penalty}
                    classroombasic_pk={datas.classroombasic_pk}
                    keywords={datas.keywords}
                  />
                )}
              </div>
            </Card.Text>
            <Card.Text>
              <div style={{ width: "100%", margin: "0" }}>
                <button
                  type="button"
                  className="btn"
                  id="detailbtn"
                  onClick={() => {
                    fetch("http://127.0.0.1:8000/main/interest/" + id, {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json",
                        Authorization: "jwt " + token,
                      },
                      body: JSON.stringify({}),
                    })
                      .then((response) => response.json())
                      .then((res) => {
                        console.log(res.data);
                      });
                  }}
                >
                  좋아요
                </button>
              </div>
            </Card.Text>
          </Card.Body>
          <Card.Footer className="text-muted">
            <button
              type="button"
              className="btn"
              id="detailbtn"
              onClick={handleShow}
            >
              방 입장하기
            </button>
          </Card.Footer>
        </Card>
      </div>
    </div>
  );
}

export default Detailroom;
