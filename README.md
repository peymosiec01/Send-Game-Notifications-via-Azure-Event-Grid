# **Send Game Notifications via Azure Event Grid 🏀**


## **Overview**
**Day 2 of the 30 Days DevOps Challenge** `#DevOpsAllStarsChallenge`

This project demonstrates an event-driven solution for sending NBA game notifications using **Azure Event Grid** and a timer-triggered Azure Function.



## **Features**
- Fetches NBA game results via a scheduled Azure Function.
- Publishes notifications to an Azure Event Grid Topic.
- Subscribes to Event Grid events for email notifications using Azure Logic Apps.
- Configurable and easy-to-deploy project structure.



## **Project Structure**

```yaml
GAME-DAY-NOTIFICATIONS/
    ├── timer_trigger_game_notifications/ 
        ├── init.py                  # Main function logic 
        ├── function.json            # Azure Function configuration
    ├── .gitignore                   # Git ignore rules
    ├── host.json                    # Host-level configuration for Azure Functions
    ├── local.settings.json          # Local environment settings
    ├── README.md                    # Project documentation
    ├── requirements.txt             # Python dependencies
```



## **Azure Resources Used**

![image](https://github.com/user-attachments/assets/fa716613-f895-40d1-bc8e-be8b96762620)

- **Resource Group**: To organize all Azure resources.
- **Azure Function App**:Fetch game data and sending it to the Event Grid Topic.
- **Azure Event Grid Topic**: Publishes game notifications as events.
- **Logic App**: Sends email notifications when events are received.
- **Azure Storage**: Optional for diagnostics or logs.
- **Cron Job**: Automates the periodic execution of the Python script.



## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/Send-Game-Notifications-via-Azure-Event-Grid.git
cd Send-Game-Notifications-via-Azure-Event-Grid
```

### **2. Install Python Dependencies**
```python
pip install -r requirements.txt
```

### **3. Configure Local Environment**

Update the `local.settings.json` file with your settings:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<YourAzureStorageConnectionString>",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "EVENT_GRID_TOPIC_ENDPOINT": "<YourEventGridTopicEndpoint>",
    "EVENT_GRID_TOPIC_KEY": "<YourEventGridTopicKey>",
    "SPORTS_API_KEY": "<YourNBAApiKey>"
  }
}
```

Update the `function.json` file with your configuration of the timer-triggered Azure Function:
- **Timer Schedule (schedule):** The function runs every minute (0 */1 * * * *).
- **authLevel:** Admin access level for the trigger
```json
{
    "scriptFile": "__init__.py",
    "entryPoint": "main",
    "bindings": [
      {
        "authLevel": "admin",
        "name": "mytimer",
        "type": "timerTrigger",
        "direction": "in",
        "schedule": "0 */1 * * * *",
        "useMonitor": true
      }
    ]
}
```

### **4. Set Up Azure Resources**
- **Resource Group**: Organizes all project-related resources.
- **Azure Event Grid Topic**: Centralized event publisher for game notifications.
- **Logic App**: Subscribed to Event Grid for sending email notifications.
- **Azure Storage Account**: Required for Azure Function bindings and internal state management.
- **Timer-Triggered Azure Function**: Automates game notification events.


## **Testing Locally**
Run the Azure Function locally:
```bash
func start
```

## **Sample Event**
A sample event published to Event Grid:
![image](https://github.com/user-attachments/assets/0bf4d2bb-5a12-47c1-b599-9ab8bb65bc5a)


## **Deploying App**
After setting up the Azure resources and configuring your local environment, deploy the Azure Function to the Function App:
```bash
func azure functionapp publish GameNotifications --build remote
```
This command ensures that the project is built and deployed in Azure.

## **License**
This project is licensed under the MIT License.
