import React, { useState, useContext } from "react";
import { Form, Col, Button, Row } from "react-bootstrap";
import "./Login.css";
import { useHistory, useParams } from "react-router-dom";

// # body - keywords : ['a', 'b', 'c']

function UserKeyword(props) {
  const [keywords, setkeywords] = useState("");
  let token = localStorage.getItem("wtw-token") || "";

  return (
    <div className="logincontain">
      <Form>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="2">
            키워드 입력
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="Name"
              placeholder="키워드"
              onChange={(e) => {
                let arr = e.target.value;
                let stringToArray = arr.split(",");
                setkeywords(stringToArray);
              }}
            />
          </Col>
        </Form.Group>
        <br></br>
        <Button
          variant="primary"
          type="submit"
          onClick={() => {
            fetch("http://127.0.0.1:8000/oneuser/keyword", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: "jwt " + token,
              },
              body: JSON.stringify({
                keywords: keywords,
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
      </Form>
    </div>
  );
}

export default UserKeyword;
