# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: jolt/plugins/remote_execution/worker.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from jolt import common_pb2 as jolt_dot_common__pb2
from jolt.plugins.remote_execution import scheduler_pb2 as jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*jolt/plugins/remote_execution/worker.proto\x1a\x11jolt/common.proto\x1a-jolt/plugins/remote_execution/scheduler.proto\"\xaf\x01\n\rWorkerRequest\x12%\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32\x15.WorkerRequest.Action\x12\x1c\n\x05\x62uild\x18\x02 \x01(\x0b\x32\r.BuildRequest\x12\x11\n\tworker_id\x18\x03 \x01(\t\x12\x10\n\x08\x62uild_id\x18\x04 \x01(\t\"4\n\x06\x41\x63tion\x12\t\n\x05\x42UILD\x10\x00\x12\x10\n\x0c\x43\x41NCEL_BUILD\x10\x01\x12\r\n\tTERMINATE\x10\x02\"\xf1\x01\n\x0cWorkerUpdate\x12$\n\x06status\x18\x01 \x01(\x0e\x32\x14.WorkerUpdate.Status\x12\x1b\n\x08platform\x18\x02 \x01(\x0b\x32\t.Platform\x12 \n\rtask_platform\x18\x04 \x01(\x0b\x32\t.Platform\x12\x1b\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x0c.WorkerError\"_\n\x06Status\x12\r\n\tENLISTING\x10\x00\x12\r\n\tDELISTING\x10\x01\x12\x0f\n\x0b\x42UILD_ENDED\x10\x02\x12\x11\n\rDEPLOY_FAILED\x10\x03\x12\x13\n\x0f\x45XECUTOR_FAILED\x10\x04\"/\n\x0bWorkerError\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t2i\n\x06Worker\x12\x34\n\x0fGetInstructions\x12\r.WorkerUpdate\x1a\x0e.WorkerRequest(\x01\x30\x01\x12)\n\x08GetTasks\x12\x0b.TaskUpdate\x1a\x0c.TaskRequest(\x01\x30\x01\x42\x0eZ\x0cpkg/protocolb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'jolt.plugins.remote_execution.worker_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\014pkg/protocol'
  _WORKERREQUEST._serialized_start=113
  _WORKERREQUEST._serialized_end=288
  _WORKERREQUEST_ACTION._serialized_start=236
  _WORKERREQUEST_ACTION._serialized_end=288
  _WORKERUPDATE._serialized_start=291
  _WORKERUPDATE._serialized_end=532
  _WORKERUPDATE_STATUS._serialized_start=437
  _WORKERUPDATE_STATUS._serialized_end=532
  _WORKERERROR._serialized_start=534
  _WORKERERROR._serialized_end=581
  _WORKER._serialized_start=583
  _WORKER._serialized_end=688
# @@protoc_insertion_point(module_scope)
