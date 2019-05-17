import React from 'react'
import {Link} from 'react-router-dom';

function Links (props) {
    return (
        <div className="navbar">
            <ul>
                <li><a><Link to = '/'><strong>Baseball</strong></Link></a></li>
                <li><a><Link to = '/'>My Portfolio</Link></a></li>
                <li><a><Link to = '/'>link 1</Link></a></li>
                <li><a><Link to = '/'>link 2</Link></a></li>
            </ul>
        </div>
    )
}

export default Links;