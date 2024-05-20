"""Module for encoding and decoding length delimited fields"""

# Copyright (c) 2018-2024 NCC Group Plc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import binascii
import copy
import sys
import six
import logging


import blackboxprotobuf.lib
from blackboxprotobuf.lib.types import varint, wiretypes
from blackboxprotobuf.lib.exceptions import (
    EncoderException,
    DecoderException,
    TypedefException,
)

if six.PY3:
    import typing

    if typing.TYPE_CHECKING:
        from blackboxprotobuf.lib.config import Config
        from typing import Any, Callable, Dict, Tuple, Optional, List
        from blackboxprotobuf.lib.pytypes import Message, TypeDef, FieldDef


def encode_string(value):
    # type: (Any) -> bytes
    """Encode a string as a length delimited byte array"""
    try:
        value = six.ensure_text(value)
    except TypeError as exc:
        six.raise_from(
            EncoderException("Error encoding string to message: %r" % value), exc
        )
    return encode_bytes(value)


def encode_bytes(value):
    # type: (Any) -> bytes
    """Encode a length delimited byte array"""
    if isinstance(value, bytearray):
        value = bytes(value)
    try:
        value = six.ensure_binary(value)
    except TypeError as exc:
        six.raise_from(
            EncoderException("Error encoding bytes to message: %r" % value), exc
        )

    if not isinstance(value, bytes):
        raise EncoderException(
            "encode_bytes must receive a bytes or bytearray value: %s %r"
            % (type(value), value)
        )
    encoded_length = varint.encode_varint(len(value))
    return encoded_length + value


def decode_bytes(buf, pos):
    # type: (bytes, int) -> Tuple[bytes, int]
    """Decode a length delimited bytes array from buf"""
    length, pos = varint.decode_varint(buf, pos)
    end = pos + length
    try:
        return buf[pos:end], end
    except IndexError as exc:
        six.raise_from(
            DecoderException(
                (
                    "Error decoding bytes. Decoded length %d is longer than bytes"
                    " available %d"
                )
                % (length, len(buf) - pos)
            ),
            exc,
        )


def encode_bytes_hex(value):
    # type: (Any) -> bytes
    """Encode a length delimited byte array represented by a hex string"""
    try:
        return encode_bytes(binascii.unhexlify(value))
    except (TypeError, binascii.Error) as exc:
        six.raise_from(
            EncoderException("Error encoding hex bytestring %s" % value), exc
        )


def decode_bytes_hex(buf, pos):
    # type: (bytes, int) -> Tuple[bytes, int]
    """Decode a length delimited byte array from buf and return a hex encoded string"""
    value, pos = decode_bytes(buf, pos)
    return binascii.hexlify(value), pos


def decode_string(value, pos):
    # type: (bytes, int) -> Tuple[str, int]
    """Decode a length delimited byte array as a string"""
    length, pos = varint.decode_varint(value, pos)
    end = pos + length
    try:
        # backslash escaping isn't reversible easily
        return value[pos:end].decode("utf-8"), end
    except (TypeError, UnicodeDecodeError) as exc:
        six.raise_from(
            DecoderException("Error decoding UTF-8 string %r" % value[pos:end]), exc
        )


def encode_tag(field_number, wire_type):
    # type: (int, int) -> bytes
    # Not checking bounds here, should be check before
    tag_number = (field_number << 3) | wire_type
    return varint.encode_uvarint(tag_number)


def decode_tag(buf, pos):
    # type: (bytes, int) -> Tuple[int, int, int]
    tag_number, pos = varint.decode_uvarint(buf, pos)
    field_number = tag_number >> 3
    wire_type = tag_number & 0x7
    return field_number, wire_type, pos


def encode_message(data, config, typedef, path=None, field_order=None):
    # type: (Message, Config, TypeDef, Optional[List[str]], Optional[List[str]]) -> bytes
    """Encode a Python dictionary to a binary protobuf message"""
    output = bytearray()
    if path is None:
        path = []

    output_len = 0
    field_outputs = {}  # type: Dict[str, List[bytes]]
    for field_id, value in data.items():
        field_number, outputs = _encode_message_field(
            config, typedef, path, field_id, value
        )

        # In case the field number is represented in multiple locations in data
        # (eg. as an int, as name, as a string with an int)
        if field_number in field_outputs:
            field_outputs[field_number].extend(outputs)
        else:
            field_outputs[field_number] = outputs
        output_len += len(outputs)

    output = bytearray()
    if output_len > 0:
        if (
            config.preserve_field_order
            and field_order is not None
            and len(field_order) == output_len
        ):
            # check for old typedefs which had field_order as a tuple
            if isinstance(field_order[0], tuple):
                field_order = [x[0] for x in field_order]
            for field_number in field_order:
                try:
                    output += field_outputs[field_number].pop(0)
                except (IndexError, KeyError):
                    # If these don't match up despite us checking the overall
                    # length, then we probably have something weird going on
                    # with field naming.
                    # This might mean ordering is off from the original, but
                    # should break real protobuf messages
                    logging.warning(
                        "The field_order list does not match the fields from _encode_message_field"
                    )
                    # If we're hitting a mismatch between the field order and
                    # what data we have, then just bail. We can encode the rest
                    # normally
                    break

        # Group  together elements in an array
        for values in field_outputs.values():
            for value in values:
                output += value

    return output


def _encode_message_field(config, typedef, path, field_id, value):
    # type: (Config, TypeDef, List[str], str | int, Any) -> Tuple[str, List[bytes]]
    # Get the field number convert it as necessary
    alt_field_number = None

    field_number = None
    # Convert the field_id, which could be a number or a name, into a field number
    # From a correctness standpoint, field_number should probably be an int
    # type, but IIRC that leads to headaches elsewhere
    if isinstance(field_id, six.text_type):
        if "-" in field_id:
            field_id, alt_field_number = field_id.split("-")
        if field_id.isdigit():
            field_number = field_id
        else:
            for number, info in typedef.items():
                if (
                    info.get("name", "") != ""
                    and info["name"] == field_id
                    and field_id != ""
                ):
                    field_number = number
                    break
    else:
        field_number = six.ensure_text(str(field_id))

    field_path = path[:]
    field_path.append(str(field_number))

    if field_number is None or field_number not in typedef:
        raise EncoderException(
            "Provided field name/number %s / %s is not valid"
            % (field_id, field_number),
            field_path,
        )

    field_typedef = typedef[field_number]

    # Get encoder
    if "type" not in field_typedef:
        raise TypedefException(
            "Field %s does not have a defined type." % field_number, field_path
        )

    field_type = field_typedef["type"]
    field_order = field_typedef.get("field_order", None)

    field_encoder = None  # type: Callable[[Any], bytes] | None
    if alt_field_number is not None:
        if alt_field_number not in field_typedef["alt_typedefs"]:
            raise EncoderException(
                "Provided alt field name/number %s is not valid for field_number %s"
                % (alt_field_number, field_number),
                field_path,
            )
        alt_field_type = field_typedef["alt_typedefs"][alt_field_number]
        if isinstance(alt_field_type, six.text_type):
            # just let the field
            field_type = alt_field_type
        else:
            innertypedef = alt_field_type
            field_encoder = lambda data: encode_lendelim_message(
                data, config, innertypedef, path=field_path, field_order=field_order
            )

    if field_encoder is None:
        if field_type == "message":
            if "message_typedef" in field_typedef:
                innertypedef = field_typedef["message_typedef"]
            elif "message_type_name" in field_typedef:
                message_type_name = field_typedef["message_type_name"]
                if message_type_name not in config.known_types:
                    raise TypedefException(
                        "Message type (%s) has not been defined"
                        % field_typedef["message_type_name"],
                        field_path,
                    )
                innertypedef = config.known_types[message_type_name]
            else:
                raise TypedefException(
                    "Could not find message typedef for %s" % field_number,
                    field_path,
                )

            field_encoder = lambda data: encode_lendelim_message(
                data, config, innertypedef, path=field_path, field_order=field_order
            )
        else:
            if field_type not in blackboxprotobuf.lib.types.ENCODERS:
                raise TypedefException("Unknown type: %s" % field_type)
            field_encoder = blackboxprotobuf.lib.types.ENCODERS[field_type]
            if field_encoder is None:
                raise TypedefException(
                    "Encoder not implemented for %s" % field_type, field_path
                )

    # Encode the tag
    tag = encode_tag(
        int(field_number), blackboxprotobuf.lib.types.WIRETYPES[field_type]
    )

    outputs = []
    try:
        # Repeated values we'll encode each one separately and add them to the outputs list
        # Packed values take in a list, but encode them into a single length
        # delimited field, so we handle those as a non-repeated value
        if isinstance(value, list) and not field_type.startswith("packed_"):
            for repeated in value:
                outputs.append(tag + field_encoder(repeated))
        else:
            outputs.append(tag + field_encoder(value))

    except EncoderException as exc:
        exc.set_path(field_path)
        six.reraise(*sys.exc_info())

    return field_number, outputs


def decode_message(buf, config, typedef=None, pos=0, end=None, depth=0, path=None):
    # type: (bytes, Config, Optional[TypeDef], int, Optional[int], int, Optional[List[str]]) -> Tuple[Message, TypeDef, List[str], int]
    """Decode a protobuf message with no length prefix"""
    if end is None:
        end = len(buf)

    if typedef is None:
        typedef = {}
    else:
        # Don't want to accidentally modify the original
        typedef = copy.deepcopy(typedef)

    if path is None:
        path = []

    output = {}  # type: Message

    grouped_fields, field_order, pos = _group_by_number(buf, pos, end, path)
    for field_number, (wire_type, buffers) in grouped_fields.items():
        # wire_type should already be validated by _group_by_number

        path = path[:] + [field_number]
        field_outputs = None
        field_typedef = typedef.get(field_number, {})
        field_key = _get_field_key(field_number, typedef, path)
        # Easy cases. Fixed size or bytes/string
        if wire_type in [
            wiretypes.FIXED32,
            wiretypes.FIXED64,
            wiretypes.VARINT,
        ] or ("type" in field_typedef and field_typedef["type"] != "message"):
            if "type" not in field_typedef:
                field_typedef["type"] = config.get_default_type(wire_type)
            else:
                # have a type, but make sure it matches the wiretype
                if (
                    blackboxprotobuf.lib.types.WIRETYPES[field_typedef["type"]]
                    != wire_type
                ):
                    raise DecoderException(
                        "Type %s from typedef did not match wiretype %s for "
                        "field %s" % (field_typedef["type"], wire_type, field_key),
                        path=path,
                    )

            # we already have a type, just map the decoder
            if field_typedef["type"] not in blackboxprotobuf.lib.types.DECODERS:
                raise TypedefException(
                    "Got unkown type %s for field_number %s"
                    % (field_typedef["type"], field_number),
                    path=path,
                )

            decoder = blackboxprotobuf.lib.types.DECODERS[field_typedef["type"]]
            field_outputs = [decoder(buf, 0) for buf in buffers]

            # this shouldn't happen, but let's check just in case
            for buf, _pos in zip(buffers, [y for _, y in field_outputs]):
                assert len(buf) == _pos

            field_outputs = [value for (value, _) in field_outputs]

            # Packed decoding will return a list of lists
            if field_typedef["type"].startswith("packed_"):
                field_outputs = [y for x in field_outputs for y in x]
                field_typedef[
                    "seen_repeated"
                ] = True  # packed fields are always repeated

            # Convert to a single element if theres only 1 field and we've
            # never seen it repeated before
            if len(field_outputs) > 1 or field_typedef.get("seen_repeated", False):
                output[field_key] = field_outputs
                field_typedef["seen_repeated"] = True
            else:
                output[field_key] = field_outputs[0]

        elif wire_type == wiretypes.LENGTH_DELIMITED:
            _try_decode_lendelim_fields(
                buffers, field_key, field_typedef, output, config
            )

        # Save the field typedef/type back to the typedef
        typedef[field_number] = field_typedef

    return output, typedef, field_order, pos


def _group_by_number(buf, pos, end, path):
    # type: (bytes, int, int, List[str]) -> Tuple[Dict[str, Tuple[int, List[bytes]]], List[str], int]
    # Parse through the whole message and split into buffers based on wire
    # type and organized by field number. This forces us to parse the whole
    # message at once, but I think we're doing that anyway. This catches size
    # errors early as well, which is usually the best indicator of if it's a
    # protobuf message or not.
    # Returns a dictionary like:
    #     {
    #         "2": (<wiretype>, [<data>])
    #     }

    output_map = {}  # type: Dict[str, Tuple[int, List[bytes]]]
    field_order = []
    while pos < end:
        # Read in a field
        field_number, wire_type, pos = decode_tag(buf, pos)

        # We want field numbers as strings everywhere
        field_id = six.ensure_text(str(field_number))

        field_path = path[:] + [field_id]

        if field_id in output_map and output_map[field_id][0] != wire_type:
            # This should never happen
            raise DecoderException(
                "Field %s has mistmatched wiretypes. Previous: %s Now: %s"
                % (field_id, output_map[field_id][0], wire_type),
                path=field_path,
            )

        length = None
        if wire_type == wiretypes.VARINT:
            # We actually have to read in the whole varint to figure out it's size
            _, new_pos = varint.decode_uvarint(buf, pos)
            length = new_pos - pos
        elif wire_type == wiretypes.FIXED32:
            length = 4
        elif wire_type == wiretypes.FIXED64:
            length = 8
        elif wire_type == wiretypes.LENGTH_DELIMITED:
            # Read the length from the start of the message
            # add on the length of the length tag as well
            bytes_length, new_pos = varint.decode_varint(buf, pos)
            length = bytes_length + (new_pos - pos)
        elif wire_type in [
            wiretypes.START_GROUP,
            wiretypes.END_GROUP,
        ]:
            raise DecoderException("GROUP wire types not supported", path=field_path)
        else:
            raise DecoderException(
                "Got unknown wire type: %d" % wire_type, path=field_path
            )
        if pos + length > end:
            raise DecoderException(
                "Decoded length for field %s goes over end: %d > %d"
                % (field_id, pos + length, end),
                path=field_path,
            )

        field_buf = buf[pos : pos + length]

        if field_id in output_map:
            output_map[field_id][1].append(field_buf)
        else:
            output_map[field_id] = (wire_type, [field_buf])
        field_order.append(field_id)
        pos += length
    return output_map, field_order, pos


def _get_field_key(field_number, typedef, path):
    # type: (str | int, TypeDef, List[str]) -> str
    # Translate a field_number into a name if one is available in the typedef
    if not isinstance(field_number, (int, six.text_type)):
        raise EncoderException("Field key in message must be a str or int", path=path)
    if isinstance(field_number, int):
        field_number = six.ensure_text(str(field_number))

    # handle an alt_typedef by transforming 1-1 to name-1
    # I don't think should actually be used with the current uses of
    # _get_field_key
    alt_field_number = None
    if "-" in field_number:
        field_number, alt_field_number = field_number.split("-")

    if field_number in typedef and typedef[field_number].get("name", "") != "":
        field_key = typedef[field_number]["name"]
    else:
        field_key = field_number
    # Return the new field_name + alt_field_number
    return field_key + ("" if alt_field_number is None else "-" + alt_field_number)


def _try_decode_lendelim_fields(
    buffers, field_key, field_typedef, message_output, config
):
    # type: (List[bytes], str, FieldDef, Message, Config) -> None
    # Mutates message_output

    # This is where things get weird
    # To start, since we want to decode messages and not treat every
    # embedded message as bytes, we have to guess if it's a message or
    # not.
    # Unlike other types, we can't assume our message types are
    # consistent across the tree or even within the same message.
    # A field could be a bytes type that that decodes to multiple different
    # messages that don't have the same type definition. This is where
    # 'alt_typedefs' let us say that these are the different message types
    # we've seen for this one field.
    # In general, if something decodes as a message once, the rest should too
    # and we can enforce that across a single message, but not multiple
    # messages.
    # This is going to change the definition of "alt_typedefs" a bit from just
    # alternate message type definitions to also allowing downgrading to
    # 'bytes' or string with an 'alt_type' if it doesn't parse

    try:
        outputs_map = {}  # type: Dict[str, Any]
        field_order = []  # type: List[str]
        # grab all dictonary alt_typedefs
        all_typedefs = {
            # we don't want this to modify in-place if it fails
            key: copy.deepcopy(value)
            for key, value in field_typedef.get("alt_typedefs", {}).items()
            if isinstance(value, dict)
        }  # type: Dict[str, TypeDef]
        all_typedefs["1"] = copy.deepcopy(field_typedef.get("message_typedef", {}))

        for buf in buffers:
            output = None
            output_typedef = None
            output_typedef_num = None
            new_field_order = []  # type: List[str]
            for alt_typedef_num, alt_typedef in sorted(
                all_typedefs.items(), key=lambda x: int(x[0])
            ):
                try:
                    (
                        output,
                        output_typedef,
                        new_field_order,
                        _,
                    ) = decode_lendelim_message(buf, config, alt_typedef)
                except:
                    continue
                output_typedef_num = alt_typedef_num
                break
            # try an anonymous type
            # let the error propogate up if we fail this
            if output is None:
                output, output_typedef, new_field_order, _ = decode_lendelim_message(
                    buf, config, {}
                )
                output_typedef_num = six.ensure_text(
                    str(max([int(i) for i in ["0"] + list(all_typedefs.keys())]) + 1)
                )

            if output_typedef is None or output_typedef_num is None:
                raise DecoderException(
                    "Could not find an output_typedef or output_typedef_num. This should not happen under any circumstances."
                )
            # save the output or typedef we found
            all_typedefs[output_typedef_num] = output_typedef
            output_list = outputs_map.get(output_typedef_num, [])
            output_list.append(output)
            outputs_map[output_typedef_num] = output_list

            # we should technically have a different field order for each instance of the data
            # but that would require a very messy JSON which we're trying to avoid
            if len(new_field_order) > len(field_order):
                field_order = new_field_order
        # was able to decode everything as a message
        field_typedef["type"] = "message"
        field_typedef["message_typedef"] = all_typedefs["1"]

        if config.preserve_field_order:
            field_typedef["field_order"] = field_order

        if len(all_typedefs.keys()) > 1:
            del all_typedefs["1"]
            field_typedef.setdefault("alt_typedefs", {}).update(all_typedefs)
        # messages get set as "key-alt_number"
        for output_typedef_num, outputs in outputs_map.items():
            output_field_key = field_key
            if output_typedef_num != "1":
                output_field_key += "-" + output_typedef_num

            if len(outputs) > 1 or field_typedef.get("seen_repeated", False):
                message_output[output_field_key] = outputs
                field_typedef["seen_repeated"] = True
            else:
                message_output[output_field_key] = outputs[0]
        # success, return
        return
    except DecoderException as exc:
        # this should be pretty common, don't be noisy or throw an exception
        logging.debug(
            "Could not decode a buffer for field number %s as a message: %s",
            field_key,
            exc,
        )

    # Decoding as a message did not work, try strings and then bytes
    # The bytes decoding should never fail
    for target_type in ["string", config.default_binary_type]:
        try:
            outputs = []
            decoder = blackboxprotobuf.lib.types.DECODERS[target_type]
            for buf in buffers:
                output, _ = decoder(buf, 0)
                outputs.append(output)

            # all outputs worked, this is our type
            # check if there is a message type already in the typedef
            if "type" in field_typedef and "message" == field_typedef["type"]:
                # we already had a message type. save it as an alt_typedef

                # check if we already have this type as an alt_typedef
                output_typedef_nums = [
                    key
                    for key, value in field_typedef.setdefault(
                        "alt_typedefs", {}
                    ).items()
                    if value == target_type
                ]
                output_typedef_num = None
                if len(output_typedef_nums) == 0:
                    # find the next largest alt typedef number to put this type as
                    output_typedef_num = six.ensure_text(
                        str(
                            max([int(i) for i in ["0"] + list(all_typedefs.keys())]) + 1
                        )
                    )
                    field_typedef.setdefault("alt_typedefs", {})[
                        output_typedef_num
                    ] = target_type
                else:
                    # we already have an alt typedef with this number
                    output_typedef_num = output_typedef_nums[0]
                message_output[field_key + "-" + output_typedef_num] = (
                    outputs if len(outputs) > 1 else outputs[0]
                )
            else:
                field_typedef["type"] = target_type
                message_output[field_key] = outputs if len(outputs) > 1 else outputs[0]
            return
        except DecoderException:
            continue


def encode_lendelim_message(data, config, typedef, path=None, field_order=None):
    # type: (Message, Config, TypeDef, Optional[List[str]], Optional[List[str]]) -> bytes
    """Encode data as a length delimited protobuf message"""
    message_out = encode_message(
        data, config, typedef, path=path, field_order=field_order
    )
    length = varint.encode_varint(len(message_out))
    logging.debug("Message length encoded: %d", len(length) + len(message_out))
    return length + message_out


def decode_lendelim_message(buf, config, typedef=None, pos=0, depth=0, path=None):
    # type: (bytes, Config, Optional[TypeDef], int, int, Optional[List[str]]) -> Tuple[Message, TypeDef, List[str], int]
    """Deocde a length delimited protobuf message from buf"""
    length, pos = varint.decode_varint(buf, pos)
    ret = decode_message(
        buf, config, typedef, pos, pos + length, depth=depth, path=path
    )
    return ret


def generate_packed_encoder(wrapped_encoder):
    # type: (Callable[[Any], bytes]) -> Callable[[List[Any]], bytes]
    """Generate an encoder for a packed type based on a base type encoder"""

    def length_wrapper(values):
        # type: (List[Any]) -> bytes
        # Encode repeat values and prefix with the length
        output = bytearray()
        for value in values:
            output += wrapped_encoder(value)
        length = varint.encode_varint(len(output))
        return length + output

    return length_wrapper


def generate_packed_decoder(wrapped_decoder):
    # type: (Callable[[bytes, int], Tuple[Any, int]]) -> Callable[[bytes, int], Tuple[List[Any], int]]
    """Generate an decoder for a packed type based on a base type decoder"""

    def length_wrapper(buf, pos):
        # type: (bytes, int) -> Tuple[List[Any], int]
        # Decode repeat values prefixed with the length
        length, pos = varint.decode_varint(buf, pos)
        end = pos + length
        output = []
        while pos < end:
            value, pos = wrapped_decoder(buf, pos)
            output.append(value)
        if pos > end:
            raise DecoderException(
                (
                    "Error decoding packed field. Packed length larger than"
                    " buffer: decoded = %d, left = %d"
                )
                % (length, len(buf) - pos)
            )
        return output, pos

    return length_wrapper
