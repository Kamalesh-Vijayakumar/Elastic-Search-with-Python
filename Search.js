import React, { useState } from 'react';
import axios from 'axios';

function Search() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const response = await axios.post('http://localhost:5000/search', { query });
            setResults(response.data);  
        } catch (error) {
            console.error('Error during data fetch:', error);
        }
    };

    return (
        <div style={{ marginTop: '20px', marginBottom: '20px' }}>
            <input
                style={{ marginRight: '10px' }}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search..."
            />
            <button style={{ padding: '10px 20px' }} onClick={handleSearch}>Search</button>
            {results.length > 0 && (
                <ul>
                    {results.map((result, index) => (
                        <li key={index}>
                            <strong>Name:</strong> {result._source['Full Name'] || 'No Name Provided'}, 
                            <strong>Job Title:</strong> {result._source['Job Title']},
                            <strong>Department:</strong> {result._source['Department']},
                            <strong>Gender:</strong> {result._source['Gender']},
                            <strong>Age:</strong> {result._source['Age']},
                            <strong>Country:</strong> {result._source['Country']},
                            <strong>City:</strong> {result._source['City']}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Search;
