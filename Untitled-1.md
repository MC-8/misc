# Notes
Startup code:
1. Disables interrupts
2. Copy any initialised data from ROM to RAM
3. Zeros uninitialised data area
4. Allocate space for and initialize the stack
5. Initialize the processor's stack pointer
6. Call main()

Linker script:
Sometimes used to control the exact order of code and data section. Also to establish the physical location of each section in memory.

stack
heap
.bss
.data
.text

Memory model (Cortex M4)
Vendor specific
private peripheral bus
External devices
Extaenrla RAM
On-chip Peripherals
SRAM
Code



Interrupt table.
Cortex-M has a vector table at 0 that contains all pointers,
The first entry contains the start-up value for the SP register, the second is the reset vector.

Map file?

RISC:
Fetch
Decode
Execute
Memory Access
Writeback
