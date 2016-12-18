class Converter(object):
    """
    Convenience Wrapper based on conversion functions.
    Derived classes must define class methods 'to_internal' and 'from_internal'.
    """

    def __init__(self, value, *acceptable_types):
        if type(self) == type(value):
            self.value = value.value
        elif isinstance(value, acceptable_types):
            self.value = value
        else:
            self.cw_val = value

    @property
    def cw_val(self):
        try:
            return getattr(type(self), 'from_internal')(self.value)
        except:
            raise TypeError("error while converting {} to type {}".format(self.value, type(self)))

    @classmethod
    def from_internal(cls, value):
        raise AttributeError("derived class {} do not provide 'from_internal' method".format(cls))

    @cw_val.setter
    def cw_val(self, value):
        try:
            self.value = self.to_internal(value)
        except:
            raise TypeError("cannot convert value {} to type {}".format(value, type(self)))

    @classmethod
    def to_internal(cls, value):
        raise AttributeError("derived class {} do not provide 'to_internal' method".format(cls))

    def __str__(self):
        return self.cw_val


class CW_dict(Converter):
    """
    Convenience Wrapper based on dictionary mapping.
    Builds 'to_internal' and 'from_internal' methods automatically.
    Derived classes must define static 'alias_map' dictionary.
    """

    def __init__(self, value, *acceptable_types):
        Converter.__init__(self, value, *acceptable_types)

    @classmethod
    def to_internal(cls, alias):
        alias_map = getattr(cls, 'alias_map', None)
        if alias_map is None:
            raise AttributeError("CW class must provide 'alias_map' attribute")
        if alias not in alias_map:
            raise ValueError("unknown alias " + str(alias))
        return alias_map[alias]

    @classmethod
    def from_internal(cls, value):
        alias_map = getattr(cls, 'alias_map', None)
        if alias_map is None:
            raise AttributeError("CW class must provide 'alias_map' attribute")
        for alias, val in alias_map.items():
            if val == value:
                return alias
        raise ValueError("no alias matches value " + str(value))


class CW_in_port(CW_dict):
    """Convenience wrapper for Port Type field"""
    def __init__(self, value):
        CW_dict.__init__(self, value, int)
    alias_map = {
        'drop': 0x00,
        'ctrl': 0xFF
    }


class CW_eth(Converter):
    """Convenience Wrapper for MAC address"""
    def __init__(self, value):
        Converter.__init__(self, value, int)

    @classmethod
    def to_internal(cls, value):
        return sum(int(x) << (5 - i) * 8 for i, x in enumerate(value.split(':')))
        # return reduce(lambda s, x: (s << 8) + int(x), mac.split(':'), 0)

    @classmethod
    def from_internal(cls, value):
        """Converts integer into conventional MAC string (ca:fe:de:ad:be:ef)"""
        return ':'.join(str((value >> x) & 0xFF) for x in range(40, -8, -8))


class CW_eth_type(CW_dict):
    """Convenience Wrapper for Ether Type field"""
    def __init__(self, value):
        CW_dict.__init__(self, value, int)
    alias_map = {
        'ipv4': 0x0800,
        'arp':  0x0806
    }


class CW_ip(Converter):
    """Convenience Wrapper for IP address"""
    def __init__(self, value):
        Converter.__init__(self, value, int)

    @classmethod
    def to_internal(cls, value):
        return sum(int(x) << (3 - i) * 8 for i, x in enumerate(value.split('.')))
        # return reduce(lambda s, x: (s << 8) + int(x), ip.split('.'), 0)

    @classmethod
    def from_internal(cls, value):
        return '.'.join(str((value >> x) & 0xFF) for x in range(24, -8, -8))


class CW_ip_proto(CW_dict):
    """Convenience Wrapper for IP protocol field"""
    def __init__(self, value):
        CW_dict.__init__(self, value, int)
    alias_map = {
        'ipv4': 4,
        'tcp':  6
    }


class CW_tp_port(CW_dict):
    """Convenience wrapper for transport protocol port"""
    def __init__(self, value):
        CW_dict.__init__(self, value, int)
    alias_map = {
        'http': 80,
        'ssh':  22
    }
