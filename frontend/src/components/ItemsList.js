// src/components/ItemsList.js
import React, { useEffect, useState } from 'react';

function ItemsList() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetch('http://localhost:3000/items')
            .then((response) => response.json())
            .then((data) => {
                setItems(data);
            })
            .catch((error) => {
                console.error('Error fetching items:', error);
            });
    }, []);

    return (
        <div>
            <h1>Items</h1>
            {items.length === 0 ? (
                <p>No items found.</p>
            ) : (
                <ul>
                    {items.map((item) => (
                        <li key={item.ItemID}>
                            <strong>{item.Name}</strong> ({item.Rarity})
                            <p>{item.Description}</p>
                            {item.ImageURL && <img src={item.ImageURL} alt={item.Name} width="100" />}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default ItemsList;
