# Please edit this list and import only required elements
import webnotes

from webnotes.model.doc import Document
from webnotes import session, form, msgprint, errprint

# -----------------------------------------------------------------------------------------

class DocType:
	def __init__(self, doc, doclist=[]):
		self.doc = doc
		self.doclist = doclist

	def autoname(self):
		if self.doc.customer:
			self.doc.name = self.doc.customer + '-' + self.doc.address_type
		elif self.doc.supplier:
			self.doc.name = self.doc.supplier + '-' + self.doc.address_type
		elif self.doc.sales_partner:
			self.doc.name = self.doc.sales_partner + '-' + self.doc.address_type
			
		# filter out bad characters in name
		#self.doc.name = self.doc.name.replace('&','and').replace('.','').replace("'",'').replace('"','').replace(',','').replace('`','')

#----------------------
# Call to Validate
#----------------------
	def validate(self):
		self.validate_primary_address()
		self.validate_shipping_address()

#----------------------
# Validate that there can only be one primary address for particular customer, supplier
#----------------------
	def validate_primary_address(self):
		sql = webnotes.conn.sql
		if self.doc.is_primary_address == 1:
			if self.doc.customer: 
				sql("update tabAddress set is_primary_address=0 where customer = '%s'" % (self.doc.customer))
			elif self.doc.supplier:
				sql("update tabAddress set is_primary_address=0 where supplier = '%s'" % (self.doc.supplier))
			elif self.doc.sales_partner:
				sql("update tabAddress set is_primary_address=0 where sales_partner = '%s'" % (self.doc.sales_partner))
		elif not self.doc.is_shipping_address:
			if self.doc.customer: 
				if not sql("select name from tabAddress where is_primary_address=1 and customer = '%s'" % (self.doc.customer)):
					self.doc.is_primary_address = 1
			elif self.doc.supplier:
				if not sql("select name from tabAddress where is_primary_address=1 and supplier = '%s'" % (self.doc.supplier)):
					self.doc.is_primary_address = 1
			elif self.doc.sales_partner:
				if not sql("select name from tabAddress where is_primary_address=1 and sales_partner = '%s'" % (self.doc.sales_partner)):
					self.doc.is_primary_address = 1

				
#----------------------
# Validate that there can only be one shipping address for particular customer, supplier
#----------------------
	def validate_shipping_address(self):
		sql = webnotes.conn.sql
		if self.doc.is_shipping_address == 1:
			if self.doc.customer: 
				sql("update tabAddress set is_shipping_address=0 where customer = '%s'" % (self.doc.customer))
			elif self.doc.supplier:
				sql("update tabAddress set is_shipping_address=0 where supplier = '%s'" % (self.doc.supplier))			
			elif self.doc.sales_partner:
				sql("update tabAddress set is_shipping_address=0 where sales_partner = '%s'" % (self.doc.sales_partner))			
