import React, { useEffect, useState } from 'react';

function ItemsList() {
    const [items, setItems] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://localhost:3000/items')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch items');
                }
                return response.json();
            })
            .then(data => setItems(data))
            .catch(error => setError(error.message));
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div id="items">
            {items.map((item) => (
                <div key={item.item_id}>
                    <strong>{item.Name}</strong> ({item.Rarity})
                </div>
            ))}
        </div>
    );
}

export default ItemsList;
