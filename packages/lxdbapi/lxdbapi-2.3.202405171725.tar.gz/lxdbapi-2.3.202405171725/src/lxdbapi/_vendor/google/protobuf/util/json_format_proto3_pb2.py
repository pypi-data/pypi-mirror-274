# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/util/json_format_proto3.proto
"""Generated protocol buffer code."""
from ....google.protobuf.internal import enum_type_wrapper
from ....google.protobuf import descriptor as _descriptor
from ....google.protobuf import descriptor_pool as _descriptor_pool
from ....google.protobuf import message as _message
from ....google.protobuf import reflection as _reflection
from ....google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ....google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ....google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from ....google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from ....google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from ....google.protobuf import unittest_pb2 as google_dot_protobuf_dot_unittest__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-google/protobuf/util/json_format_proto3.proto\x12\x06proto3\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a google/protobuf/field_mask.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1egoogle/protobuf/unittest.proto\"\x1c\n\x0bMessageType\x12\r\n\x05value\x18\x01 \x01(\x05\"\x94\x05\n\x0bTestMessage\x12\x12\n\nbool_value\x18\x01 \x01(\x08\x12\x13\n\x0bint32_value\x18\x02 \x01(\x05\x12\x13\n\x0bint64_value\x18\x03 \x01(\x03\x12\x14\n\x0cuint32_value\x18\x04 \x01(\r\x12\x14\n\x0cuint64_value\x18\x05 \x01(\x04\x12\x13\n\x0b\x66loat_value\x18\x06 \x01(\x02\x12\x14\n\x0c\x64ouble_value\x18\x07 \x01(\x01\x12\x14\n\x0cstring_value\x18\x08 \x01(\t\x12\x13\n\x0b\x62ytes_value\x18\t \x01(\x0c\x12$\n\nenum_value\x18\n \x01(\x0e\x32\x10.proto3.EnumType\x12*\n\rmessage_value\x18\x0b \x01(\x0b\x32\x13.proto3.MessageType\x12\x1b\n\x13repeated_bool_value\x18\x15 \x03(\x08\x12\x1c\n\x14repeated_int32_value\x18\x16 \x03(\x05\x12\x1c\n\x14repeated_int64_value\x18\x17 \x03(\x03\x12\x1d\n\x15repeated_uint32_value\x18\x18 \x03(\r\x12\x1d\n\x15repeated_uint64_value\x18\x19 \x03(\x04\x12\x1c\n\x14repeated_float_value\x18\x1a \x03(\x02\x12\x1d\n\x15repeated_double_value\x18\x1b \x03(\x01\x12\x1d\n\x15repeated_string_value\x18\x1c \x03(\t\x12\x1c\n\x14repeated_bytes_value\x18\x1d \x03(\x0c\x12-\n\x13repeated_enum_value\x18\x1e \x03(\x0e\x32\x10.proto3.EnumType\x12\x33\n\x16repeated_message_value\x18\x1f \x03(\x0b\x32\x13.proto3.MessageType\"\x8c\x02\n\tTestOneof\x12\x1b\n\x11oneof_int32_value\x18\x01 \x01(\x05H\x00\x12\x1c\n\x12oneof_string_value\x18\x02 \x01(\tH\x00\x12\x1b\n\x11oneof_bytes_value\x18\x03 \x01(\x0cH\x00\x12,\n\x10oneof_enum_value\x18\x04 \x01(\x0e\x32\x10.proto3.EnumTypeH\x00\x12\x32\n\x13oneof_message_value\x18\x05 \x01(\x0b\x32\x13.proto3.MessageTypeH\x00\x12\x36\n\x10oneof_null_value\x18\x06 \x01(\x0e\x32\x1a.google.protobuf.NullValueH\x00\x42\r\n\x0boneof_value\"\xe1\x04\n\x07TestMap\x12.\n\x08\x62ool_map\x18\x01 \x03(\x0b\x32\x1c.proto3.TestMap.BoolMapEntry\x12\x30\n\tint32_map\x18\x02 \x03(\x0b\x32\x1d.proto3.TestMap.Int32MapEntry\x12\x30\n\tint64_map\x18\x03 \x03(\x0b\x32\x1d.proto3.TestMap.Int64MapEntry\x12\x32\n\nuint32_map\x18\x04 \x03(\x0b\x32\x1e.proto3.TestMap.Uint32MapEntry\x12\x32\n\nuint64_map\x18\x05 \x03(\x0b\x32\x1e.proto3.TestMap.Uint64MapEntry\x12\x32\n\nstring_map\x18\x06 \x03(\x0b\x32\x1e.proto3.TestMap.StringMapEntry\x1a.\n\x0c\x42oolMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rInt32MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rInt64MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eUint32MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eUint64MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x04\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eStringMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\x85\x06\n\rTestNestedMap\x12\x34\n\x08\x62ool_map\x18\x01 \x03(\x0b\x32\".proto3.TestNestedMap.BoolMapEntry\x12\x36\n\tint32_map\x18\x02 \x03(\x0b\x32#.proto3.TestNestedMap.Int32MapEntry\x12\x36\n\tint64_map\x18\x03 \x03(\x0b\x32#.proto3.TestNestedMap.Int64MapEntry\x12\x38\n\nuint32_map\x18\x04 \x03(\x0b\x32$.proto3.TestNestedMap.Uint32MapEntry\x12\x38\n\nuint64_map\x18\x05 \x03(\x0b\x32$.proto3.TestNestedMap.Uint64MapEntry\x12\x38\n\nstring_map\x18\x06 \x03(\x0b\x32$.proto3.TestNestedMap.StringMapEntry\x12\x32\n\x07map_map\x18\x07 \x03(\x0b\x32!.proto3.TestNestedMap.MapMapEntry\x1a.\n\x0c\x42oolMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rInt32MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rInt64MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eUint32MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eUint64MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x04\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eStringMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x44\n\x0bMapMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12$\n\x05value\x18\x02 \x01(\x0b\x32\x15.proto3.TestNestedMap:\x02\x38\x01\"{\n\rTestStringMap\x12\x38\n\nstring_map\x18\x01 \x03(\x0b\x32$.proto3.TestStringMap.StringMapEntry\x1a\x30\n\x0eStringMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xee\x07\n\x0bTestWrapper\x12.\n\nbool_value\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x30\n\x0bint32_value\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x30\n\x0bint64_value\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x32\n\x0cuint32_value\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x32\n\x0cuint64_value\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.UInt64Value\x12\x30\n\x0b\x66loat_value\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12\x32\n\x0c\x64ouble_value\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\x0cstring_value\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x30\n\x0b\x62ytes_value\x18\t \x01(\x0b\x32\x1b.google.protobuf.BytesValue\x12\x37\n\x13repeated_bool_value\x18\x0b \x03(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x39\n\x14repeated_int32_value\x18\x0c \x03(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x39\n\x14repeated_int64_value\x18\r \x03(\x0b\x32\x1b.google.protobuf.Int64Value\x12;\n\x15repeated_uint32_value\x18\x0e \x03(\x0b\x32\x1c.google.protobuf.UInt32Value\x12;\n\x15repeated_uint64_value\x18\x0f \x03(\x0b\x32\x1c.google.protobuf.UInt64Value\x12\x39\n\x14repeated_float_value\x18\x10 \x03(\x0b\x32\x1b.google.protobuf.FloatValue\x12;\n\x15repeated_double_value\x18\x11 \x03(\x0b\x32\x1c.google.protobuf.DoubleValue\x12;\n\x15repeated_string_value\x18\x12 \x03(\x0b\x32\x1c.google.protobuf.StringValue\x12\x39\n\x14repeated_bytes_value\x18\x13 \x03(\x0b\x32\x1b.google.protobuf.BytesValue\"n\n\rTestTimestamp\x12)\n\x05value\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0erepeated_value\x18\x02 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\"k\n\x0cTestDuration\x12(\n\x05value\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x31\n\x0erepeated_value\x18\x02 \x03(\x0b\x32\x19.google.protobuf.Duration\":\n\rTestFieldMask\x12)\n\x05value\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"e\n\nTestStruct\x12&\n\x05value\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12/\n\x0erepeated_value\x18\x02 \x03(\x0b\x32\x17.google.protobuf.Struct\"\\\n\x07TestAny\x12#\n\x05value\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\x12,\n\x0erepeated_value\x18\x02 \x03(\x0b\x32\x14.google.protobuf.Any\"b\n\tTestValue\x12%\n\x05value\x18\x01 \x01(\x0b\x32\x16.google.protobuf.Value\x12.\n\x0erepeated_value\x18\x02 \x03(\x0b\x32\x16.google.protobuf.Value\"n\n\rTestListValue\x12)\n\x05value\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x32\n\x0erepeated_value\x18\x02 \x03(\x0b\x32\x1a.google.protobuf.ListValue\"\x89\x01\n\rTestBoolValue\x12\x12\n\nbool_value\x18\x01 \x01(\x08\x12\x34\n\x08\x62ool_map\x18\x02 \x03(\x0b\x32\".proto3.TestBoolValue.BoolMapEntry\x1a.\n\x0c\x42oolMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"+\n\x12TestCustomJsonName\x12\x15\n\x05value\x18\x01 \x01(\x05R\x06@value\"J\n\x0eTestExtensions\x12\x38\n\nextensions\x18\x01 \x01(\x0b\x32$.protobuf_unittest.TestAllExtensions\"\x84\x01\n\rTestEnumValue\x12%\n\x0b\x65num_value1\x18\x01 \x01(\x0e\x32\x10.proto3.EnumType\x12%\n\x0b\x65num_value2\x18\x02 \x01(\x0e\x32\x10.proto3.EnumType\x12%\n\x0b\x65num_value3\x18\x03 \x01(\x0e\x32\x10.proto3.EnumType*\x1c\n\x08\x45numType\x12\x07\n\x03\x46OO\x10\x00\x12\x07\n\x03\x42\x41R\x10\x01\x42,\n\x18\x63om.google.protobuf.utilB\x10JsonFormatProto3b\x06proto3')

_ENUMTYPE = DESCRIPTOR.enum_types_by_name['EnumType']
EnumType = enum_type_wrapper.EnumTypeWrapper(_ENUMTYPE)
FOO = 0
BAR = 1


_MESSAGETYPE = DESCRIPTOR.message_types_by_name['MessageType']
_TESTMESSAGE = DESCRIPTOR.message_types_by_name['TestMessage']
_TESTONEOF = DESCRIPTOR.message_types_by_name['TestOneof']
_TESTMAP = DESCRIPTOR.message_types_by_name['TestMap']
_TESTMAP_BOOLMAPENTRY = _TESTMAP.nested_types_by_name['BoolMapEntry']
_TESTMAP_INT32MAPENTRY = _TESTMAP.nested_types_by_name['Int32MapEntry']
_TESTMAP_INT64MAPENTRY = _TESTMAP.nested_types_by_name['Int64MapEntry']
_TESTMAP_UINT32MAPENTRY = _TESTMAP.nested_types_by_name['Uint32MapEntry']
_TESTMAP_UINT64MAPENTRY = _TESTMAP.nested_types_by_name['Uint64MapEntry']
_TESTMAP_STRINGMAPENTRY = _TESTMAP.nested_types_by_name['StringMapEntry']
_TESTNESTEDMAP = DESCRIPTOR.message_types_by_name['TestNestedMap']
_TESTNESTEDMAP_BOOLMAPENTRY = _TESTNESTEDMAP.nested_types_by_name['BoolMapEntry']
_TESTNESTEDMAP_INT32MAPENTRY = _TESTNESTEDMAP.nested_types_by_name['Int32MapEntry']
_TESTNESTEDMAP_INT64MAPENTRY = _TESTNESTEDMAP.nested_types_by_name['Int64MapEntry']
_TESTNESTEDMAP_UINT32MAPENTRY = _TESTNESTEDMAP.nested_types_by_name['Uint32MapEntry']
_TESTNESTEDMAP_UINT64MAPENTRY = _TESTNESTEDMAP.nested_types_by_name['Uint64MapEntry']
_TESTNESTEDMAP_STRINGMAPENTRY = _TESTNESTEDMAP.nested_types_by_name['StringMapEntry']
_TESTNESTEDMAP_MAPMAPENTRY = _TESTNESTEDMAP.nested_types_by_name['MapMapEntry']
_TESTSTRINGMAP = DESCRIPTOR.message_types_by_name['TestStringMap']
_TESTSTRINGMAP_STRINGMAPENTRY = _TESTSTRINGMAP.nested_types_by_name['StringMapEntry']
_TESTWRAPPER = DESCRIPTOR.message_types_by_name['TestWrapper']
_TESTTIMESTAMP = DESCRIPTOR.message_types_by_name['TestTimestamp']
_TESTDURATION = DESCRIPTOR.message_types_by_name['TestDuration']
_TESTFIELDMASK = DESCRIPTOR.message_types_by_name['TestFieldMask']
_TESTSTRUCT = DESCRIPTOR.message_types_by_name['TestStruct']
_TESTANY = DESCRIPTOR.message_types_by_name['TestAny']
_TESTVALUE = DESCRIPTOR.message_types_by_name['TestValue']
_TESTLISTVALUE = DESCRIPTOR.message_types_by_name['TestListValue']
_TESTBOOLVALUE = DESCRIPTOR.message_types_by_name['TestBoolValue']
_TESTBOOLVALUE_BOOLMAPENTRY = _TESTBOOLVALUE.nested_types_by_name['BoolMapEntry']
_TESTCUSTOMJSONNAME = DESCRIPTOR.message_types_by_name['TestCustomJsonName']
_TESTEXTENSIONS = DESCRIPTOR.message_types_by_name['TestExtensions']
_TESTENUMVALUE = DESCRIPTOR.message_types_by_name['TestEnumValue']
MessageType = _reflection.GeneratedProtocolMessageType('MessageType', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGETYPE,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.MessageType)
  })
_sym_db.RegisterMessage(MessageType)

TestMessage = _reflection.GeneratedProtocolMessageType('TestMessage', (_message.Message,), {
  'DESCRIPTOR' : _TESTMESSAGE,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestMessage)
  })
_sym_db.RegisterMessage(TestMessage)

TestOneof = _reflection.GeneratedProtocolMessageType('TestOneof', (_message.Message,), {
  'DESCRIPTOR' : _TESTONEOF,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestOneof)
  })
_sym_db.RegisterMessage(TestOneof)

TestMap = _reflection.GeneratedProtocolMessageType('TestMap', (_message.Message,), {

  'BoolMapEntry' : _reflection.GeneratedProtocolMessageType('BoolMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMAP_BOOLMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestMap.BoolMapEntry)
    })
  ,

  'Int32MapEntry' : _reflection.GeneratedProtocolMessageType('Int32MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMAP_INT32MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestMap.Int32MapEntry)
    })
  ,

  'Int64MapEntry' : _reflection.GeneratedProtocolMessageType('Int64MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMAP_INT64MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestMap.Int64MapEntry)
    })
  ,

  'Uint32MapEntry' : _reflection.GeneratedProtocolMessageType('Uint32MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMAP_UINT32MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestMap.Uint32MapEntry)
    })
  ,

  'Uint64MapEntry' : _reflection.GeneratedProtocolMessageType('Uint64MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMAP_UINT64MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestMap.Uint64MapEntry)
    })
  ,

  'StringMapEntry' : _reflection.GeneratedProtocolMessageType('StringMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMAP_STRINGMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestMap.StringMapEntry)
    })
  ,
  'DESCRIPTOR' : _TESTMAP,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestMap)
  })
_sym_db.RegisterMessage(TestMap)
_sym_db.RegisterMessage(TestMap.BoolMapEntry)
_sym_db.RegisterMessage(TestMap.Int32MapEntry)
_sym_db.RegisterMessage(TestMap.Int64MapEntry)
_sym_db.RegisterMessage(TestMap.Uint32MapEntry)
_sym_db.RegisterMessage(TestMap.Uint64MapEntry)
_sym_db.RegisterMessage(TestMap.StringMapEntry)

TestNestedMap = _reflection.GeneratedProtocolMessageType('TestNestedMap', (_message.Message,), {

  'BoolMapEntry' : _reflection.GeneratedProtocolMessageType('BoolMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_BOOLMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.BoolMapEntry)
    })
  ,

  'Int32MapEntry' : _reflection.GeneratedProtocolMessageType('Int32MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_INT32MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.Int32MapEntry)
    })
  ,

  'Int64MapEntry' : _reflection.GeneratedProtocolMessageType('Int64MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_INT64MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.Int64MapEntry)
    })
  ,

  'Uint32MapEntry' : _reflection.GeneratedProtocolMessageType('Uint32MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_UINT32MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.Uint32MapEntry)
    })
  ,

  'Uint64MapEntry' : _reflection.GeneratedProtocolMessageType('Uint64MapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_UINT64MAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.Uint64MapEntry)
    })
  ,

  'StringMapEntry' : _reflection.GeneratedProtocolMessageType('StringMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_STRINGMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.StringMapEntry)
    })
  ,

  'MapMapEntry' : _reflection.GeneratedProtocolMessageType('MapMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTNESTEDMAP_MAPMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestNestedMap.MapMapEntry)
    })
  ,
  'DESCRIPTOR' : _TESTNESTEDMAP,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestNestedMap)
  })
_sym_db.RegisterMessage(TestNestedMap)
_sym_db.RegisterMessage(TestNestedMap.BoolMapEntry)
_sym_db.RegisterMessage(TestNestedMap.Int32MapEntry)
_sym_db.RegisterMessage(TestNestedMap.Int64MapEntry)
_sym_db.RegisterMessage(TestNestedMap.Uint32MapEntry)
_sym_db.RegisterMessage(TestNestedMap.Uint64MapEntry)
_sym_db.RegisterMessage(TestNestedMap.StringMapEntry)
_sym_db.RegisterMessage(TestNestedMap.MapMapEntry)

TestStringMap = _reflection.GeneratedProtocolMessageType('TestStringMap', (_message.Message,), {

  'StringMapEntry' : _reflection.GeneratedProtocolMessageType('StringMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTSTRINGMAP_STRINGMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestStringMap.StringMapEntry)
    })
  ,
  'DESCRIPTOR' : _TESTSTRINGMAP,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestStringMap)
  })
_sym_db.RegisterMessage(TestStringMap)
_sym_db.RegisterMessage(TestStringMap.StringMapEntry)

TestWrapper = _reflection.GeneratedProtocolMessageType('TestWrapper', (_message.Message,), {
  'DESCRIPTOR' : _TESTWRAPPER,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestWrapper)
  })
_sym_db.RegisterMessage(TestWrapper)

TestTimestamp = _reflection.GeneratedProtocolMessageType('TestTimestamp', (_message.Message,), {
  'DESCRIPTOR' : _TESTTIMESTAMP,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestTimestamp)
  })
_sym_db.RegisterMessage(TestTimestamp)

TestDuration = _reflection.GeneratedProtocolMessageType('TestDuration', (_message.Message,), {
  'DESCRIPTOR' : _TESTDURATION,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestDuration)
  })
_sym_db.RegisterMessage(TestDuration)

TestFieldMask = _reflection.GeneratedProtocolMessageType('TestFieldMask', (_message.Message,), {
  'DESCRIPTOR' : _TESTFIELDMASK,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestFieldMask)
  })
_sym_db.RegisterMessage(TestFieldMask)

TestStruct = _reflection.GeneratedProtocolMessageType('TestStruct', (_message.Message,), {
  'DESCRIPTOR' : _TESTSTRUCT,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestStruct)
  })
_sym_db.RegisterMessage(TestStruct)

TestAny = _reflection.GeneratedProtocolMessageType('TestAny', (_message.Message,), {
  'DESCRIPTOR' : _TESTANY,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestAny)
  })
_sym_db.RegisterMessage(TestAny)

TestValue = _reflection.GeneratedProtocolMessageType('TestValue', (_message.Message,), {
  'DESCRIPTOR' : _TESTVALUE,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestValue)
  })
_sym_db.RegisterMessage(TestValue)

TestListValue = _reflection.GeneratedProtocolMessageType('TestListValue', (_message.Message,), {
  'DESCRIPTOR' : _TESTLISTVALUE,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestListValue)
  })
_sym_db.RegisterMessage(TestListValue)

TestBoolValue = _reflection.GeneratedProtocolMessageType('TestBoolValue', (_message.Message,), {

  'BoolMapEntry' : _reflection.GeneratedProtocolMessageType('BoolMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTBOOLVALUE_BOOLMAPENTRY,
    '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
    # @@protoc_insertion_point(class_scope:proto3.TestBoolValue.BoolMapEntry)
    })
  ,
  'DESCRIPTOR' : _TESTBOOLVALUE,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestBoolValue)
  })
_sym_db.RegisterMessage(TestBoolValue)
_sym_db.RegisterMessage(TestBoolValue.BoolMapEntry)

TestCustomJsonName = _reflection.GeneratedProtocolMessageType('TestCustomJsonName', (_message.Message,), {
  'DESCRIPTOR' : _TESTCUSTOMJSONNAME,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestCustomJsonName)
  })
_sym_db.RegisterMessage(TestCustomJsonName)

TestExtensions = _reflection.GeneratedProtocolMessageType('TestExtensions', (_message.Message,), {
  'DESCRIPTOR' : _TESTEXTENSIONS,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestExtensions)
  })
_sym_db.RegisterMessage(TestExtensions)

TestEnumValue = _reflection.GeneratedProtocolMessageType('TestEnumValue', (_message.Message,), {
  'DESCRIPTOR' : _TESTENUMVALUE,
  '__module__' : 'google.protobuf.util.json_format_proto3_pb2'
  # @@protoc_insertion_point(class_scope:proto3.TestEnumValue)
  })
_sym_db.RegisterMessage(TestEnumValue)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030com.google.protobuf.utilB\020JsonFormatProto3'
  _TESTMAP_BOOLMAPENTRY._options = None
  _TESTMAP_BOOLMAPENTRY._serialized_options = b'8\001'
  _TESTMAP_INT32MAPENTRY._options = None
  _TESTMAP_INT32MAPENTRY._serialized_options = b'8\001'
  _TESTMAP_INT64MAPENTRY._options = None
  _TESTMAP_INT64MAPENTRY._serialized_options = b'8\001'
  _TESTMAP_UINT32MAPENTRY._options = None
  _TESTMAP_UINT32MAPENTRY._serialized_options = b'8\001'
  _TESTMAP_UINT64MAPENTRY._options = None
  _TESTMAP_UINT64MAPENTRY._serialized_options = b'8\001'
  _TESTMAP_STRINGMAPENTRY._options = None
  _TESTMAP_STRINGMAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_BOOLMAPENTRY._options = None
  _TESTNESTEDMAP_BOOLMAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_INT32MAPENTRY._options = None
  _TESTNESTEDMAP_INT32MAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_INT64MAPENTRY._options = None
  _TESTNESTEDMAP_INT64MAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_UINT32MAPENTRY._options = None
  _TESTNESTEDMAP_UINT32MAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_UINT64MAPENTRY._options = None
  _TESTNESTEDMAP_UINT64MAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_STRINGMAPENTRY._options = None
  _TESTNESTEDMAP_STRINGMAPENTRY._serialized_options = b'8\001'
  _TESTNESTEDMAP_MAPMAPENTRY._options = None
  _TESTNESTEDMAP_MAPMAPENTRY._serialized_options = b'8\001'
  _TESTSTRINGMAP_STRINGMAPENTRY._options = None
  _TESTSTRINGMAP_STRINGMAPENTRY._serialized_options = b'8\001'
  _TESTBOOLVALUE_BOOLMAPENTRY._options = None
  _TESTBOOLVALUE_BOOLMAPENTRY._serialized_options = b'8\001'
  _ENUMTYPE._serialized_start=4849
  _ENUMTYPE._serialized_end=4877
  _MESSAGETYPE._serialized_start=277
  _MESSAGETYPE._serialized_end=305
  _TESTMESSAGE._serialized_start=308
  _TESTMESSAGE._serialized_end=968
  _TESTONEOF._serialized_start=971
  _TESTONEOF._serialized_end=1239
  _TESTMAP._serialized_start=1242
  _TESTMAP._serialized_end=1851
  _TESTMAP_BOOLMAPENTRY._serialized_start=1557
  _TESTMAP_BOOLMAPENTRY._serialized_end=1603
  _TESTMAP_INT32MAPENTRY._serialized_start=1605
  _TESTMAP_INT32MAPENTRY._serialized_end=1652
  _TESTMAP_INT64MAPENTRY._serialized_start=1654
  _TESTMAP_INT64MAPENTRY._serialized_end=1701
  _TESTMAP_UINT32MAPENTRY._serialized_start=1703
  _TESTMAP_UINT32MAPENTRY._serialized_end=1751
  _TESTMAP_UINT64MAPENTRY._serialized_start=1753
  _TESTMAP_UINT64MAPENTRY._serialized_end=1801
  _TESTMAP_STRINGMAPENTRY._serialized_start=1803
  _TESTMAP_STRINGMAPENTRY._serialized_end=1851
  _TESTNESTEDMAP._serialized_start=1854
  _TESTNESTEDMAP._serialized_end=2627
  _TESTNESTEDMAP_BOOLMAPENTRY._serialized_start=1557
  _TESTNESTEDMAP_BOOLMAPENTRY._serialized_end=1603
  _TESTNESTEDMAP_INT32MAPENTRY._serialized_start=1605
  _TESTNESTEDMAP_INT32MAPENTRY._serialized_end=1652
  _TESTNESTEDMAP_INT64MAPENTRY._serialized_start=1654
  _TESTNESTEDMAP_INT64MAPENTRY._serialized_end=1701
  _TESTNESTEDMAP_UINT32MAPENTRY._serialized_start=1703
  _TESTNESTEDMAP_UINT32MAPENTRY._serialized_end=1751
  _TESTNESTEDMAP_UINT64MAPENTRY._serialized_start=1753
  _TESTNESTEDMAP_UINT64MAPENTRY._serialized_end=1801
  _TESTNESTEDMAP_STRINGMAPENTRY._serialized_start=1803
  _TESTNESTEDMAP_STRINGMAPENTRY._serialized_end=1851
  _TESTNESTEDMAP_MAPMAPENTRY._serialized_start=2559
  _TESTNESTEDMAP_MAPMAPENTRY._serialized_end=2627
  _TESTSTRINGMAP._serialized_start=2629
  _TESTSTRINGMAP._serialized_end=2752
  _TESTSTRINGMAP_STRINGMAPENTRY._serialized_start=2704
  _TESTSTRINGMAP_STRINGMAPENTRY._serialized_end=2752
  _TESTWRAPPER._serialized_start=2755
  _TESTWRAPPER._serialized_end=3761
  _TESTTIMESTAMP._serialized_start=3763
  _TESTTIMESTAMP._serialized_end=3873
  _TESTDURATION._serialized_start=3875
  _TESTDURATION._serialized_end=3982
  _TESTFIELDMASK._serialized_start=3984
  _TESTFIELDMASK._serialized_end=4042
  _TESTSTRUCT._serialized_start=4044
  _TESTSTRUCT._serialized_end=4145
  _TESTANY._serialized_start=4147
  _TESTANY._serialized_end=4239
  _TESTVALUE._serialized_start=4241
  _TESTVALUE._serialized_end=4339
  _TESTLISTVALUE._serialized_start=4341
  _TESTLISTVALUE._serialized_end=4451
  _TESTBOOLVALUE._serialized_start=4454
  _TESTBOOLVALUE._serialized_end=4591
  _TESTBOOLVALUE_BOOLMAPENTRY._serialized_start=1557
  _TESTBOOLVALUE_BOOLMAPENTRY._serialized_end=1603
  _TESTCUSTOMJSONNAME._serialized_start=4593
  _TESTCUSTOMJSONNAME._serialized_end=4636
  _TESTEXTENSIONS._serialized_start=4638
  _TESTEXTENSIONS._serialized_end=4712
  _TESTENUMVALUE._serialized_start=4715
  _TESTENUMVALUE._serialized_end=4847
# @@protoc_insertion_point(module_scope)
