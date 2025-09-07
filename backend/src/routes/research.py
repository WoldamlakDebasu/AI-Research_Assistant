from flask import Blueprint, request, jsonify, Response
from flask_socketio import emit
import uuid
import threading
from src.agent import ResearchAgent

research_bp = Blueprint('research', __name__)

# Store active research tasks
active_tasks = {}

@research_bp.route('/research', methods=['POST'])
def start_research():
    """Start a new research task"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create research agent
        agent = ResearchAgent(task_id)
        active_tasks[task_id] = {
            'agent': agent,
            'status': 'started',
            'query': query
        }
        
        # Start research in background thread
        thread = threading.Thread(target=agent.research, args=(query,))
        thread.daemon = True
        thread.start()
        
        return jsonify({'task_id': task_id}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@research_bp.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """Get status of a research task"""
    try:
        if task_id not in active_tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = active_tasks[task_id]
        agent = task['agent']
        
        return jsonify({
            'task_id': task_id,
            'status': agent.status,
            'thoughts': agent.thoughts,
            'report': agent.report,
            'progress': agent.progress
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@research_bp.route('/download/<task_id>', methods=['GET'])
def download_report(task_id):
    """Download the research report as a text file"""
    try:
        if task_id not in active_tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = active_tasks[task_id]
        agent = task['agent']
        
        if agent.status != 'completed' or not agent.report:
            return jsonify({'error': 'Report not available'}), 404
            
        return Response(
            agent.report,
            mimetype="text/plain",
            headers={"Content-disposition": f"attachment; filename=research_report_{task_id[:8]}.txt"}
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

