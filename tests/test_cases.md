# Test Cases

| ID | Test case | Expected result |
|---|---|---|
| TC01 | Add valid workstation | Asset is stored successfully |
| TC02 | Add duplicate Asset ID | Validation error is shown |
| TC03 | Enter invalid Asset Type | Validation error is shown |
| TC04 | Enter invalid IP address | Validation error is shown |
| TC05 | Display assets | Inventory and summary counts are displayed |
| TC06 | Search by Asset ID/name/IP/department | Matching assets are displayed |
| TC07 | Update an existing asset | Selected fields are updated |
| TC08 | Update a non-existing asset | `Asset not found.` is displayed |
| TC09 | Delete an existing asset | Asset is removed from storage |
| TC10 | Delete a non-existing asset | `Asset not found.` is displayed |
| TC11 | Invalid menu choice | `Invalid choice. Please select 1-6.` is displayed |
| TC12 | Empty required input | Validation error is shown |
