import React, { Component } from "react";
//import "../node_modules/bootstrap/dist/css/bootstrap.min.css";

class ScControlInputs extends Component {
  state = {};
  render() {
    return (
      <div>
        <form action="">
          <div className="row">
            <div className="form-group col">
              <label for="dimensions">Dimensions </label>
              <input
                type="text"
                id="dimensions"
                className="dim form-control"
              ></input>
            </div>
            <div className="form-group col">
              <label>Frames </label>
              <input
                type="text"
                id="hello"
                className="frame form-control"
              ></input>
            </div>
            <div className="form-group col">
              <label>Hex code </label>
              <input
                type="text"
                id=""
                className="bitarray form-control"
              ></input>
            </div>
          </div>
        </form>
        <div className="form-group row">
          <button type="button">Enter</button>
        </div>
      </div>
    );
  }
}

export default ScControlInputs;
