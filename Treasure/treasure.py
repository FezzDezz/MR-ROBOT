# -*- coding: utf-8 -*-
from dataclasses import dataclass, field, asdict, astuple, replace
from .template import Template

# noinspection PyTypeChecker
@dataclass
class Treasure:
	photos_id: list[str] = None
	location: list[str, float] = None
	product: str = None
	amount: str = None
	hide_type: str = None
	hide_caption: str = None
	iso_color: list[str] = None
	district: str = None

	def to_dict(self):
		return asdict(self)

	def to_tuple(self):
		return astuple(self)

	def apply_template(self, template: Template):
		self.product = template.product
		self.amount = template.amount
		self.hide_type = template.hide_type
		self.iso_color = template.iso_color
		self.district = template.district
		pass

	def erase(self):
		self.photos_id = None
		self.location = None
		self.product = None
		self.hide_type = None
		self.iso_color = None
		self.iso_color = None
		self.district = None


	pass
