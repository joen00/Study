import React, { useState, useEffect, useContext } from "react";
import { Form, Col, Button, Row, ToggleButton } from "react-bootstrap";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import "./Login.css";
import { useHistory, useParams } from "react-router-dom";

import axios from "axios";

function Signup(props) {
  const [username, setusername] = React.useState("");
  const [email, setemail] = React.useState("");
  const [password1, setpassword1] = React.useState("");
  const [password2, setpassword2] = React.useState("");
  const [user_goal, setuser_goal] = React.useState("");
  let history = useHistory();
  return (
    <div className="logincontain">
      <Form>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            Name
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="Name"
              onChange={(e) => {
                setusername(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            ID
          </Form.Label>
          <Col sm="10">
            <Form.Control type="ID" placeholder="ID" />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            Email
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="email"
              placeholder="Email"
              onChange={(e) => {
                setemail(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextPassword">
          <Form.Label column sm="2">
            Password1
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="password"
              placeholder="Password1"
              onChange={(e) => {
                setpassword1(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextPassword">
          <Form.Label column sm="2">
            Password2
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="password"
              placeholder="Password2"
              onChange={(e) => {
                setpassword2(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="2">
            ??????
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="??????"
              onChange={(e) => {
                setuser_goal(e.target.value);
              }}
            />
          </Col>
        </Form.Group>
        {/* ??????????????? ??????????????????
        <div className="checkhere">
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="?????????" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="??????" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="??????" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="??????" />
          </Form.Group>
        </div> */}
        <br></br>
        <br></br>
        <Form.Group className="mb-3">
          <Form.Check
            required
            label="Agree to terms and conditions"
            feedback="You must agree before submitting."
            feedbackType="invalid"
          />
        </Form.Group>
        <Button
          variant="primary"
          type="submit"
          onClick={() => {
            axios({
              method: "post",
              url: "/oneuser/rest-auth/registration",
              data: {
                username: username,
                email: email,
                password1: password1,
                password2: password2,
                user_goal: user_goal,
              },
            })
              .then((res) => {
                history.push("/");
                window.alert("???????????? ??????");
              })
              .catch((error) => {
                console.log(error);
              });
          }}
        >
          Submit
        </Button>
      </Form>
    </div>
  );
}

export default Signup;
