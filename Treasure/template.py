# -*- coding: utf-8 -*-
from dataclasses import dataclass, asdict, astuple


# noinspection PyTypeChecker
@dataclass
class Template:
	# photos_id: list[str] = field(default=None)
	# location: list[str, float] = field(default=None)
	product: str = None
	amount: str = None
	hide_type: str = None
	iso_color: list[str] = None
	district: str = None
	owner_user: str = None

	def to_dict(self):
		"""
		Returns self as dictionary where `key=dict.key` and `value=dict.value`

		:rtype: dict
		"""
		return asdict(self)

	def to_tuple(self):
		return astuple(self)

	def erase(self):
		self.product = None
		self.amount = None
		self.hide_type = None
		self.iso_color = None
		self.district = None

	def set_random(self):
		self.product = None
		self.amount = None
		self.hide_type = None
		self.iso_color = None
		self.district = None



	@property
	def ToString(self):
		text  = '<code>    товар</code><b>:</b> <i>{}</i>\n'.format("❌" if self.product is None else self.product)
		text += '<code>кількість</code><b>:</b> <i>{}</i>\n'.format("❌" if self.amount is None else self.amount)
		text += '<code>      тип</code><b>:</b> <i>{}</i>\n'.format("❌" if self.hide_type is None else self.hide_type)
		text += '<code>колір ізо</code><b>:</b> <i>{}</i>\n'.format("❌" if self.iso_color is None else self.iso_color[0])
		text += '<code>    район</code><b>:</b> <i>{}</i>\n'.format("❌" if self.district is None else self.district)
		return text

	@property
	def IsSet(self):
		for item in self.to_dict().items():
			if item[0] != 'owner_user' and item[1] is None:
				return  False
		return True

	pass
