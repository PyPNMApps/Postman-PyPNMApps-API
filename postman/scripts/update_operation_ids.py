#!/usr/bin/env python3
"""
Script to update PyPNM API collection with correct operation_id format.
Based on collection run analysis showing API returns operation_id in nested structure.
"""

import json
import sys
from pathlib import Path

def update_collection(collection_path):
    """Update the collection with correct operation_id references."""
    
    # Read the collection
    with open(collection_path, 'r', encoding='utf-8') as f:
        collection = json.load(f)
    
    # Track changes
    changes = []
    
    # 1. Add collection variables for operation_id and group_id
    if 'variable' not in collection:
        collection['variable'] = []
    
    # Check if operation_id variable exists
    has_operation_id = any(v.get('key') == 'operation_id' for v in collection['variable'])
    has_group_id = any(v.get('key') == 'group_id' for v in collection['variable'])
    
    if not has_operation_id:
        collection['variable'].append({
            "key": "operation_id",
            "value": "op-001",
            "type": "string"
        })
        changes.append("Added operation_id collection variable")
    
    if not has_group_id:
        collection['variable'].append({
            "key": "group_id",
            "value": "grp-001",
            "type": "string"
        })
        changes.append("Added group_id collection variable")
    
    # 2. Update all requests recursively
    def update_items(items):
        for item in items:
            if 'item' in item:
                # It's a folder, recurse
                update_items(item['item'])
            elif 'request' in item:
                # It's a request
                request = item['request']
                
                # Update path variables that use hardcoded operation_id
                if 'url' in request and 'variable' in request['url']:
                    for var in request['url']['variable']:
                        if var.get('key') == 'operation_id' and var.get('value') == 'op-001':
                            var['value'] = '{{operation_id}}'
                            changes.append(f"Updated operation_id path variable in: {item.get('name', 'Unknown')}")
                        elif var.get('key') == 'group_id' and var.get('value') == 'grp-001':
                            var['value'] = '{{group_id}}'
                            changes.append(f"Updated group_id path variable in: {item.get('name', 'Unknown')}")
                
            # Update test scripts
            if 'event' in item:
                for event in item['event']:
                    if event.get('listen') == 'test' and 'script' in event:
                        script_lines = event['script'].get('exec', [])
                        updated = False
                        
                        for i, line in enumerate(script_lines):
                            # Fix: operation.id -> operation.operation_id
                            if "operation).to.have.property('id')" in line:
                                script_lines[i] = line.replace("property('id')", "property('operation_id')")
                                updated = True
                            
                            if "operation.id)" in line and "collectionVariables.set" in line:
                                script_lines[i] = line.replace("operation.id)", "operation.operation_id)")
                                updated = True
                            
                            # Fix: jsonData.id -> jsonData.operation.operation_id (for Get Operation Status)
                            if "jsonData).to.have.property('id')" in line and "Operation status" in str(script_lines):
                                script_lines[i] = line.replace("jsonData).to.have.property('id')", "jsonData).to.have.property('operation')")
                                updated = True
                            
                            if "jsonData).to.have.property('status')" in line and i > 0 and "jsonData).to.have.property('id')" in script_lines[i-1]:
                                script_lines[i] = line.replace("jsonData).to.have.property('status')", "jsonData.operation).to.have.property('operation_id')")
                                # Insert new line after
                                script_lines.insert(i+1, "        pm.expect(jsonData.operation).to.have.property('status');")
                                updated = True
                            
                            if "jsonData.status)" in line and "oneOf" in line and i > 1 and "Operation status" in str(script_lines):
                                script_lines[i] = line.replace("jsonData.status)", "jsonData.operation.status)")
                                updated = True
                            
                            # Fix: jsonData.id -> jsonData.operation_id (for Multi RxMER Status)
                            if "jsonData).to.have.property('id')" in line and "Multi" not in item.get('name', ''):
                                # This is for the pypnm/operations/status endpoint
                                pass  # Already handled above
                            elif "jsonData).to.have.property('id')" in line:
                                # This is for multi operations
                                script_lines[i] = line.replace("property('id')", "property('operation_id')")
                                updated = True
                            
                            # Fix: Response is an array -> Response contains operations array
                            if "Response is an array of operations" in line and "Get Group Operations" in item.get('name', ''):
                                script_lines[i] = line.replace("Response is an array of operations", "Response contains operations array")
                                updated = True
                            
                            if "jsonData).to.be.an('array')" in line and i > 0 and "Response contains operations array" in script_lines[i-1]:
                                script_lines[i] = "        pm.expect(jsonData).to.have.property('operations');"
                                script_lines.insert(i+1, "        pm.expect(jsonData.operations).to.be.an('array');")
                                updated = True
                        
                        if updated:
                            changes.append(f"Updated test script in: {item.get('name', 'Unknown')}")
    
    # Process all items
    if 'item' in collection:
        update_items(collection['item'])
    
    # Write back the collection
    with open(collection_path, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2)
    
    return changes

if __name__ == '__main__':
    collection_path = Path(__file__).parent.parent / 'collections' / 'PyPNM API.postman_collection.json'
    
    if not collection_path.exists():
        print(f"Error: Collection not found at {collection_path}")
        sys.exit(1)
    
    print(f"Updating collection: {collection_path}")
    changes = update_collection(collection_path)
    
    print(f"\nCompleted {len(changes)} changes:")
    for change in changes:
        print(f"  - {change}")
    
    print("\nCollection updated successfully!")
