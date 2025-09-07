# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_sierpinski_lfsr(dut):
    dut._log.info("Starting Sierpiński LFSR test")

    # Clock: 100 kHz (10 us period)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset and enable
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Released reset, starting sequence capture")

    # Capture first 50 outputs
    sequence = []
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        sequence.append(int(dut.uo_out.value))

    dut._log.info(f"Observed sequence: {sequence}")

    # Basic checks:
    # 1. Not all outputs are zero
    assert any(sequence), "Error: LFSR stuck at zero!"

    # 2. Not all outputs are the same
    assert len(set(sequence)) > 1, "Error: Output not changing!"

    # Optional: ensure pattern length is non-trivial
    unique_count = len(set(sequence))
    dut._log.info(f"Unique outputs seen in 50 cycles: {unique_count}")
    assert unique_count > 10, "Error: LFSR sequence too short!"

