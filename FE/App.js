import React from 'react';
import './App.css';
const axios = require("axios");


  class App extends React.Component {
    constructor(props) {
		super(props);
		this.state ={
			file: null,
			results: []
		};
		this.onFormSubmit = this.onSubmit.bind(this);
		this.onChange = this.onChange.bind(this);
    }
    
    onSubmit= async(e)=> {
		e.preventDefault();
		console.log(this.state.results)
		const formData = new FormData();
		formData.append('img',this.state.file);
		const config = {
			headers: {'content-type': 'multipart/form-data'}
		};
		await axios.post("http://127.0.0.1:5000/api/searchImg",formData,config)
			.then((res) => this.setState({ results: res.data["results"] }))
			.catch((error) => {console.log(error)});
    }

    onChange = async (e) => {        
        axios.delete("http://127.0.0.1:5000/api/clean")
        this.setState({fileprev: URL.createObjectURL(e.target.files[0])});
        this.setState({file: e.target.files[0]});
      }
    
    render() {
      return (
        <div>
			<div className="upload">
				<label>upload image</label>
				<input type="file" onChange={this.onChange}></input>
            	<img src={this.state.fileprev}/>
          	</div>
          	<button className="submitButton" onClick={this.onSubmit}>
				  upload
			</button>
          
          	<div className="results">
            	{this.state.results.map((i) => {return <img src={i}></img>;})}
          	</div>
        </div>
      	);
    	}
	  }
	  
export default App;

