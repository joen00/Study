import React, { useState, useRef, useEffect } from "react";

import p1 from "./p1.png";
import p2 from "./p2.png";
import p3 from "./p3.png";
import {
  ProgressBar,
  Accordion,
  Form,
  Badge,
  Button,
  Offcanvas,
  Col,
  Row,
  Card,
} from "react-bootstrap";
import { useParams } from "react-router-dom";
import "./Room.css";
import { propTypes } from "react-bootstrap/esm/Image";
import Mainselect from "./Mainselect.js";
import Mainroomscore from "./Mainroomscore.js";
import Subgoal from "./Subgoal.js";
import User from "./User.js";
import { Link, Route, Switch } from "react-router-dom";
import Chathistory from "./Chathistory.js";
import Myinfo from "./Myinfo.js";

function Room(props) {
  const now = 60;
  const [show, setShow] = useState(false);
  const [show1, setShow1] = useState(false);
  const [show2, setShow2] = useState(false);
  const [show3, setShow3] = useState(false);
  const [show4, setShow4] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleClose1 = () => setShow1(false);
  const handleShow1 = () => setShow1(true);
  const handleClose2 = () => setShow2(false);
  const handleShow2 = () => setShow2(true);
  const handleClose3 = () => setShow3(false);
  const handleShow3 = () => setShow3(true);
  const handleClose4 = () => setShow4(false);
  const handleShow4 = () => setShow4(true);

  let { id } = useParams();
  const [Q1, setQ1] = React.useState(null);
  const [Q2, setQ2] = React.useState(null);
  const [score, setscore] = React.useState("");
  let token = localStorage.getItem("wtw-token") || "";

  const [Mai, setMai] = useState([]);
  const [datas, setDatas] = useState(null);

  const [Mairomms, setMairomms] = useState([]);
  const [datas1, setDatas1] = useState(null);

  const [method, setmethod] = useState("");
  const [title, settitle] = useState("");
  const [attribute, setattribute] = useState("");
  const [explain, setexplain] = useState("");
  const [date_start, setdate_start] = useState("");
  const [date_end, setdate_end] = useState("");
  const [attend, setattend] = useState("");

  const [userid, setuserid] = useState("");
  const [userscore, setuserscore] = useState("");

  const [subgoal, setsubgoal] = useState([]);
  const [subgoaldatas, setsubgoalDatas] = useState(null);

  const [userinfo, setuserinfo] = useState([]);
  const [userinfodatas, setuserinfoDatas] = useState(null);

  const [chathistorys, setchathistorys] = useState([]);
  const [chathistorydatas, setchathistoryDatas] = useState(null);

  const [myinfos, setmyinfos] = useState([]);
  const [myinfodatas, setmyinfosDatas] = useState(null);

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
    fetch("http://127.0.0.1:8000/main/room/subgoals/" + id, {
      headers: {
        Authorization: "jwt " + token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setsubgoal([data]);
        setsubgoalDatas(data);
      });
    fetch("http://127.0.0.1:8000/main/room/user/list/" + id, {
      headers: {
        Authorization: "jwt " + token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setuserinfo([data]);
        setuserinfoDatas(data);
      });

    fetch("http://127.0.0.1:8000/main/room/chat/history/" + id, {
      headers: {
        Authorization: "jwt " + token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setchathistorys([data["results"]]);
        setchathistoryDatas(data["results"]);
      });
    fetch("http://127.0.0.1:8000/oneuser/info", {
      headers: {
        Authorization: "jwt " + token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setmyinfos([data]);
        setmyinfosDatas(data);
      });
  }, []);

  return (
    <div className="main">
      <div className="first">
        <div className="box" id="pororo">
          <img
            className="profile"
            src="https://cdn.pixabay.com/photo/2021/07/23/15/04/coffee-6487522_960_720.jpg"
          />
        </div>

        <div style={{ width: "100%", margin: "0" }}>
          {myinfodatas && (
            <Myinfo
              id={myinfodatas.id}
              username={myinfodatas.username}
              score={myinfodatas.score}
              group_joined={myinfodatas.group_joined}
              user_goal={myinfodatas.user_goal}
              keywords={myinfodatas.keywords}
              email={myinfodatas.email}
            />
          )}
        </div>

        <br></br>
        <>
          <button type="button" className="btn" id="btn4" onClick={handleShow}>
            시각화
          </button>
          <Offcanvas show={show} onHide={handleClose}>
            <Offcanvas.Header closeButton>
              <Offcanvas.Title>세부사항</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
              <div>
                <img alt="p1" width="100%" height="100%" src={p1} />
                <img alt="p2" width="100%" height="100%" src={p2} />
                <img alt="p3" width="100%" height="100%" src={p3} />
              </div>
            </Offcanvas.Body>
          </Offcanvas>
        </>
      </div>
      <div className="second">
        <br></br>
        <br></br>
        <br></br>
        <button
          type="button"
          className="btn"
          id="btn4"
          onClick={() =>
            window.open("http://127.0.0.1:8080/main/room/video/" + id, "_blank")
          }
        >
          회의 방으로 바로 가기
        </button>
        <div>
          {chathistorydatas && (
            <Chathistory chathistorydatas={chathistorydatas} />
          )}
        </div>
      </div>

      <div className="thrid">
        <Accordion defaultActiveKey="1">
          <Accordion.Item eventKey="0">
            <Accordion.Header>방 제목</Accordion.Header>
            <Accordion.Body className="thrid-1-1">
              <button
                type="button"
                className="btn"
                id="btn4"
                onClick={handleShow1}
              >
                상세내용
              </button>
              &nbsp;&nbsp;
              <button
                type="button"
                className="btn"
                id="btn4"
                onClick={handleShow3}
              >
                설정
              </button>
              <Offcanvas show={show1} onHide={handleClose1}>
                <Offcanvas.Header closeButton>
                  <Offcanvas.Title>상세 내용</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                  <div>
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
                          score={datas.score}
                        />
                      )}
                    </div>
                    <div>
                      <p>
                        Q1) 해당 스터디에 만족하셨나요? or 해당 스터디가
                        사용자의 목적에 적합한 스터디였나요?
                      </p>
                      <p>매우 그렇다면 5점 그렇지 않다면 1점</p>
                      <Form.Control
                        className="hi2"
                        type="text"
                        placeholder="평점 입력"
                        onChange={(e) => {
                          setQ1(e.target.value);
                        }}
                      />
                    </div>
                    <br></br>
                    <br></br>
                    <br></br>
                    <div>
                      <p>
                        Q2) 해당 스터디에 불만족하셨나요? or 해당 스터디가
                        사용자의 목적에 부적합한 스터디였나요?
                      </p>
                      <p>매우 그렇다면 5점 그렇지 않다면 1점</p>
                      <Form.Control
                        className="hi2"
                        type="text"
                        placeholder="평점 입력"
                        onChange={(e) => {
                          setQ2(e.target.value);
                        }}
                      />
                      <br></br>
                      <br></br>
                      <br></br>
                      <p>점수를 1 ~ 5점 사이로 평가해주세요</p>
                      <Form.Control
                        className="hi2"
                        type="text"
                        placeholder="점수 입력"
                        onChange={(e) => {
                          setscore(e.target.value);
                        }}
                      />
                    </div>
                    &nbsp;&nbsp;
                    <Cal
                      Q1={Q1}
                      Q2={Q2}
                      score={score}
                      setscore={setscore}
                      id={id}
                      token={token}
                    />
                  </div>
                </Offcanvas.Body>
              </Offcanvas>
              <Offcanvas show={show3} onHide={handleClose3}>
                <Offcanvas.Header closeButton></Offcanvas.Header>
                <Offcanvas.Body>
                  <div>
                    <Form>
                      <p>생성 : CREATE / 업데이트 : UPDATE / 삭제 : DELETE</p>
                      <Form.Control
                        className="hi2"
                        type="text"
                        placeholder="method"
                        onChange={(e) => {
                          setmethod(e.target.value);
                        }}
                      />
                      <br></br>
                      <br></br>
                      <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">
                          제목
                        </Form.Label>
                        <Col sm="10">
                          <Form.Control
                            type="Name"
                            placeholder="제목"
                            onChange={(e) => {
                              settitle(e.target.value);
                            }}
                          />
                        </Col>
                      </Form.Group>
                      <p>
                        sub_goal : 1 / homework : 2 / meeting : 3 / other(import
                        day) : 4
                      </p>
                      <Form.Control
                        type="Name"
                        placeholder="attribute"
                        onChange={(e) => {
                          setattribute(e.target.value);
                        }}
                      />
                      <br></br>
                      <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">
                          설명
                        </Form.Label>
                        <Col sm="10">
                          <Form.Control
                            type="Name"
                            placeholder="explain"
                            onChange={(e) => {
                              setexplain(e.target.value);
                            }}
                          />
                        </Col>
                      </Form.Group>
                      <p>시작 날짜 : 년도-월-일T시:분</p>
                      <Form.Control
                        type="Name"
                        placeholder="date_start"
                        onChange={(e) => {
                          setdate_start(e.target.value);
                        }}
                      />
                      <br></br>
                      <p>끝나는 날짜 : 년도-월-일T시:분</p>
                      <Form.Control
                        type="Name"
                        placeholder="date_end"
                        onChange={(e) => {
                          setdate_end(e.target.value);
                        }}
                      />
                      <br></br>
                      <Button
                        variant="primary"
                        type="submit"
                        onClick={() => {
                          fetch(
                            "http://127.0.0.1:8000/main/room/subgoals/" + id,
                            {
                              method: "POST",
                              headers: {
                                "Content-Type": "application/json",
                                Authorization: "jwt " + token,
                              },
                              body: JSON.stringify({
                                method: method,
                                title: title,
                                attribute: attribute,
                                explain: explain,
                                date_start: date_start,
                                date_end: date_end,
                              }),
                            }
                          )
                            .then((response) => response.json())
                            .then((res) => {
                              console.log(res.data);
                            });
                        }}
                      >
                        Submit
                      </Button>
                    </Form>
                  </div>
                </Offcanvas.Body>
              </Offcanvas>
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>

        <Accordion defaultActiveKey="1">
          <Accordion.Item eventKey="0">
            <Accordion.Header>참여한 사람들</Accordion.Header>
            <Accordion.Body className="thrid-1-1">
              <button
                type="button"
                className="btn"
                id="btn4"
                onClick={handleShow2}
              >
                팀원 평가
              </button>
              <Offcanvas show={show2} onHide={handleClose2}>
                <Offcanvas.Header closeButton>
                  <Offcanvas.Title>참여한 유저들</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                  <div>
                    <div>
                      {userinfodatas && <User userinfodatas={userinfodatas} />}
                    </div>
                    <Form>
                      <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">
                          id
                        </Form.Label>
                        <Col sm="10">
                          <Form.Control
                            type="Name"
                            placeholder="id"
                            onChange={(e) => {
                              setuserid(e.target.value);
                            }}
                          />
                        </Col>
                      </Form.Group>
                      <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">
                          score
                        </Form.Label>
                        <Col sm="10">
                          <Form.Control
                            type="Name"
                            placeholder="score"
                            onChange={(e) => {
                              setuserscore(e.target.value);
                            }}
                          />
                        </Col>
                      </Form.Group>
                      <br></br>
                      <Button
                        variant="primary"
                        type="submit"
                        onClick={() => {
                          fetch(
                            "http://127.0.0.1:8000/main/room/user/score/" + id,
                            {
                              method: "POST",
                              headers: {
                                "Content-Type": "application/json",
                                Authorization: "jwt " + token,
                              },
                              body: JSON.stringify({
                                ratee: userid,
                                score: userscore,
                              }),
                            }
                          )
                            .then((response) => response.json())
                            .then((res) => {
                              console.log(res.data);
                            });
                        }}
                      >
                        Submit
                      </Button>
                    </Form>
                  </div>
                </Offcanvas.Body>
              </Offcanvas>
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>

        <div className="thrid-3">
          <button
            type="button"
            className="btn btn-default btn-lg btn-block"
            id="btn4"
            onClick={handleShow4}
          >
            출석체크
          </button>
          <Offcanvas show={show4} onHide={handleClose4}>
            <Offcanvas.Header closeButton></Offcanvas.Header>
            <Offcanvas.Body>
              <div>
                <p> 서브 목표 출석체크 </p>
                <div>
                  {subgoaldatas && <Subgoal subgoaldatas={subgoaldatas} />}
                </div>
                <Form>
                  <Form.Group as={Row} className="mb-3">
                    <Form.Label column sm="2">
                      id
                    </Form.Label>
                    <Col sm="10">
                      <Form.Control
                        type="Name"
                        placeholder="id"
                        onChange={(e) => {
                          setattend(e.target.value);
                        }}
                      />
                    </Col>
                  </Form.Group>
                  <br></br>
                  <Button
                    variant="primary"
                    type="submit"
                    onClick={() => {
                      fetch(
                        "http://127.0.0.1:8000/main/room/attendtion/" +
                          id +
                          "/" +
                          attend,
                        {
                          method: "POST",
                          headers: {
                            "Content-Type": "application/json",
                            Authorization: "jwt " + token,
                          },
                          body: JSON.stringify({
                            attendance: true,
                          }),
                        }
                      )
                        .then((response) => response.json())
                        .then((res) => {
                          console.log(res.data);
                        });
                    }}
                  >
                    Submit
                  </Button>
                </Form>
              </div>
            </Offcanvas.Body>
          </Offcanvas>
        </div>
        <div className="thrid-4">
          <hr />
          업로드된 파일들
        </div>
        <div className="thrid-5">
          <Form.Group controlId="formFileMultiple" className="mb-3">
            <Form.Control type="file" multiple />
          </Form.Group>
        </div>
      </div>
    </div>
  );
}

function Cal(props) {
  if (props.Q1 == 5 && props.Q2 == 5) {
    props.setscore(3);
    return (
      <Button
        variant="primary"
        type="submit"
        onClick={() => {
          fetch("http://127.0.0.1:8000/main/room/score/" + props.id, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "jwt " + props.token,
            },
            body: JSON.stringify({
              score: props.score,
            }),
          })
            .then((response) => response.json())
            .then((res) => {
              console.log(res.data);
            });
        }}
      >
        Submit
      </Button>
    );
  } else if (props.Q1 == 1 && props.Q2 == 1) {
    props.setscore(3);
    return (
      <Button
        variant="primary"
        type="submit"
        onClick={() => {
          fetch("http://127.0.0.1:8000/main/room/score/" + props.id, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "jwt " + props.token,
            },
            body: JSON.stringify({
              score: props.score,
            }),
          })
            .then((response) => response.json())
            .then((res) => {
              console.log(res.data);
            });
        }}
      >
        Submit
      </Button>
    );
  } else {
    return (
      <Button
        variant="primary"
        type="submit"
        onClick={() => {
          fetch("http://127.0.0.1:8000/main/room/score/" + props.id, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "jwt " + props.token,
            },
            body: JSON.stringify({
              score: props.score,
            }),
          })
            .then((response) => response.json())
            .then((res) => {
              console.log(res.data);
            });
        }}
      >
        Submit
      </Button>
    );
  }
}

export default Room;
