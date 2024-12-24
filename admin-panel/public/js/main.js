let currentDate = dayjs();
let selectedDate = null;

// Initialize the calendar
function initCalendar() {
    updateMonthDisplay();
    renderCalendar();
    loadAppointments();
}

// Update the month display
function updateMonthDisplay() {
    document.getElementById('currentMonth').textContent = 
        currentDate.format('MMMM YYYY');
}

// Render the calendar
function renderCalendar() {
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = '';

    // Add day headers
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    days.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'calendar-day header';
        dayHeader.textContent = day;
        calendar.appendChild(dayHeader);
    });

    // Get start of month
    const startOfMonth = currentDate.startOf('month');
    const daysInMonth = currentDate.daysInMonth();
    const startDay = startOfMonth.day();

    // Add empty days
    for (let i = 0; i < startDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendar.appendChild(emptyDay);
    }

    // Add month days
    for (let i = 1; i <= daysInMonth; i++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        dayElement.textContent = i;
        
        const dateString = currentDate.date(i).format('YYYY-MM-DD');
        dayElement.onclick = () => selectDate(dateString);
        
        calendar.appendChild(dayElement);
    }
}

// Load appointments for selected date
async function loadAppointments(date) {
    const appointmentsList = document.getElementById('appointmentsList');
    appointmentsList.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`/api/appointments/${date || ''}`);
        const appointments = await response.json();

        appointmentsList.innerHTML = appointments.length ? 
            appointments.map(appointment => `
                <div class="appointment-card">
                    <p><strong>Time:</strong> ${appointment.time_slot}</p>
                    <p><strong>Service:</strong> ${appointment.service_id}</p>
                    <p><strong>Customer:</strong> ${appointment.user_name}</p>
                    <p><strong>Price:</strong> ₹${appointment.price}</p>
                </div>
            `).join('') :
            '<p>No appointments for this date</p>';
    } catch (error) {
        appointmentsList.innerHTML = '<p>Error loading appointments</p>';
        console.error('Error:', error);
    }
}

// Handle date selection
function selectDate(dateString) {
    selectedDate = dateString;
    document.querySelectorAll('.calendar-day').forEach(day => {
        day.classList.remove('selected');
    });
    event.target.classList.add('selected');
    loadAppointments(dateString);
}

// Navigation functions
function previousMonth() {
    currentDate = currentDate.subtract(1, 'month');
    updateMonthDisplay();
    renderCalendar();
}

function nextMonth() {
    currentDate = currentDate.add(1, 'month');
    updateMonthDisplay();
    renderCalendar();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initCalendar); 