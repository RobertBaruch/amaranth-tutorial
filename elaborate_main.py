from amaranth import ClockDomain, Module
from amaranth.cli import main

from thing_block import ThingBlock


if __name__ == "__main__":
    sync = ClockDomain()

    block = ThingBlock()

    m = Module()
    m.domains += sync
    m.submodules += block

    main(m, ports=[sync.clk, sync.rst])
