# Modules

> Note: This chapter is merely a short introduction. The [Modules](https://amaranth-lang.org/docs/amaranth/latest/lang.html#modules) chapter of the Amaranth language guide goes into more detail.

A *module* is a reusable bit of HDL code. Think of it like the specification of a chip, where now you can use as many of those chips as you want in other modules.

## Basic structure of a module

Modules can be conveniently created using Python classes derived from Amaranth's `Elaboratable` class. A minimal starting skeleton is shown here. A bit later we'll take a look at how to put HDL code in modules.

```python
from amaranth import Elaboratable, Module
from amaranth.build import Platform


class ThingBlock(Elaboratable):
    def __init__(self):
        pass

    def elaborate(self, platform: Platform) -> Module:
        m = Module()
        return m
```

## Elaborating a module

Elaboration means translating your HDL code to either Verilog or RTLIL (Register Transfer Language Intermediate Language) representation.

A minimal main file for elaborating a top-level module and all its submodules is shown here. Again, much of this will be made clear in a short while.

```python
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
```

Note that `ThingBlock` is the module class we defined above. We also define a top-level module `m` which contains an instantiation of `ThingBlock` (`block`), plus some other things that we explain further below.

* `main(module, ports=[<ports>], platform="<platform>")` elaborates the given module, including any submodules, recursively. All `elaborate()` methods will have its `platform` argument set to the given `platform`, which can be `None`, or a `Platform` representing a particular chip or development board. Elaboratables might create different logic for different platforms, and they can directly access chip pins via the platform.

```sh
python3 elaborate_main.py generate -t [v|il|cc] > thing.[v|il|cc]
```

Generating a module results in a single file which includes all submodules.

You should choose Verilog (`-t v`) if you want to work with vendor tools that understand Verilog, or use RTLIL (`-t il`) if you will be working with yosys. You can also output a C++ file for CXXRTL (`-t cc`).

## Domains

A *domain*, in its basic definition, is a grouping of logic elements. If we consider a module as a black box with inputs and outputs, then any given output is generated within one and only one domain. If you attempt to set an output in more than one domain, you'll get an error during elaboration that the signal has more than one driver -- a "driver-driver conflict".

`Modules` come with two domains built in: a combinatorial domain and a synchronous domain.

The domains in a `Module` can be accessed through its `d` attribute.

### Combinatorial

Logic that contains no clocked elements is called *combinatorial*: it just combines logic elements together. This is one of the domains that a `Module` contains. It is always named `comb`, and it can be accessed via `m.d.comb`.

### Synchronous

Logic that contains clocked elements is called *synchronous* because all of the flip-flops (FFs) within a particular clock domain all change, in synchrony, according to the clock domain's clock. Each clock domain also has a reset signal which can reset all FFs to a given state. Finally, the domain specifies the edge of its clock on which all the FFs change: positive or negative.

FFs that are not clocked using the edge of a given clock domain cannot be in that clock domain. By definition, they have a different clock and reset, and so belong in a different clock domain. Attempts to set a signal in two clock domains will result in a driver-driver conflict.

Some hardware supports only one clock domain. Many FPGAs support at least two clock domains.

Unless otherwise specified, there is one synchronous domain in a `Module` called `sync`. It can be accessed via `m.d.sync`.

### Creating more domains

There is no reason to create combinatorial domains. As mentioned above, modules already contain one combinatorial domain, `comb`.

You can create a synchronous clock domain using `ClockDomain("<domain-name>", clk_edge="<pos|neg>")`. This gives you both the clock and the reset signal for the domain. By default, the domain name is `sync` and the clock edge is `pos`.

You add the domain to a module using the syntax `m.domains += <clockdomain>`. For example, to add a clock domain called `clk` to module `m`:

```python
from amaranth import ClockDomain

m = Module()
m.domains += ClockDomain("clk")

m.d.clk += ... # logic to add in the "clk" clock domain.
```

You can access a domain within a module via its name. So a domain created via `ClockDomain("myclk")` is accessed via `m.d.myclk`, or `m.d["myclk"]`.

You can get the clock and reset signals like so:

* `ClockSignal(domain="<domain>")` gives you the clock signal for the given domain.
* `ResetSignal(domain="<domain>")` gives you the reset signal for the given domain.

### Tip: clock domains with the same clock but different edges

This can be done simply by creating one `ClockDomain` for the positive edge, and then creating another `ClockDomain` with a different domain name and `clk_edge="neg"`:

```python
pos = ClockDomain("pos")
neg = ClockDomain("neg", clk_edge="neg")
```

Next, assign the positive domain's clock and reset signal to the negative domain:

```python
neg.clk = pos.clk
neg.rst = pos.rst
```

And then you can add these to the module. We can add more than domain to a module with the same statement:

```python
m.domains += [pos, neg]
```

### Access to domains

As stated above, a module can access its domains via its `d` attribute. By default, if a synchronous domain is added to a module's `domains` attribute, then all modules everywhere will also have access to that domain via their `d` attribute, even if that module is not a submodule of the module where the domain was added. This is convenient when dealing with hardware that has global clock domains.

```python
m = Module()
m2 = Module()

m.domains += ClockDomain("thing")
m.d.thing += # logic
m2.d.thing += # logic
```

You can explicitly inhibit this global propagation by setting the `local` named parameter of the `ClockDomain` to `True`. This forces the clock to only be present in the domain of the module it was added to, and all submodules of that module.

```python
m = Module()
m2 = Module()

m.domains += ClockDomain("thing", local=True)
m.d.thing += # logic
m2.d.thing += # this will fail
```

## Ports

The equivalent of ports in a module is public attributes. In the following example, `a` and `data` are publicly available to other modules, while `b` is not, just as `a` and `data` are publicly available to other Python classes, and `b` is not.

```python
class ThingBlock(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.data = Signal(8)

    def elaborate(self, platform: str):
        m = Module()

        b = Signal()

        return m
```

## Reset/default values for signals

If a signal is set in the *combinatorial* domain, then you can specify the default value of the signal if it is not set. By default, this is zero, but for a non-zero value, you can specify the default value for a signal when constructing the signal by setting the `reset` named parameter in the constructor. For example, this creates a 16-bit unsigned signal, `self.x`, which defaults to `0x1000` if not set:

```python
self.x = Signal(unsigned(16), reset=0x1000)  # Yes, "reset".
```

Likewise, if a signal is set in a *synchronous* domain, then you can specify its reset value using the `reset` named parameter in the constructor. By default the reset value is zero.

### Explicitly not resetting

For synchronous signals (that is, signals set in a synchronous domain), you can specify that it should *not* reset on the reset signal, instead only getting an *initial value* on power-up. This is done by setting the `reset_less` named parameter in the constructor to `True`:

```python
self.x = Signal(unsigned(16), reset=0x1000, reset_less=True)
```

This would create a 16-bit unsigned signal that is initially set to `0x1000`, but is not reset to that value when the domain's reset signal is activated.

This is especially useful during simulation or formal verification where you want to activate the reset, but keep some signals "outside" the reset. For example, a cycle counter that maintains its count across resets.
