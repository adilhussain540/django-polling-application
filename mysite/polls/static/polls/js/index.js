import React from 'react'
import ReactDOM from 'react-dom'


class Welcome extends React.Component {
  render (){
    console.log("hy")
    return (<h1>Hello, {props.name}</h1>)
  }
}

const element = <Welcome name="world" />;
ReactDOM.render(
  element,
  document.getElementById('react')
);
