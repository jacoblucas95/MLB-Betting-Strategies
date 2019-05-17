import React, {Component} from "react";
import Stats from './Stats';

const data = [1,2,3,4,5,6,7];


class StatsTable extends Component {
    render () {
        let rows = data.map((element, i) => {
            return <Stats data={element} key={i} />
          });
        return (
            <div>
                <table className="table">
                    <tr>
                        <th>column 1</th>
                        <th>column 2</th>
                    </tr>
                    <tr>
                        <td>{rows}</td>
                        <td>{rows}</td>
                    </tr>
                </table>
            </div>
        )
    }
}

export default StatsTable;