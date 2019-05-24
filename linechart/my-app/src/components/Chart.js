import React, {Component} from "react"
import {XYPlot, XAxis, YAxis, VerticalGridLines, HorizontalGridLines, LineSeries
    } from 'react-vis';
// import dateFormat from 'dateformat'

const API_URL = "http://localhost:5000/api/dataset";

class Chart extends Component{

    state = {
        dataset : []
    }

    componentDidMount() {
        fetch(API_URL)
        // Bringing JSON data into a variable
        .then(blob => blob.json()).then(json => {
            let baseball_api = json
            console.log(baseball_api)
    
        let x = baseball_api.map((element, i) => { 
            return element.Date})
        console.log("Date:", x)

        let y = baseball_api.map((element, i) => {
            return element.Portfolio_Value})
        console.log("Portfolio Value:", y)

        const dataset = x.map((x, i) => 
            ({x: new Date(x), y: y[i]}));

        console.log("this is the new dict", this.state.dataset)
        this.setState({dataset: dataset})
        console.log("LORD HAVE MERCY ON MY SOUL",this.state.dataset)

            }
        )
    }

    render () {
        return (
            <div>   
            <XYPlot
                xType='time'
                height={750}
                width={2000}
                >
                <VerticalGridLines />
                <HorizontalGridLines />
                <XAxis />
                <YAxis />
                <LineSeries
                    style = {
                        {color : "blue",
                        fill : "none"}
                    }
                    data={this.state.dataset}/>
            </XYPlot>
            </div>
        );
    }
}


export default Chart;

