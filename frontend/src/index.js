import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

import { BrowserRouter } from "react-router-dom";

import { Provider } from "react-redux";
import { combineReducers, createStore } from "redux";

let alert초기값 = true;

function reducer2(state = alert초기값, 액션) {
  if (액션.type === "alert닫기") {
    return false;
  } else {
    return state;
  }
}

let 초기값 = [
  { id: 0, name: "멋진신발", quan: 2 },
  { id: 1, name: "멋진신발1", quan: 7 },
];

// reducer는 항상 state를 뱉어야한다, 수정된 state를 뱉는 함수
function reducer(state = 초기값, 액션) {
  //액션은 dispatch할때 모든 데이터
  if (액션.type === "항목추가") {
    let copy = [...state];
    copy.push(액션.payload);
    return copy;
  } else if (액션.type === "수량증가") {
    // 데이터 수정 방법이다 -> state수정 후 -> 결과값을 뱉기
    let copy = [...state];
    copy[0].quan++;
    return copy;
  } else if (액션.type === "수량감소") {
    let copy = [...state];
    copy[0].quan--;
    return copy;
  } else {
    return state; // 수정이 필요없으면 기본값
  }
}

let store = createStore(combineReducers({ reducer, reducer2 })); //state를 내뱉는다.

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Provider store={store}>
        <App />
      </Provider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
