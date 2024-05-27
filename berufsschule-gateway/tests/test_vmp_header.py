from unittest import TestCase, main

class TestVmpHeader(TestCase):
	 def test_initialize(self) -> None:
	 	frame = \
	 		b'VMP\x00E}bB\x06\x01vA11\x00\xdc\xc8\xf5e6\xf0\x9f!\x9c\xdb\x07@)\x15i?\xff\xff\xff\xff\xff\xff\xff\xff
	 		\xff\xff\xff\xff' \
	 		b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x98`-B\xff\xff\xff\xff\x00\x00\x00\x00
	 		\x00\x00\x00\x00' \
	 		b'\x00\x00\x00'
	
	 	vmp_header = VmpHeader()
	 	vmp_header.from_frame(frame, 2)
	
	 	self.assertTrue(vmp_header.is_vmp_header)
	 	self.assertEqual('E', vmp_header.variant)
	 	self.assertEqual(105013885, vmp_header.device_id)
	 	self.assertEqual(Channel('vA11', 1), vmp_header.channel)
	 	self.assertEqual(1710606556, vmp_header.seconds)
	 	self.assertEqual([2.12277889251709, 0.9104791283607483], vmp_header.columns_values)
	
	 def test_not_vmp_header(self) -> None:
	 	vmp_header = VmpHeader()
	 	vmp_header.from_frame(b'\x18\n>\xb3Y\xcb\xe6\xb9{\xed', 5)
	
	 	self.assertFalse(vmp_header.is_vmp_header)
	
	 def test_nan_values(self) -> None:
	 	frame = \
	 		b'VMP\x00E}bB\x06\x01vA11\x00\xdc\xc8\xf5e6\xf0\x9f!\x9c\xdb\x07@)\x15i?\xff\xff\xff\xff\xff\xff\xff\xff
	 		\xff\xff\xff\xff' \
	 		b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x98`-B\xff\xff\xff\xff\x00\x00\x00\x00
	 		\x00\x00\x00\x00' \
	 		b'\x00\x00\x00'
	
	 	vmp_header = VmpHeader()
	 	vmp_header.from_frame(frame, 5)
	
	 	self.assertEqual([2.12277889251709, 0.9104791283607483], vmp_header.columns_values[:2])
	
	 	for value in vmp_header.columns_values[3:]:
	 		self.assertTrue(isnan(value))

if __name__ == '__main__':
	main()