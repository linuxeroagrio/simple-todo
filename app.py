import os

from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import get_config, ProductionConfig
from models import db, Task


def create_app(config_class=None):
    """Factory de la aplicación Flask."""
    app = Flask(__name__)
    
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    if hasattr(config_class, 'init_app'):
        config_class.init_app(app)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    register_routes(app)
    
    return app


def register_routes(app):
    """Registra todas las rutas de la aplicación."""
    
    @app.route('/')
    def index():
        """Página principal con la lista de tareas."""
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return render_template('index.html', tasks=tasks)
    
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """API: Obtiene todas las tareas."""
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return jsonify([task.to_dict() for task in tasks])
    
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """API: Crea una nueva tarea."""
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'El título es requerido'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', '')
        )
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """API: Obtiene una tarea específica."""
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict())
    
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """API: Actualiza una tarea existente."""
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        db.session.commit()
        return jsonify(task.to_dict())
    
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """API: Elimina una tarea."""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Tarea eliminada correctamente'}), 200
    
    @app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
    def toggle_task(task_id):
        """API: Cambia el estado de completado de una tarea."""
        task = Task.query.get_or_404(task_id)
        task.completed = not task.completed
        db.session.commit()
        return jsonify(task.to_dict())


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
