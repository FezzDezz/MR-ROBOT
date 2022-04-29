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

	@property
	def ToString(self):
		text  = '<code>     фото</code><b>:</b> <i>{}</i>\n'.format("❌" if self.photos_id is None else '✅')
		text += '<code>  локація</code><b>:</b> <i>{}</i>\n'.format("❌" if self.location is None else f'{self.location[0]},{self.location[1]}')
		text += '<code>    товар</code><b>:</b> <i>{}</i>\n'.format("❌" if self.product is None else self.product)
		text += '<code>кількість</code><b>:</b> <i>{}</i>\n'.format("❌" if self.amount is None else self.amount)
		text += '<code>      тип</code><b>:</b> <i>{}</i>\n'.format("❌" if self.hide_type is None else self.hide_type)
		text += '<code>колір ізо</code><b>:</b> <i>{}</i>\n'.format("❌" if self.iso_color is None else f'{self.iso_color[0]} {self.iso_color[1]}')
		text += '<code>    район</code><b>:</b> <i>{}</i>\n'.format("❌" if self.district is None else self.district)
		return text

	pass
