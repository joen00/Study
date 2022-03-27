import React, { useState, useRef, useEffect } from "react";
import { useHistory, useParams } from "react-router-dom";
import { Tab, Nav, Row, Col, Card, Button } from "react-bootstrap";
import "./Mypage.css";
import UserKeyword from "./UserKeyword.js";
import { Link, Route, Switch } from "react-router-dom";
import Room_per_req from "./Room_per_req.js";
import Interestcheck from "./Interestcheck.js";
import Myinfo from "./Myinfo.js";

function Mypage(props) {
  let token = localStorage.getItem("wtw-token") || "";
  let { id } = useParams();

  const [Mai, setMai] = useState([]);
  const [datas, setDatas] = useState(null);

  const [interest, setinterest] = useState([]);
  const [interestdatas, setinterestDatas] = useState(null);
  const [myinfos, setmyinfos] = useState([]);
  const [myinfodatas, setmyinfosDatas] = useState(null);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/main/interest/list", {
      headers: {
        Authorization: "jwt " + token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setinterest([data]);
        setinterestDatas(data);
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
    <div className="container">
      <Switch>
        <Route path="/mypage/userkeyword">
          <UserKeyword />
        </Route>
      </Switch>
      <Card.Link as={Link} to="/mypage/userkeyword">
        유저 키워드
      </Card.Link>
      <Tab.Container id="left-tabs-example" defaultActiveKey="first">
        <Row>
          <Col sm={3}>
            <Nav variant="pills" className="flex-column">
              <Nav.Item>
                <Nav.Link eventKey="first">내 정보</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="second">개설한 방</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="three">방 입장</Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={9}>
            <Tab.Content>
              <Tab.Pane eventKey="first">
                <Card className="text-center">
                  <Card.Header>My ID</Card.Header>
                  <Card.Body>
                    <Card.Text>
                      <div className="box" id="pororo">
                        <img
                          className="profile"
                          src="https://cdn.pixabay.com/photo/2021/07/23/15/04/coffee-6487522_960_720.jpg"
                        />
                      </div>
                      <br></br>
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
                      <p>내가 좋아요 누른 방 목록</p>
                      <div>
                        {interestdatas && (
                          <Interestcheck interestdatas={interestdatas} />
                        )}
                      </div>
                    </Card.Text>
                  </Card.Body>
                  <Card.Footer className="text-muted">프로필 수정</Card.Footer>
                </Card>
              </Tab.Pane>
              <Tab.Pane eventKey="second">
                <Sonnet2 />
              </Tab.Pane>
              <Tab.Pane eventKey="three">
                <Sonnet3
                  token={token}
                  id={id}
                  Mai={Mai}
                  setMai={setMai}
                  datas={datas}
                  setDatas={setDatas}
                />
              </Tab.Pane>
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
      <div className="container"></div>
    </div>
  );
}

function Sonnet2() {
  return (
    <div>
      <Card className="text-center">
        <Card.Header>개설한 방</Card.Header>
        <Card.Body>
          <Card.Text>
            <p>
              코딩 스터디 7/10
              <button type="button" className="btn" id="btn1">
                삭제
              </button>
            </p>
            <p>
              취업 스터디 9/15
              <button type="button" className="btn" id="btn1">
                삭제
              </button>
            </p>
          </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
}

function Sonnet3(props) {
  useEffect(() => {
    fetch("http://127.0.0.1:8000/main/room/permission/request", {
      headers: {
        Authorization: "jwt " + props.token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        props.setMai([data.results]);
        props.setDatas(data.results[0]);
      });
  }, []);
  return (
    <div>
      <Card className="text-center">
        <Card.Header>방 입장</Card.Header>
        <Card.Body>
          <Card.Text>
            <div className="openroom">
              <div style={{ width: "100%", margin: "0" }}>
                {props.datas && (
                  <Room_per_req
                    id={props.datas.id}
                    classroombasic_pk={props.datas.classroombasic_pk}
                    user_pk={props.datas.user_pk}
                  />
                )}
              </div>
            </div>
          </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Mypage;
