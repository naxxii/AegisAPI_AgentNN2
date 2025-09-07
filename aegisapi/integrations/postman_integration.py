"""
Postman Integration for AegisAPI AgentNN
Supports importing Postman collections and exporting test results
"""
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..telemetry import log_event

class PostmanCollection:
    """Represents a Postman collection"""

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.name = data.get('info', {}).get('name', 'Unnamed Collection')
        self.requests = []

    def parse_requests(self) -> List[Dict[str, Any]]:
        """Parse all requests from the collection"""
        requests = []

        def extract_requests(items, parent_folder=""):
            for item in items:
                if 'request' in item:
                    # This is a request
                    request_data = self._parse_request(item, parent_folder)
                    requests.append(request_data)
                elif 'item' in item:
                    # This is a folder
                    folder_name = item.get('name', 'Unnamed Folder')
                    current_folder = f"{parent_folder}/{folder_name}" if parent_folder else folder_name
                    extract_requests(item['item'], current_folder)

        if 'item' in self.data:
            extract_requests(self.data['item'])

        self.requests = requests
        return requests

    def _parse_request(self, item: Dict[str, Any], folder: str = "") -> Dict[str, Any]:
        """Parse individual request from collection"""
        request = item['request']
        url_data = request.get('url', {})

        # Handle different URL formats
        if isinstance(url_data, str):
            url = url_data
            path = url_data
        elif isinstance(url_data, dict):
            if 'raw' in url_data:
                url = url_data['raw']
                path = url_data.get('path', [])
                if isinstance(path, list):
                    path = '/' + '/'.join(path)
                else:
                    path = str(path)
            else:
                url = str(url_data)
                path = str(url_data)
        else:
            url = str(url_data)
            path = str(url_data)

        # Parse method
        method = request.get('method', 'GET')

        # Parse headers
        headers = {}
        for header in request.get('header', []):
            if header.get('key') and header.get('value'):
                headers[header['key']] = header['value']

        # Parse body
        body = {}
        request_body = request.get('body', {})
        if request_body.get('mode') == 'raw' and request_body.get('raw'):
            try:
                body = json.loads(request_body['raw'])
            except:
                body = request_body['raw']

        # Parse query parameters
        params = {}
        if isinstance(url_data, dict) and 'query' in url_data:
            for query in url_data['query']:
                if query.get('key') and query.get('value'):
                    params[query['key']] = query['value']

        return {
            'id': str(uuid.uuid4()),
            'name': item.get('name', 'Unnamed Request'),
            'method': method,
            'url': url,
            'path': path,
            'headers': headers,
            'params': params,
            'body': body,
            'folder': folder,
            'description': item.get('description', ''),
            'tests': item.get('event', [])
        }

    def to_openapi_spec(self) -> Dict[str, Any]:
        """Convert Postman collection to OpenAPI specification"""
        spec = {
            'openapi': '3.0.3',
            'info': {
                'title': self.name,
                'version': '1.0.0',
                'description': f'Converted from Postman collection: {self.name}'
            },
            'servers': [{'url': 'https://api.example.com'}],  # Default, should be updated
            'paths': {}
        }

        for request in self.requests:
            path = request['path']
            method = request['method'].lower()

            if path not in spec['paths']:
                spec['paths'][path] = {}

            # Create OpenAPI operation
            operation = {
                'summary': request['name'],
                'description': request['description'],
                'responses': {
                    '200': {
                        'description': 'Successful response'
                    }
                }
            }

            # Add parameters
            if request['params']:
                operation['parameters'] = []
                for param_name, param_value in request['params'].items():
                    operation['parameters'].append({
                        'name': param_name,
                        'in': 'query',
                        'schema': {'type': 'string'},
                        'example': param_value
                    })

            # Add request body
            if request['body'] and request['method'] in ['POST', 'PUT', 'PATCH']:
                operation['requestBody'] = {
                    'content': {
                        'application/json': {
                            'schema': {'type': 'object'},
                            'example': request['body']
                        }
                    }
                }

            spec['paths'][path][method] = operation

        return spec

class PostmanIntegration:
    """Main Postman integration class"""

    def __init__(self):
        self.collections = {}

    def load_collection(self, file_path: str) -> PostmanCollection:
        """Load Postman collection from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            collection = PostmanCollection(data)
            self.collections[collection.name] = collection

            log_event({
                'type': 'postman_collection_loaded',
                'summary': f'Loaded collection: {collection.name}',
                'details': {
                    'file_path': file_path,
                    'collection_name': collection.name
                }
            })

            return collection

        except Exception as e:
            log_event({
                'type': 'postman_collection_error',
                'summary': f'Failed to load collection: {str(e)}',
                'details': {'file_path': file_path, 'error': str(e)}
            })
            raise

    def convert_to_openapi(self, collection_name: str) -> Dict[str, Any]:
        """Convert Postman collection to OpenAPI spec"""
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' not loaded")

        collection = self.collections[collection_name]
        return collection.to_openapi_spec()

    def generate_aegis_tests(self, collection_name: str, output_dir: str = "tests_from_postman") -> str:
        """Generate AegisAPI tests from Postman collection"""
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' not loaded")

        collection = self.collections[collection_name]
        requests = collection.parse_requests()

        # Convert to OpenAPI format first
        openapi_spec = collection.to_openapi_spec()

        # Save as temporary OpenAPI file
        import tempfile
        import os
        from ..generator import generate_tests
        from pathlib import Path

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            import yaml
            yaml.dump(openapi_spec, f)
            temp_spec_path = f.name

        try:
            # Generate AegisAPI tests
            output_path = Path(output_dir)
            generate_tests(temp_spec_path, output_path, "none")

            log_event({
                'type': 'postman_tests_generated',
                'summary': f'Generated {len(requests)} tests from Postman collection',
                'details': {
                    'collection_name': collection_name,
                    'output_dir': str(output_path),
                    'test_count': len(requests)
                }
            })

            return str(output_path)

        finally:
            # Clean up temporary file
            os.unlink(temp_spec_path)

    def export_test_results(self, collection_name: str, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export AegisAPI test results back to Postman collection format"""
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' not loaded")

        collection = self.collections[collection_name]

        # Create new collection with test results
        export_collection = {
            'info': {
                'name': f'{collection_name} - AegisAPI Results',
                'description': f'Test results generated by AegisAPI AgentNN on {datetime.now().isoformat()}',
                'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
            },
            'item': []
        }

        # Add test results as collection items
        for test_name, result in test_results.items():
            item = {
                'name': f'Test Result: {test_name}',
                'description': f'AegisAPI test execution result for {test_name}',
                'request': {
                    'method': 'GET',
                    'header': [],
                    'url': {
                        'raw': 'http://localhost:8080/api/status',
                        'host': ['localhost'],
                        'port': '8080',
                        'path': ['api', 'status']
                    }
                },
                'response': [{
                    'name': f'Result for {test_name}',
                    'originalRequest': {},
                    'status': 'OK' if result.get('success', False) else 'Error',
                    'code': 200 if result.get('success', False) else 500,
                    'header': [{'key': 'Content-Type', 'value': 'application/json'}],
                    'body': json.dumps(result, indent=2),
                    'responseTime': result.get('duration', 0)
                }]
            }
            export_collection['item'].append(item)

        return export_collection

def create_postman_environment(results: Dict[str, Any]) -> Dict[str, Any]:
    """Create Postman environment file with test results"""
    environment = {
        'id': str(uuid.uuid4()),
        'name': 'AegisAPI Test Results',
        'values': []
    }

    # Add test result variables
    for key, value in results.items():
        if isinstance(value, (str, int, float, bool)):
            environment['values'].append({
                'key': key,
                'value': str(value),
                'enabled': True
            })

    return environment

# CLI Integration Functions
def import_postman_collection(collection_path: str, output_spec: str = None) -> str:
    """CLI command to import Postman collection and convert to OpenAPI"""
    integration = PostmanIntegration()
    collection = integration.load_collection(collection_path)

    if output_spec:
        openapi_spec = integration.convert_to_openapi(collection.name)
        with open(output_spec, 'w', encoding='utf-8') as f:
            import yaml
            yaml.dump(openapi_spec, f)
        return f"Converted Postman collection to OpenAPI spec: {output_spec}"

    return f"Loaded Postman collection: {collection.name} with {len(collection.requests)} requests"

def generate_from_postman(collection_path: str, output_dir: str = "tests_from_postman") -> str:
    """CLI command to generate AegisAPI tests directly from Postman collection"""
    integration = PostmanIntegration()
    collection = integration.load_collection(collection_path)
    test_dir = integration.generate_aegis_tests(collection.name, output_dir)

    return f"Generated AegisAPI tests from Postman collection in: {test_dir}"

# Example usage
if __name__ == "__main__":
    # Example: Convert Postman collection to AegisAPI tests
    integration = PostmanIntegration()

    # Load Postman collection
    collection = integration.load_collection("path/to/your/collection.json")

    # Generate AegisAPI tests
    test_dir = integration.generate_aegis_tests(collection.name)

    print(f"✅ Generated {len(collection.requests)} AegisAPI tests in: {test_dir}")

    # Convert to OpenAPI for further processing
    openapi_spec = integration.convert_to_openapi(collection.name)

    # Save OpenAPI spec
    with open("converted_api.yaml", 'w') as f:
        import yaml
        yaml.dump(openapi_spec, f)

    print("✅ Converted Postman collection to OpenAPI specification")
