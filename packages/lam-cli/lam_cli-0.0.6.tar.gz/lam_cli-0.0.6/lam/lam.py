#!/usr/bin/env python3

import json
import logging
import os
import shutil
import socket
import subprocess
from datetime import datetime

import click
from logtail import LogtailHandler
from posthog import Posthog

posthog = Posthog(project_api_key='phc_wfeHFG0p5yZIdBpjVYy00o5x1HbEpggdMzIuFYgNPSK', host='https://app.posthog.com')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

handler = LogtailHandler(source_token="TYz3WrrvC8ehYjXdAEGGyiDp")
logger.addHandler(handler)

jq_path = 'jq'

def truncate_long_strings(data, max_length=1000, truncation_msg="... (truncated)"):
    """
    Truncate long strings in a JSON object if they exceed max_length.
    Append a message to indicate truncation.
    """
    if isinstance(data, dict):
        return {key: truncate_long_strings(value, max_length, truncation_msg) for key, value in data.items()}
    elif isinstance(data, list):
        return [truncate_long_strings(item, max_length, truncation_msg) for item in data]
    elif isinstance(data, str):
        return data[:max_length] + truncation_msg if len(data) > max_length else data
    return data

def generate_distinct_id(workspace_id, flow_id):
    user_id = os.getuid()
    hostname = socket.gethostname()
    return f"{user_id}_{hostname}_{workspace_id}_{flow_id}"

def track_event(event_name, properties, workspace_id="local", flow_id="local"):
    logger.info(f"Event {event_name} triggered, with properties: {properties}")

    try:
        distinct_id = generate_distinct_id(workspace_id, flow_id)
        posthog.capture(distinct_id=distinct_id, event=event_name, properties=properties)
    except Exception as e:
        logger.error(f"Error logging event: {e}")

def parse_program_file(program_file):
    logger.info(f"Parsing program file: {program_file}")
    with open(program_file, 'r') as file:
        return ''.join(line for line in file if not line.strip().startswith('#'))

def run_jq(jq_script, input_data):
    logger.info(f"Running jq script {jq_script} with input data {truncate_long_strings(input_data)}")
    process = subprocess.Popen([jq_path, '-c', jq_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate(input=input_data)
    if error:
        logger.error(f"Error running jq: {error}")
    return output, error

def process_input(input, workspace_id, flow_id):
    logger.info(f"Processing input: {truncate_long_strings(input)}")
    if os.path.isfile(input):
        with open(input, 'r') as file:
            return file.read(), None
    try:
        json.loads(input)
        return input, None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        track_event('lam.run.error', {'error': f"Invalid JSON input: {e}", 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        return None, str(e)

def handle_jq_output(output, as_json, workspace_id, flow_id):
    logger.info(f"Handling jq output: {truncate_long_strings(output)}")
    try:
        json_output = json.loads(output)
        if not isinstance(json_output, dict):
            track_event('lam.run.warn', {'error': 'Invalid JSON output', 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
            return {"lam.result": json_output} if as_json else output, None
        return json_output if as_json else output, None
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON output, may be multiple JSON objects. Attempting to parse as JSON lines.")
        track_event('lam.run.warn', {'error': f"Invalid JSON output: {e}", 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        if as_json:
            json_objects = [json.loads(line) for line in output.strip().split('\n') if line]
            return {"lam.concatenated": json_objects}, None
        return output, "Failed to parse JSON output."

def write_to_result_file(result, result_file):
    with open(result_file, 'w') as file:
        file.write(json.dumps(result, indent=4))

@click.group()
def lam():
    pass

@lam.command()
@click.argument('program_file', type=click.Path(exists=True))
@click.argument('input', type=str)
@click.option('--workspace_id', default="local", help="Workspace ID")
@click.option('--flow_id', default="local", help="Flow ID")
@click.option('--as-json', is_flag=True, default=True, help="Output as JSON")
def run(program_file, input, workspace_id, flow_id, as_json):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"lam_run_{workspace_id}_{flow_id}_{timestamp}.log"
    result_file = f"lam_result_{workspace_id}_{flow_id}_{timestamp}.json"

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    logger.info(f"Logging to {log_file}")
    logger.info(f"Running command with program file: {program_file}, input: {truncate_long_strings(input)}, workspace_id: {workspace_id}, flow_id: {flow_id}, as_json: {as_json}")
    if not shutil.which("jq"):
        logger.error("Unable to find jq, killing process")
        click.echo({"lam.error": "jq is not installed"}, err=True)
        track_event('lam.run.error', {'error': 'jq is not installed', 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        write_to_result_file({"lam.error": "jq is not installed"}, result_file) 
        return

    input_data, error = process_input(input, workspace_id, flow_id)
    if error:
        click.echo({"lam.error": f"Invalid input: {error}"}, err=True)
        track_event('lam.run.error', {'error': f"Invalid input: {error}", 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        write_to_result_file({"lam.error": f"Invalid input: {error}"}, result_file)
        return

    jq_script = parse_program_file(program_file)
    track_event('lam.run.start', {'program_file': program_file, 'as_json': as_json, 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
    output, jq_error = run_jq(jq_script, input_data)

    if jq_error:
        click.echo({"lam.error": jq_error}, err=True)
        track_event('lam.run.run_jq_error', {'error': jq_error, 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        write_to_result_file({"lam.error": jq_error}, result_file)
        return

    result, error = handle_jq_output(output, as_json, workspace_id, flow_id)
    if error:
        click.echo({"lam.error": error}, err=True)
        track_event('lam.run.handle_jq_output_error', {'error': error, 'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        write_to_result_file({"lam.error": error}, result_file)
    else:
        click.echo(json.dumps(result, indent=4) if as_json else result)
        track_event('lam.run.success', {'workspace_id': workspace_id, 'flow_id': flow_id}, workspace_id, flow_id)
        write_to_result_file(result, result_file)

    logger.info("Run complete, waiting for event logger to finish")
    logger.removeHandler(file_handler)

if __name__ == '__main__':
    lam()