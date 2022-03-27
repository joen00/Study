import React from "react";
import { Form, Col, Button, Row, FloatingLabel } from "react-bootstrap";
import "./Login.css";
import { useHistory } from "react-router-dom";

function Createroom(props) {
  let history = useHistory();
  const [title, settitle] = React.useState("");
  const [password, setpassword] = React.useState("");
  const [score, setscore] = React.useState("");
  const [enterence_fee, setenterence_fee] = React.useState("");
  const [explain, setexplain] = React.useState("");
  const [grace_period, setgrace_period] = React.useState("");
  const [main_goal, setmain_goal] = React.useState("");
  const [max_user_count, setmax_user_count] = React.useState("");
  const [meeting_days, setmeeting_days] = React.useState("");
  const [meeting_times, setmeeting_times] = React.useState("");
  const [penalty, setpenalty] = React.useState("");
  const [period_renew, setperiod_renew] = React.useState("");
  const [season, setseason] = React.useState("");
  const [total_money, settotal_money] = React.useState("");
  const [user_count, setuser_count] = React.useState("");

  let token = localStorage.getItem("wtw-token") || "";

  return (
    <div className="logincontain">
      <Form>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            방 제목
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="방 제목"
              onChange={(e) => {
                settitle(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            비밀번호
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="비밀번호"
              onChange={(e) => {
                setpassword(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            점수
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="점수"
              onChange={(e) => {
                setscore(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            최대인원
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="최대인원"
              onChange={(e) => {
                setmax_user_count(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            총 인원
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="최대인원"
              onChange={(e) => {
                setuser_count(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            grace_period
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="grace_period"
              onChange={(e) => {
                setgrace_period(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            주/시간
          </Form.Label>
          <Col>
            <Form.Control
              type="Name"
              placeholder="1,2"
              onChange={(e) => {
                setmeeting_days(e.target.value);
              }}
            />
          </Col>
          <Col>
            <Form.Control
              type="Name"
              placeholder="2시간"
              onChange={(e) => {
                setmeeting_times(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            금액
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="금액"
              onChange={(e) => {
                setenterence_fee(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            총 금액
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="금액"
              onChange={(e) => {
                settotal_money(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            패널티
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="패널티"
              onChange={(e) => {
                setpenalty(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            period_renew
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="period_renew"
              onChange={(e) => {
                setperiod_renew(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            season
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="season"
              onChange={(e) => {
                setseason(1);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            목표
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="season"
              onChange={(e) => {
                setmain_goal(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        방의 관심분야에 체크해주세요
        <div className="checkhere">
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="스터디" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="운동" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="개발" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="면접" />
          </Form.Group>
        </div>
        <FloatingLabel controlId="floatingTextarea2" label="상세 안내 내용">
          <Form.Control
            as="textarea"
            placeholder="Leave a comment here"
            onChange={(e) => {
              setexplain(e.target.value);
            }}
            style={{ height: "500px" }}
          />
        </FloatingLabel>
        <br></br>
        <Button
          variant="primary"
          type="submit"
          onClick={() => {
            fetch("http://127.0.0.1:8000/main/newroom", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: "jwt " + token,
              },
              body: JSON.stringify({
                password: password,
                title: title,
                score: score,
                info: {
                  grace_period: grace_period,
                  max_user_count: max_user_count,
                  main_goal: main_goal,
                  period_renew: period_renew,
                  enterence_fee: enterence_fee,
                  meeting_days: meeting_days,
                  meeting_times: meeting_times,
                  penalty: penalty,
                  explain: explain,
                  season: season,
                  total_money: total_money,
                  user_count: user_count,
                },
              }),
            })
              .then((response) => response.json())
              .then((res) => {
                console.log(res.data);
                history.push("/");
              });
          }}
        >
          Submit
        </Button>
      </Form>
    </div>
  );
}

export default Createroom;
