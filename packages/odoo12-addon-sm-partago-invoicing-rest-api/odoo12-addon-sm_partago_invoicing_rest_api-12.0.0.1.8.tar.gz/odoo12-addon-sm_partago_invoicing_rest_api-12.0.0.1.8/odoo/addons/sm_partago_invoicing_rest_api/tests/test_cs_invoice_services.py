from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError
from odoo.addons.sm_partago_invoicing_rest_api.services.cs_invoice_services import CsInvoiceService

@tagged('post_install', 'sm_partago_invoicing_rest_api')
class TestCsInvoiceServices(TransactionCase):

    def setUp(self):
        super(TestCsInvoiceServices, self).setUp()
        self.invoice_service = CsInvoiceService(self)
        
        # Common Variables
        self.ref = 'T/123456789A'
        self.cs_person_index = self.invoice_service._filter_reference(self.ref)
        self.email = 'newtest@example.com'
        self.customer = {
            'name': 'Test Partner',
            'email': self.email,
            'reference': self.ref,
            'country': 'ES'
        }

        # Deleting all cs_person_index and emails before starting the tests (it will be restored once finished on rollback)
        self.env['res.partner'].search([('cs_person_index', '=', self.cs_person_index)]).unlink()
        self.env['res.partner'].search([('email', '=', self.email)]).unlink()
    
    def test_find_or_create_partner(self):
        """ Test finding existing partner based on cs_person_index """
        
        # create a new partner with cs_person_index
        partner = self.env['res.partner'].create({'name': 'Test Partner', 'cs_person_index': self.cs_person_index})
        
        found_partner = self.invoice_service._find_or_create_partner(customer=self.customer)
        
        # assert that the found partner is equal to the created one
        self.assertEqual(found_partner, partner)

    def test_find_or_create_partner_by_email(self):
        """ Test finding existing partner based on email """
        
        # create a new partner with email
        partner = self.env['res.partner'].create({'name': 'Test Partner', 'email': self.email})
        
        found_partner = self.invoice_service._find_or_create_partner(customer=self.customer)
        
        # assert that the found partner is equal to the created one
        self.assertEqual(found_partner, partner)

    def test_create_new_partner(self):
        """ Test creating a new partner """
        
        found_partner = self.invoice_service._find_or_create_partner(customer=self.customer)
        
        # assert that the partner was created correctly
        self.assertEqual(found_partner.name, self.customer['name'])
        self.assertEqual(found_partner.email, self.customer['email'])
        self.assertEqual(found_partner.cs_person_index, self.invoice_service._filter_reference(self.customer['reference']))
        self.assertEqual(found_partner.country_id.code, self.customer['country'])
        
    def test_create_new_partner_with_same_reference(self):
        """ Test creating a new partner with same email as other 2 existing email """
        
        # create a new partner with same email

        ref_test = 'T/999999999Z'
        
        self.env['res.partner'].create({'name': 'Test Partner  ', 'email': self.email, 'cs_person_index': self.cs_person_index})
        self.env['res.partner'].create({'name': 'Test Partner 2', 'email': self.email, 'cs_person_index': self.cs_person_index})
        
        #new customer, different index but same email
        new_customer = {
            'name': 'New Test Partner',
            'email': self.email,
            'reference': ref_test,
            'country': 'ES'
        }
        
        # this should raise an error because the email already exists
        with self.assertRaises(ValidationError):
            self.invoice_service._find_or_create_partner(customer=new_customer)
