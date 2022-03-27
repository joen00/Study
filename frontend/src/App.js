/* eslint-disable */
import "./App.css";
import React, { useState, useContext } from "react";
import { useHistory, useParams } from "react-router-dom";
import {
  Navbar,
  Container,
  NavDropdown,
  Nav,
  Card,
  ListGroup,
  ListGroupItem,
  Button,
} from "react-bootstrap";
import Data from "./data";
import Detail from "./Detail";
import Heartroom from "./Heartroom";
import Mypage from "./Mypage";
import Detailroom from "./Detailroom";
import axios from "axios";
import Room from "./Room";
import Login from "./Login.js";
import Signup from "./Signup.js";
import Createroom from "./Createroom.js";
import { FaHeart, FaRegHeart, FaBook } from "react-icons/fa";
import Keyword from "./Keyword.js";
import { Link, Route, Switch } from "react-router-dom";

export let 재고context = React.createContext();

function App() {
  let [studyroom, studyroomChange] = useState(Data);
  let [like, likeChange] = useState(false);
  let token = localStorage.getItem("wtw-token") || "";
  return (
    <div className="App">
      <Navbars />
      <Switch>
        <Route exact path="/">
          <div className="container">
            <button
              className="btn btn-primary"
              onClick={() => {
                axios
                  .get("/main/")
                  .then((result) => {
                    studyroomChange([...studyroom, ...result.data["results"]]);
                  })
                  .catch(() => {
                    console.log("실패했다");
                  });
              }}
            >
              더보기
            </button>
            <div className="row">
              {studyroom.map((a, i) => {
                return (
                  <Cardcomponent
                    studyroom={studyroom[i]}
                    i={i}
                    key={i}
                    like={like}
                    likeChange={likeChange}
                    token={token}
                  />
                );
              })}
            </div>
          </div>
        </Route>
        <Route path="/detail">
          <Detail studyroom={studyroom} />
        </Route>

        <Route path="/heart">
          <Heartroom studyroom={studyroom} />
        </Route>

        <Route path="/mypage">
          <Mypage studyroom={studyroom} />
        </Route>

        <Route path="/detailroom/:id">
          <Detailroom />
        </Route>

        <Route path="/room/:id">
          <Room studyroom={studyroom} />
        </Route>

        <Route path="/login">
          <Login studyroom={studyroom} />
        </Route>

        <Route path="/signup">
          <Signup studyroom={studyroom} />
        </Route>
        <Route path="/createroom">
          <Createroom studyroom={studyroom} />
        </Route>
        <Route path="/keyword/:id">
          <Keyword />
        </Route>
      </Switch>
    </div>
  );
}

function Cardcomponent(props) {
  return (
    <div className="col-md-3">
      <Card style={{ width: "18rem", margin: "1rem" }}>
        <Card.Img variant="top" />
        <Card.Body>
          <Card.Title>
            {props.studyroom.title}&nbsp;
            {props.like ? (
              <FaHeart
                style={{ color: "red", fontSize: "24px" }}
                onClick={() => {
                  props.like ? props.likeChange(false) : props.likeChange(true);
                }}
              />
            ) : (
              <FaRegHeart
                style={{ color: "red", fontSize: "24px" }}
                onClick={() => {
                  props.like ? props.likeChange(false) : props.likeChange(true);
                }}
              />
            )}
          </Card.Title>

          <Card.Text>{props.studyroom.date_register}</Card.Text>
        </Card.Body>
        <ListGroup className="list-group-flush">
          <ListGroupItem>{props.studyroom.id}</ListGroupItem>
          <ListGroupItem>{props.studyroom.owner}</ListGroupItem>
          <ListGroupItem>{props.studyroom.score}</ListGroupItem>
          <ListGroupItem>
            <Button
              variant="primary"
              type="submit"
              onClick={() => {
                fetch(
                  "http://127.0.0.1:8000/main/room/join/request/" +
                    props.studyroom.id,
                  {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                      Authorization: "jwt " + props.token,
                    },
                    body: JSON.stringify({}),
                  }
                )
                  .then((response) => response.json())
                  .then((res) => {
                    console.log(res.data);
                    history.push("/");
                  });
              }}
            >
              방 입장 요청
            </Button>
          </ListGroupItem>
        </ListGroup>
        <Card.Body>
          <Card.Link as={Link} to={`/detailroom/${props.studyroom.id}`}>
            방 세부사항
          </Card.Link>
          <Card.Link as={Link} to={`/keyword/${props.studyroom.id}`}>
            키워드 설정
          </Card.Link>
          <Card.Link as={Link} to={`/room/${props.studyroom.id}`}>
            방 입장하기
          </Card.Link>
        </Card.Body>
      </Card>
    </div>
  );
}

function Navbars(props) {
  let history = useHistory();
  let token = localStorage.getItem("wtw-token") || "";
  const onClickHandler = () => {
    fetch("http://127.0.0.1:8000/oneuser/rest-auth/logout/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    })
      .then((response) => response.json())
      .then((response) => {
        alert("로그아웃");
        history.push("/");
      });
  };
  return (
    <div>
      <Navbar bg="light" expand="lg">
        <Container>
          <Navbar.Brand as={Link} to="/">
            <FaBook
              style={{ color: "green", fontSize: "30px", marginRight: "7%" }}
            />
            StudyOne
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/">
                Home
              </Nav.Link>
              <Nav.Link as={Link} to="/detail">
                Detail
              </Nav.Link>
              <Nav.Link as={Link} to="/heart">
                Heart&nbsp;
                <FaHeart style={{ color: "red", fontSize: "20px" }} />
              </Nav.Link>
              <NavDropdown title="MyPage" id="basic-nav-dropdown">
                <NavDropdown.Item as={Link} to="/mypage">
                  MyPage
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/login">
                  login
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/signup">
                  sign up
                </NavDropdown.Item>
                <NavDropdown.Item>
                  <button onClick={onClickHandler}>로그아웃</button>
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item as={Link} to="/createroom">
                  방 개설하기
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}
export default App;
