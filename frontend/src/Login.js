import React from "react";
import { Form, Col, Button, Row } from "react-bootstrap";
import "./Login.css";
import { useHistory, useParams } from "react-router-dom";

function Login(props) {
  let history = useHistory();
  const [username, setusername] = React.useState("");
  const [email, setemail] = React.useState("");
  const [password, setpassword] = React.useState("");

  return (
    <div className="logincontain">
      <Form>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            ID
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="ID"
              placeholder="ID"
              onChange={(e) => {
                setusername(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            Email
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Email"
              placeholder="Email"
              onChange={(e) => {
                setemail(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextPassword">
          <Form.Label column sm="2">
            Password
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="password"
              placeholder="Password"
              onChange={(e) => {
                setpassword(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Button
          variant="primary"
          type="submit"
          onClick={() => {
            fetch("http://127.0.0.1:8000/oneuser/rest-auth/login/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                username: username,
                email: email,
                password: password,
              }),
            })
              .then((response) => response.json())
              .then((response) => {
                if (response.token) {
                  localStorage.setItem("wtw-token", response.token);
                  history.push("/");
                }
              });
          }}
        >
          Submit
        </Button>
      </Form>
    </div>
  );
}

export default Login;
