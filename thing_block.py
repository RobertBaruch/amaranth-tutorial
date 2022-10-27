from amaranth import Elaboratable, Module
from amaranth.build import Platform


class ThingBlock(Elaboratable):
    def __init__(self):
        pass

    def elaborate(self, platform: Platform) -> Module:
        m = Module()
        return m
