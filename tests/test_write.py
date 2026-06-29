import time
from modbus_service import ModbusPLCService

def main():
    # 1. Initialize and connect to your PLC
    plc = ModbusPLCService(port='/dev/ttyUSB0')
    
    if not plc.connect():
        print("Could not start write test: Connection failed.")
        return

    # 2. Configure your target test parameters
    # Change these values based on your PLC board's hardware manual
    target_address = 0x00  # The register address you want to change
    test_value = 0         # The value you want to write (e.g., 1 to turn on a relay)
    slave_id = 1           # Your Modbus slave ID

    print(f"\n--- Starting Modbus Write Test ---")
    print(f"Targeting Register Address: {target_address} (Decimal) / {hex(target_address)} (Hex)")
    print(f"Sending Value: {test_value}")

    # 3. Execute the write operation
    success = plc.write_output(address=target_address, value=test_value, slave_id=slave_id)

    if success:
        print("✔ Write operation successfully acknowledged by the PLC!")
        
        # 4. Optional Verification: Read the specific register back to confirm
        print("Verifying register state...")
        time.sleep(0.05)  # Small 50ms pause to let the hardware settle
        
        # Read a tiny window (count=2) starting slightly before or at our target
        updated_data = plc.read_inputs(address=target_address, count=1, slave_id=slave_id)
        
        if updated_data:
            print(f"✔ Verification Success! Current register value is now: {updated_data[0]}")
        else:
            print("❌ Failed to read back the register state for verification.")
    else:
        print("❌ Write operation failed! Check if the address is write-protected or invalid.")

    # 5. Safely clean up the connection
    print("----------------------------------")
    plc.disconnect()

if __name__ == "__main__":
    main()

