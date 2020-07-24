from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Address, City, District, Neighborhood, Customer

def sample_user(email='test@emre.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

def sample_address(city='İstanbul', district='Maltepe', neighborhood='Aydınevler', extra_info=""):
    """Create a sample address"""
    city = City.objects.create(name=city)
    district = District.objects.create(city=city, name=district)
    neighborhood = Neighborhood.objects.create(
        district=district,
        name=neighborhood
    )
    extra_info = 'Poyraz sokak No 10-12'
    address = Address.objects.create(
        city=city,
        district=district,
        neighborhood=neighborhood,
        extra_info=extra_info
    )
    return address

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating new user with an email is successful"""
        email = 'test@emre.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        
    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'test@EMRE.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    
    def test_create_address_successful(self):
        """Test creating new address is successful"""
        city = City.objects.create(name='İstanbul')
        district = District.objects.create(city=city, name='Maltepe')
        neighborhood = Neighborhood.objects.create(
            district=district,
            name='Aydınevler'
        )
        extra_info = 'Poyraz sokak No 10-12'
        address = Address.objects.create(
            city=city,
            district=district,
            neighborhood=neighborhood,
            extra_info=extra_info
        )

        self.assertEqual(
            str(address),
            (f"{district} {neighborhood} {extra_info}").upper())

    def test_create_customer_with_address_successful(self):
        """Test creating new customer with an address is successful"""
        customer = Customer.objects.create(
            user=sample_user(),
            address=sample_address(),
            phone1='5331234578',
            phone2='5331239865'
        )
        self.assertEqual(str(customer), customer.user.email)