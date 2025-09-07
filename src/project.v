/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_sierpinski_lfsr (
    input  wire clk,       // system clock
    input  wire rst_n,     // active-low reset
    output reg  [7:0] lfsr_out // 8-bit LFSR state (row of triangle)
);

    reg [7:0] lfsr;

    // Feedback taps for maximal-length LFSR (x^8 + x^6 + x^5 + x^4 + 1)
    wire feedback = lfsr[7] ^ lfsr[5] ^ lfsr[4] ^ lfsr[3];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            lfsr <= 8'b0000_0001;  // seed value (start with single '1')
        else
            lfsr <= {lfsr[6:0], feedback};
    end

    // Assign LFSR state to output
    always @(*) begin
        lfsr_out = lfsr;
    end

endmodule
