let currentDate = dayjs();
let selectedDate = null;
let datesWithAppointments = [];

// Add this function to fetch dates with appointments
async function fetchAppointmentDates() {
    try {
        const yearMonth = currentDate.format('YYYY-MM');
        const response = await fetch(`/api/appointments/dates/${yearMonth}`);
        datesWithAppointments = await response.json();
    } catch (error) {
        console.error('Error fetching appointment dates:', error);
        datesWithAppointments = [];
    }
}

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
async function renderCalendar() {
    // Fetch dates with appointments first
    await fetchAppointmentDates();
    
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
        
        // Create the date string in YYYY-MM-DD format
        const dateString = currentDate.date(i).format('YYYY-MM-DD');
        
        // Check if this date has appointments
        if (datesWithAppointments.includes(dateString)) {
            dayElement.classList.add('has-appointments');
            
            // Add appointment indicator dot
            const dot = document.createElement('div');
            dot.className = 'appointment-dot';
            dayElement.appendChild(dot);
        }

        // Create the date number element
        const dateNumber = document.createElement('span');
        dateNumber.textContent = i;
        dayElement.appendChild(dateNumber);
        
        if (selectedDate === dateString) {
            dayElement.classList.add('selected');
        }
        
        dayElement.onclick = () => selectDate(dateString, dayElement);
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

        if (appointments.length) {
            appointmentsList.innerHTML = appointments
                .map(appointment => `
                    <div class="appointment-card">
                        <p class="time">🕒 ${appointment.time_slot}</p>
                        <p><strong>Service:</strong> ${getServiceEmoji(appointment.service_id)} ${appointment.service_id}</p>
                        <p><strong>Customer:</strong> 👤 ${appointment.user_name}</p>
                        <p class="price"><strong>Price:</strong> ₹${appointment.price}</p>
                    </div>
                `).join('');
        } else {
            appointmentsList.innerHTML = `
                <div class="appointment-card">
                    <p style="text-align: center; color: var(--text-secondary);">
                        No appointments scheduled for this date
                    </p>
                </div>
            `;
        }
    } catch (error) {
        appointmentsList.innerHTML = `
            <div class="appointment-card">
                <p style="text-align: center; color: #ef4444;">
                    Error loading appointments. Please try again.
                </p>
            </div>
        `;
        console.error('Error:', error);
    }
}

// Helper function to get emoji for service
function getServiceEmoji(serviceId) {
    const emojis = {
        'haircut': '💇',
        'coloring': '🎨',
        'smoothening': '✨'
    };
    return emojis[serviceId] || '💅';
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
async function previousMonth() {
    currentDate = currentDate.subtract(1, 'month');
    updateMonthDisplay();
    await renderCalendar();
}

async function nextMonth() {
    currentDate = currentDate.add(1, 'month');
    updateMonthDisplay();
    await renderCalendar();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    updateMonthDisplay();
    renderCalendar();
}); 