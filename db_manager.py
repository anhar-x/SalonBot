from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Appointment

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///salon_bookings.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_appointment(self, user_id, user_name, service_id, date, time_slot, price):
        session = self.Session()
        try:
            appointment = Appointment(
                user_id=user_id,
                user_name=user_name,
                service_id=service_id,
                date=date,
                time_slot=time_slot,
                price=price,
                created_at=datetime.now()
            )
            session.add(appointment)
            session.commit()
            appointment_id = appointment.id
            appointment_data = {
                'id': appointment_id,
                'user_id': appointment.user_id,
                'user_name': appointment.user_name,
                'service_id': appointment.service_id,
                'date': appointment.date,
                'time_slot': appointment.time_slot,
                'price': appointment.price
            }
            return appointment_data
        finally:
            session.close()

    def check_availability(self, date, time_slot):
        session = self.Session()
        try:
            existing = session.query(Appointment).filter(
                Appointment.date == date,
                Appointment.time_slot == time_slot,
                Appointment.status == 'confirmed'
            ).first()
            return existing is None
        finally:
            session.close()

    def get_user_appointments(self, user_id):
        session = self.Session()
        try:
            return session.query(Appointment).filter(
                Appointment.user_id == user_id,
                Appointment.status == 'confirmed'
            ).all()
        finally:
            session.close() 