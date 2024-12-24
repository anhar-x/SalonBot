const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const port = 3000;

// Connect to the same SQLite database
const db = new sqlite3.Database('../salon_bookings.db', (err) => {
    if (err) {
        console.error('Error connecting to database:', err);
    } else {
        console.log('Connected to database');
    }
});

// Serve static files
app.use(express.static('public'));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// API endpoint to get appointments by date
app.get('/api/appointments/:date', (req, res) => {
    const date = req.params.date;
    const query = `
        SELECT 
            appointments.*,
            datetime(appointments.date) as appointment_date
        FROM appointments 
        WHERE date(appointment_date) = date(?)
        ORDER BY time_slot
    `;
    
    db.all(query, [date], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// API endpoint to get all appointments
app.get('/api/appointments', (req, res) => {
    const query = `
        SELECT 
            appointments.*,
            datetime(appointments.date) as appointment_date
        FROM appointments 
        ORDER BY date, time_slot
    `;
    
    db.all(query, [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

app.listen(port, () => {
    console.log(`Admin panel running at http://localhost:${port}`);
}); 