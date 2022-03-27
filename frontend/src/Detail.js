import React, { useState, useEffect, useContext } from "react";
import { useHistory, useParams } from "react-router-dom";
import styled from "styled-components";
import { 재고context } from "./App.js";
import { Card, ListGroup, ListGroupItem } from "react-bootstrap";
import { CSSTransition } from "react-transition-group";
import { connect } from "react-redux";
import { FaHeart, FaRegHeart, FaBook } from "react-icons/fa";

function Detail(props) {
  return (
    <div className="container">
      <p className="red">Detail</p>

      <div className="container">
        <재고context.Provider value={props.재고}>
          <div className="row">
            {props.studyroom.map((a, i) => {
              return (
                <Cardcomponent
                  studyroom={props.studyroom[i]}
                  i={i}
                  key={i}
                  like={props.like}
                  likeChange={props.likeChange}
                />
              );
            })}
          </div>
        </재고context.Provider>
      </div>
    </div>
  );
}

function Cardcomponent(props) {
  let 재고 = useContext(재고context);

  return (
    <div className="col-md-3">
      <Card style={{ width: "18rem", margin: "1rem" }}>
        <Card.Img variant="top" src={props.studyroom.studyimg} />
        <Card.Body>
          <Card.Title>
            {props.studyroom.title}&nbsp;
            {props.like ? (
              <FaHeart style={{ color: "red", fontSize: "24px" }} />
            ) : (
              <FaRegHeart style={{ color: "red", fontSize: "24px" }} />
            )}
          </Card.Title>

          <Card.Text>{props.studyroom.context}</Card.Text>
        </Card.Body>
        <ListGroup className="list-group-flush">
          <ListGroupItem>{props.studyroom.week_time}</ListGroupItem>
          <ListGroupItem>{props.studyroom.goal}</ListGroupItem>
          <ListGroupItem>{props.studyroom.price}</ListGroupItem>

          <Test i={props.i}></Test>
        </ListGroup>
        <Card.Body>
          <Card.Link>Card Link</Card.Link>
        </Card.Body>
      </Card>
    </div>
  );
}

function Test(props) {
  let 재고 = useContext(재고context);
  return <p>{재고[props.i]}</p>;
}
export default Detail;
