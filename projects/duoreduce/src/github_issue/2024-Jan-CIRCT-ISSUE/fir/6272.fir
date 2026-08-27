circuit Foo:
  module Foo:
    input r: {addr: UInt<3>, en: UInt<1> clk: Clock, flip data: {a: Clock}}
    input w: {addr: UInt<3>, en: UInt<1> clk: Clock, data: {a: Clock}, mask: {a: UInt<1>}}

    mem memory:
      data-type => {a: Clock}
      depth => 16
      reader => r
      writer => w
      read-latency => 1
      write-latency => 1
      read-under-write => undefined

    memory.r <= r
    memory.w <= w
