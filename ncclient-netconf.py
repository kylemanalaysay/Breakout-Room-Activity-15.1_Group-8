from ncclient import manager
import xml.dom.minidom
import requests

def connect_to_device(device_ip, username, password):
    try:
        device = manager.connect(
            host="192.168.199.128",
            username="cisco",
            password="cisco123!",
            port=830,  
            hostkey_verify=False,  
            device_params={'name': 'iosxe'},  
        )
        return device
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_running_config(device):
    try:
        running_config_xml = device.get_config(source='running').data_xml

        # Prettify the XML response using xml.dom.minidom
        dom = xml.dom.minidom.parseString(running_config_xml)
        running_config_pretty = dom.toprettyxml()

        return running_config_pretty
    except Exception as e:
        print(f"Error fetching running-config: {e}")
        return None


def make_configuration_changes(device):
    change_1 = """
    <!-- YANG model structure for change 1 -->
    <!-- Adding a loopback interface -->
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback100</name>
                <description>Loopback Interface</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
"""

    change_2 = """
    <!-- YANG model structure for change 2 -->
    <!-- Adding a user -->
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <username>
                <name>NewUser</name>
                <privilege>15</privilege>
                <password>
                    <password>password123</password>
                </password>
            </username>
        </native>
    </config>
"""

    change_3 = """
    <!-- YANG model structure for change 3 -->
    <!-- Modifying banner configuration -->
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <banner>
                <motd>
                    <banner>Updated banner message goes here</banner>
                </motd>
            </banner>
        </native>
    </config>
"""

    try:
        # Apply changes using the edit-config operation
        device.edit_config(target='running', config=change_1)
        device.edit_config(target='running', config=change_2)
        device.edit_config(target='running', config=change_3)

        print("Configuration changes applied successfully.")
    except Exception as e:
        print(f"Error applying configuration changes: {e}")

# Function to send notification to WebEx Teams group
def send_notification(message):
    # Replace 'YOUR_WEBEX_TEAMS_TOKEN' with your actual token
    token = 'MzdhMTQyY2ItZDhjYi00N2JmLTg0NzEtNjg2YjlkMWM1NjRjZjRiYWNkNTYtNWE4_P0A1_d0b19fc5-a717-4064-90e2-8d88b3acad9c'
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'roomId': 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNTdhOTMzYjAtM2M5ZS0xMWVlLWFiMDktYmQ0MzlhYWFkNjUy',  
        'text': "Hello team! I've made some configuration updates. Please review."
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending notification: {e}")


if __name__ == "__main__":
    
    device_ip = "192.168.199.128"
    username = "cisco"
    password = "cisco123!"

    # Connect to the device
    device = connect_to_device(device_ip, username, password)

    if device:
        # Get current running-config
        running_config = get_running_config(device)
        
        if running_config:
            print("Current Running Config:")
            print(running_config)

            # Make configuration changes
            make_configuration_changes(device)

            # Verify the new running-config after changes
            new_running_config = get_running_config(device)

            if new_running_config:
                print("\nNew Running Config after Changes:")
                print(new_running_config)
                send_notification("Configuration changes have been applied successfully.")

            # Close NETCONF session
            device.close_session()


